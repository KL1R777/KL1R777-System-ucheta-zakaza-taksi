from __future__ import annotations

import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from src.repositories.database import get_connection

try:
    import yaml
except ImportError: 
    yaml = None


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = PROJECT_ROOT / "out"


def _get_primary_key(conn, table: str) -> str | None:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
             AND tc.table_schema = kcu.table_schema
            WHERE tc.constraint_type = 'PRIMARY KEY'
              AND tc.table_name = %s
            ORDER BY kcu.ordinal_position
            LIMIT 1
            """,
            (table,),
        )
        row = cur.fetchone()
        return row[0] if row else None


def _get_foreign_keys(conn, table: str) -> dict[str, tuple[str, str]]:
    """column -> (ref_table, ref_column)"""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT kcu.column_name, ccu.table_name, ccu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
             AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage ccu
              ON ccu.constraint_name = tc.constraint_name
             AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY'
              AND tc.table_name = %s
            """,
            (table,),
        )
        return {r[0]: (r[1], r[2]) for r in cur.fetchall()}


def _get_referencing_foreign_keys(conn, table: str) -> list[tuple[str, str, str]]:
    """[(ref_table, fk_column, target_column)] — таблицы, которые ссылаются на нашу."""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT kcu.table_name, kcu.column_name, ccu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
             AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage ccu
              ON ccu.constraint_name = tc.constraint_name
             AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY'
              AND ccu.table_name = %s
            """,
            (table,),
        )
        return cur.fetchall()


def _fetch(conn, table: str, where: str | None = None, params: tuple = ()) -> list[dict]:
    with conn.cursor() as cur:
        sql = f'SELECT * FROM "{table}"'
        if where:
            sql += f" WHERE {where}"
        cur.execute(sql, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]


def _strip_id(col: str) -> str:
    """userID -> user, user_id -> user, orderStatus -> orderStatus."""
    if col.endswith("ID"):
        return col[:-2]
    if col.endswith("_id"):
        return col[:-3]
    return col


def _build_nested(conn, table: str, row: dict, max_depth: int, _depth: int = 0) -> dict:
    result = dict(row)
    if _depth >= max_depth:
        return result

   
    for col, (ref_table, ref_col) in _get_foreign_keys(conn, table).items():
        value = row.get(col)
        nested_key = _strip_id(col)
        if value is None:
            result[nested_key] = None
            continue
        related = _fetch(conn, ref_table, f'"{ref_col}" = %s', (value,))
        result[nested_key] = (
            _build_nested(conn, ref_table, related[0], max_depth, _depth + 1)
            if related
            else None
        )

   
    pk = _get_primary_key(conn, table)
    if pk and row.get(pk) is not None:
        for ref_table, fk_col, _target in _get_referencing_foreign_keys(conn, table):
            children = _fetch(conn, ref_table, f'"{fk_col}" = %s', (row[pk],))
            if children:
                result[ref_table.lower()] = [
                    _build_nested(conn, ref_table, c, max_depth, _depth + 1)
                    for c in children
                ]
    return result



def _serialize_json(data: Any, path: Path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


def _serialize_csv(rows: list[dict], path: Path) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    
    fieldnames: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for k in row:
            if k not in seen:
                seen.add(k)
                fieldnames.append(k)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            
            writer.writerow({
                k: (json.dumps(v, ensure_ascii=False, default=str)
                    if isinstance(v, (dict, list)) else v)
                for k, v in row.items()
            })


def _to_xml(tag: str, value: Any) -> ET.Element:
    el = ET.Element(tag)
    if isinstance(value, dict):
        for k, v in value.items():
            el.append(_to_xml(str(k), v))
    elif isinstance(value, list):
        for item in value:
            el.append(_to_xml("item", item))
    elif value is None:
        el.set("nil", "true")
    else:
        el.text = str(value)
    return el


def _serialize_xml(rows: list[dict], table: str, path: Path) -> None:
    root = ET.Element(table.lower())
    for row in rows:
        root.append(_to_xml("item", row))
    tree = ET.ElementTree(root)
    try:
        ET.indent(tree, space="  ")
    except AttributeError:
        pass
    tree.write(path, encoding="utf-8", xml_declaration=True)


def _serialize_yaml(data: Any, path: Path) -> None:
    if yaml is None:
        raise ImportError("Установите PyYAML: pip install pyyaml")
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)



def export_table(table: str, max_depth: int = 1) -> dict[str, Path]:
    
    table = table.lower()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    conn = get_connection()
    
    try:
        raw_rows = _fetch(conn, table)
        nested_rows = [
            _build_nested(conn, table, row, max_depth=max_depth)
            for row in raw_rows
        ]
    finally:
        conn.close()

    paths = {
        "json": OUT_DIR / "data.json",
        "csv":  OUT_DIR / "data.csv",
        "xml":  OUT_DIR / "data.xml",
        "yaml": OUT_DIR / "data.yaml",
    }

    _serialize_json(nested_rows, paths["json"])
    _serialize_csv(nested_rows, paths["csv"]) 
    _serialize_xml(nested_rows, table, paths["xml"])
    _serialize_yaml(nested_rows, paths["yaml"])

    print(f"Экспортировано {len(nested_rows)} записей из {table} в {OUT_DIR}")
    return paths


if __name__ == "__main__":
    import sys
    table = sys.argv[1] if len(sys.argv) > 1 else "Orders"
    export_table(table)