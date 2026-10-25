from src.repositories.database import get_connection

def create_review(orderID: int, userID: int, rating: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Reviews (orderID, userID, rating) VALUES (%s, %s, %s)",
            (orderID, userID, rating)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Ошибка create_review: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def has_review_for_order(orderID: int) -> bool:

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT 1 FROM Reviews WHERE orderID = %s", (orderID,))
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"Ошибка has_review_for_order: {e}")
        return False
    finally:
        cursor.close()
        conn.close()