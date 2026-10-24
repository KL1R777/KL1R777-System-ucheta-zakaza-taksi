from typing import Union
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

        return Status(id=row[0], status=row[1])

    except Exception as e:
        ...


    finally:
        cursor.close()
        conn.close()


def create_status(status):
    ...