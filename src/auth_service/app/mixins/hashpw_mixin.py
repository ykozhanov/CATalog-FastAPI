import bcrypt


class HashPWMixin:
    """Миксин для работы с хэшем пароля"""

    @staticmethod
    def hashpw(password: str) -> str:
        """Получить хэш пароля"""
        return bcrypt.hashpw(password=password.encode("utf-8"), salt=bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def check_hashpw(password: str, hashed_password: bytes) -> bool:
        """Сравнить пароль с хэшем"""
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
