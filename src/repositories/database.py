import psycopg2
import time
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SQL_FILE = PROJECT_ROOT / "sql" / "main.sql"


def restore_db():
    time.sleep(2)

    if not SQL_FILE.exists():
        raise FileNotFoundError(f"Не найден SQL-файл: {SQL_FILE}")

    with open(SQL_FILE, "r", encoding="utf-8") as f:
        sql_script = f.read()

    conn = get_connection()
    cursor = conn.cursor()

    
    cursor.execute("""
        DROP TABLE IF EXISTS Reviews CASCADE;
        DROP TABLE IF EXISTS Orders CASCADE;
        DROP TABLE IF EXISTS Users CASCADE;
        DROP TABLE IF EXISTS Status CASCADE;
        DROP TABLE IF EXISTS UserRoles CASCADE;
        DROP TYPE IF EXISTS order_status_enum CASCADE;
    """)

    
    cursor.execute(sql_script)

    conn.commit()
    cursor.close()
    conn.close()

    print(f"База создана из {SQL_FILE}")


def get_connection():
    return psycopg2.connect(
        dbname="mydatabase",
        user="myuser",
        password="mypassword",
        host="localhost",
        port="5432"
    )