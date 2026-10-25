from src.repositories.database import get_connection
from src.models.orders import Order
from typing import Optional, List




def take_order(id: int, driverID: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Orders SET driverID = %s, orderStatus = 2 WHERE id = %s",
            (driverID, id)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Ошибка take_order: {e}")
    finally:
        cursor.close()
        conn.close()


def completed_order(id: int, driverID: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Orders SET orderStatus = 3 WHERE id = %s AND driverID = %s AND orderStatus = 2",
            (id, driverID)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Ошибка completed_order: {e}")
    finally:
        cursor.close()
        conn.close()


def cancelled_order(id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Orders SET orderStatus = 4 WHERE id = %s AND orderStatus IN (1, 2)",
            (id,)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Ошибка cancelled_order: {e}")
    finally:
        cursor.close()
        conn.close()



def create_order(userID: int, price: float, address: str) -> Optional[int]:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Orders (userID, price, address, orderStatus) "
            "VALUES (%s, %s, %s, 1) RETURNING id",
            (userID, price, address)
        )
        row = cursor.fetchone()
        conn.commit()
        return row[0]
    except Exception as e:
        conn.rollback()
        print(f"Ошибка create_order: {e}")
        return None
    finally:
        cursor.close()
        conn.close()



def get_all_orders(orderStatus: int = 1) -> List[Order]:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Orders WHERE orderStatus = %s", (orderStatus,))
        rows = cursor.fetchall()

        return [
            Order(id=r[0], userID=r[1], price=r[2], driverID=r[3], address=r[4], orderStatus=r[5])
            for r in rows
        ]
    except Exception as e:
        print(f"Ошибка get_all_orders: {e}")
        return []
    finally:
        cursor.close()

        conn.close()


def get_orders_by_user_id(userID: int) -> List[Order]:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Orders WHERE userID = %s ORDER BY id DESC", (userID,))
        rows = cursor.fetchall()
        return [
            Order(id=r[0], userID=r[1], price=r[2], driverID=r[3], address=r[4], orderStatus=r[5])
            for r in rows
        ]
    except Exception as e:
        print(f"Ошибка get_orders_by_user_id: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_order_by_id(id: int) -> Optional[Order]:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Orders WHERE id = %s", (id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Order(id=row[0], userID=row[1], price=row[2], driverID=row[3], address=row[4], orderStatus=row[5])
    except Exception as e:
        print(f"Ошибка get_order_by_id: {e}")
        return None
    finally:
        cursor.close()
        conn.close()