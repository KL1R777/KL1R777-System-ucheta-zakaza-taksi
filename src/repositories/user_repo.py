from src.repositories.database import get_connection
from src.models.users import User


def get_user_by_id(id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Users WHERE id = %s", (id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return User(id=row[0], email=row[1], name=row[2],
                    hashed_password=row[3], userRole=row[4], money=row[5])
    except Exception as e:
        print(f"Ошибка get_user_by_id: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def create_user(email: str, name: str, hashed_password: str, userRole: int, money: float = 0.0) -> User | None:
    conn = get_connection()
    cursor = conn.cursor()
    try:

        cursor.execute(
            """INSERT INTO Users (email, name, hashed_password, userRole, money) 
               VALUES (%s, %s, %s, %s, %s) 
               RETURNING id, email, name, hashed_password, userRole, money""",
            (email, name, hashed_password, userRole, money)
        )
        row = cursor.fetchone()
        conn.commit()


        return User(
            id=row[0], email=row[1], name=row[2],
            hashed_password=row[3], userRole=row[4], money=row[5]
        )
    except Exception as e:
        conn.rollback()
        print(f"Ошибка create_user: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_user_by_email(email: str) -> User | None:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
        row = cursor.fetchone()
        if row is None:
            return None
        return User(id=row[0], email=row[1], name=row[2],
                    hashed_password=row[3], userRole=row[4], money=row[5])
    except Exception as e:
        print(f"Ошибка get_user_by_email: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def delete_user(id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:

        cursor.execute("DELETE FROM Users WHERE id = %s", (id,))
        conn.commit()
        print(f"Аккаунт {id} удален")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка delete_user: {e}")
    finally:
        cursor.close()
        conn.close()