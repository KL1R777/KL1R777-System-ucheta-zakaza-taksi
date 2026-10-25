from src.services import status_service

from src.models.enums import OrderStatus







status1 = status_service.create_status(OrderStatus.FREE)
status2 = status_service.create_status(OrderStatus.IN_PROGRESS)
status3 = status_service.create_status(OrderStatus.COMPLETED)
status4 = status_service.create_status(OrderStatus.CANCELLED)


from src.repositories import role_repo

from src.menu import run_app


def main():


    role_repo.create_role("пассажир")
    role_repo.create_role("таксист")



    run_app()



if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print("\nВыход из программы")
