from src.repositories import status_repo
from src.models import  enums




def create_status(status: enums.OrderStatus):

    status_row = status_repo.get_status_by_name(status=status)

    if status_row:

        return status_row

    else:
        status_repo.create_status(status=status)

        return status_repo.get_status_by_name(status=status)


