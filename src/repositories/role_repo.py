from src.repositories.database import get_connection
from src.models.user_roles import UserRole


def get_role_by_id(id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM UserRoles WHERE id = %s", (id,))

        row = cursor.fetchone()

        return UserRole(id=row[0], role=row[1])

    except Exception as e:
        conn.rollback()
        print("Какая то ошибка")

    finally:
        cursor.close()
        conn.close()


def create_role(role: str):
    try:

        conn = get_connection()
        cursor = conn.cursor()

        
        cursor.execute("INSERT INTO UserRoles (role) VALUES (%s)", (role,))



        conn.commit()


        return

    except Exception as e:
        conn.rollback()
        print("Какая то ошибка")

    finally:
        cursor.close()
        conn.close()



def get_role_by_name(role: str):

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM UserRoles WHERE role = %s", (role,))

        row = cursor.fetchone()
        if row:
            return UserRole(id=row[0], role=row[1])
        else:
            print("Роли нету")


    except Exception as e:
        print("Ошибка")

    finally:

        cursor.close()
        conn.close()




    

