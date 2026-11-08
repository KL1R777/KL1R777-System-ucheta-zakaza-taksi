from src.services import status_service

from src.models.enums import OrderStatus










from src.repositories import role_repo

from src.menu import run_app


def main():






    run_app()



if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print("\nВыход из программы")
