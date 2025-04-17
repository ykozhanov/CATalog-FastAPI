from abc import ABC, abstractmethod
from src.auth_service.app.models import User
from src.auth_service.app.schemas.user_schemas import UserCreateSchema, UserUpdateSchema


class AsyncUserRepositoryInterface(ABC):
    """Интерфейс асинхронного репозитория для работы с пользователями"""

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User:
        """Получить пользователя по ID. Если пользователь не найден, выбросит исключение UserNotFoundException"""
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> User:
        """Получить пользователя по username. Если пользователь не найден, выбросит исключение UserNotFoundException"""
        pass

    @abstractmethod
    async def create(self, user: UserCreateSchema) -> User:
        """Создать нового пользователя"""
        pass

    @abstractmethod
    async def update(self, updated_user: UserUpdateSchema) -> User:
        """Обновить пользователя. Если пользователь не найден, выбросит исключение UserNotFoundException"""
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        """Удалить пользователя по ID. Если пользователь не найден, выбросит исключение UserNotFoundException"""
        pass
