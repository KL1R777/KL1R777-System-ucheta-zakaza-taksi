from src.services import user_services, order_service, review_service
from src.repositories import user_repo, order_repo



def start_auth():
    print("\n=== СИСТЕМА УЧЕТА ЗАКАЗОВ ТАКСИ ===")

    while True:
        print("\n1. Я Пассажир\n2. Я Таксист\n0. Выход")
        role_choice = input("Выберите роль (1 или 2): ")

        if role_choice == "0":
            return None

        if role_choice not in ["1", "2"]:
            print("Неверный выбор.")
            continue

        role_id = int(role_choice)
        email = input("Введите логин (email): ")
        password = input("Введите пароль: ")


        user = user_repo.get_user_by_email(email)

        if user:

            if user_services.login_user(email, password):

                if user.userRole != role_id:
                    print("Внимание: Вы выбрали не ту роль! Вход выполнен под вашей реальной ролью.")
                return user
            else:
                print("Неверный пароль.")
        else:

            print("Пользователь не найден.")
            ans = input("Создать аккаунт? (да/нет): ")

            if ans.lower() == "да":

                name = input("Введите ваше имя: ")
                new_user = user_services.create_user(
                    email=email, name=name, password=password, userRole=role_id
                )
                if new_user:
                    return new_user
            else:

                print("Регистрация отменена.")
                return None


def passenger_menu(user):
    while True:
        print(f"\n--- МЕНЮ ПАССАЖИРА ({user.name}) ---")
        print("1. Заказать такси")
        print("2. История заказов")
        print("3. Проверить статус заказа")
        print("4. Отменить заказ")
        print("5. Оценить поездку")
        print("0. Выйти из аккаунта")

        choice = input("Выберите действие: ")

        if choice == "1":
            address = input("Куда поедем? (введите адрес): ")
            price = order_service.calculate_price(address)
            if price > 0:
                order_service.create_order(userID=user.id, price=price, address=address)

        elif choice == "2":
            order_service.get_history(user.id)

        elif choice == "3":
            try:
                oid = int(input("Введите номер заказа: "))
                order_service.check_status(oid)
            except ValueError:
                print("❌ Номер должен быть числом.")

        elif choice == "4":
            try:
                oid = int(input("Введите номер заказа для отмены: "))

                order_service.cancelled_order(id=oid, userID=user.id)
            except ValueError:
                print("Номер должен быть числом.")

        elif choice == "5":
            try:
                oid = int(input("Введите номер заказа: "))
                rating = int(input("Оцените от 1 до 5: "))
                review_service.rate_order(oid, user.id, rating)
            except ValueError:
                print("Некорректный ввод.")

        elif choice == "0":
            user_services.logout_user()
            break



def driver_menu(user):
    while True:
        print(f"\n--- МЕНЮ ТАКСИСТА ({user.name}) ---")
        print("1. Открыть список доступных заказов (Переход к списку)")
        print("2. Принять заказ (Выбрать заказ)")
        print("3. Завершить текущий заказ")
        print("0. Выйти из аккаунта")

        choice = input("Выберите действие: ")

        if choice == "1":
            orders = order_service.get_available_orders()
            if not orders:
                print("Нет доступных заказов.")
            for o in orders:
                print(f"Заказ №{o.id} | Адрес: {o.address} | Цена: {o.price}")

        elif choice == "2":
            try:
                oid = int(input("Введите номер заказа, который хотите взять: "))


                active_driver_orders = order_repo.get_all_orders(2)
                is_busy = any(o.driverID == user.id for o in active_driver_orders)

                if is_busy:
                    print("Уведомление: Вы уже выполняете текущий заказ!")
                    continue


                target_order = order_repo.get_order_by_id(oid)

                if not target_order or target_order.orderStatus != 1:
                    print("Вывод: 'Заказ уже занят' (или не существует)")
                    continue


                order_service.take_order(id=oid, driverID=user.id)

                # 4. "Переход в карточку заказа"
                print("\n--- КАРТОЧКА ЗАКАЗА ---")
                print(f"Заказ №{target_order.id}")
                print(f"Адрес: {target_order.address}")
                print(f"Цена: {target_order.price}")
                print("Статус: В пути")
                print("-----------------------")


            except ValueError:
                print("Номер должен быть числом.")

        elif choice == "3":
            active_orders = [o for o in order_repo.get_all_orders(2) if o.driverID == user.id]

            if not active_orders:
                print("У вас нет активных заказов в работе.")
                continue

            print("\nВаши активные заказы:")
            for o in active_orders:
                print(f"Заказ №{o.id} | Адрес: {o.address} | Цена: {o.price}")

            try:
                oid = int(input("Введите номер заказа для завершения (или 0 для отмены): "))
                if oid == 0:
                    continue
                order_service.completed_order(id=oid, driverID=user.id)
            except ValueError:
                print("Номер должен быть числом.")
        elif choice == "0":
            break


def run_app():
    while True:
        user = start_auth()
        if not user:
            print("Выход из программы.")
            break

        if user.userRole == 1:
            passenger_menu(user)
        elif user.userRole == 2:
            driver_menu(user)