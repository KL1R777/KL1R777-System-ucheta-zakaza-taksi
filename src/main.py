from src.services import user_services, role_service
from src.repositories import role_repo, user_repo
from src.repositories.database import get_connection, restore_db

restore_db()

def main1():
    print("=== 1. Проверка подключения к БД ===")
    try:
        conn = get_connection()
        conn.close()
        print("✅ Подключение работает")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return

    print("\n=== 2. Создание роли ===")
    try:
        role_service.create_role("Шофер")
        print("✅ Роль создана (или уже была)")
    except Exception as e:
        print(f"❌ Ошибка при создании роли: {e}")
        return

    print("\n=== 3. Создание пользователя ===")
    try:
        # Внимание: проверь, как называется аргумент в твоей функции!
        user = user_services.create_user(
            email="test@test.test",
            name="test",
            password="test",   # или password_hash?
            userRole=1
        )
        print(f"Результат create_user: {user}")  # <-- Смотрим, что вернулось
    except Exception as e:
        print(f"❌ Ошибка при создании пользователя: {e}")
        return

    print("\n=== 4. Поиск пользователя ===")
    try:
        found = user_repo.get_user_by_email("test@test.test")
        print(f"Найден: {found}")
        if found:
            print(f"ID: {found.id}, Name: {found.name}, Money: {found.money}")
    except Exception as e:
        print(f"❌ Ошибка при поиске: {e}")


def main2():
    role = role_service.create_role("Шофер")

    print(f"Role: ID={role.id}, name = {role.role}")


if __name__ == '__main__':
    main1()
    main2()