from src.repositories import user_repo, role_repo
from src.services import security 
from src.models.users import User


def create_user(email: str, name: str, password: str, userRole: int, money: float = 0.0) -> User | bool:
    if not security.is_valid_email(email=email):
        print("Неправильный ввод email")
        return False

    if not role_repo.get_role_by_id(id=userRole):
        print("Неизвестная роль, выберите (пассажир/таксист)")
        return False

    hashed_password = security.hash_password(password)


    user = user_repo.create_user(
        email=email, name=name, hashed_password=hashed_password,
        userRole=userRole, money=money
    )
    print(f"Аккаунт {user.email} успешно создан")
    return user

def login_user(email: str, password: str):

    if not security.is_valid_email(email):
        print("Неправильно введен email")
        return 0

    
    user = user_repo.get_user_by_email(email=email)

    if not user:
        print("email незарегистрирован")
        return False

    elif not security.verify_password(password, user.hashed_password):
        print("Неправильный пароль")
        return False

    print(f"Добро пожаловать, {user.name}!")

    return True

def logout_user():

    print("До свидания!")

    return True
    
    
    