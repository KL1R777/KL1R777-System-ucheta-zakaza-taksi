from passlib.context import CryptContext
import re

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



def is_valid_email(email: str) -> bool:
    # ^[a-zA-Z0-9_.+-]+  — начало, буквы/цифры/точки/плюсы
    # @                   — собака
    # [a-zA-Z0-9-]+       — домен (например, gmail или yandex)
    # \.                  — точка
    # [a-zA-Z0-9-.]+$     — зона (.ru, .com)
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None