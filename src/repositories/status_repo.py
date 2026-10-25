
from src.models.enums import OrderStatus
from src.models.status import Status
from src.repositories.database import get_connection



def get_status_by_name(status: OrderStatus):

    try:
        conn = get_connection()
        cursor = conn.cursor()
        status_str = status.value
        cursor.execute("SELECT * FROM Status WHERE status = %s", (status_str,))

        row = cursor.fetchone()

        if row:

            return Status(id=row[0], status=row[1])

        return

    except Exception as e:
        conn.rollback()
        print("Ошибка")


    finally:
        cursor.close()
        conn.close()


def create_status(status: OrderStatus):

    try:
        conn = get_connection()
        cursor = conn.cursor()


        cursor.execute("INSERT INTO Status (status) VALUES (%s)", (status.value, ))

        conn.commit()

        return



    except Exception as e:
        conn.rollback()
        print("Какая то ошибка")


    finally:
        cursor.close()
        conn.close()