from abc import ABC, abstractmethod


class JWTServiceInterface(ABC):
    """Интерфейс для работы с JWT токенами"""

    @abstractmethod
    def get_access_token(self, refresh_token: str) -> str:
        """Получить Access JWT token"""
        pass


    @abstractmethod
    def get_refresh_token(self, sub: str) -> str:
        """Получить Refresh JWT token"""
        pass
