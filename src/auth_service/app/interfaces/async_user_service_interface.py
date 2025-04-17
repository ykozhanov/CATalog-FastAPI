from abc import ABC, abstractmethod

from src.auth_service.app.schemas.user_schemas import (
    UserReadSchema,
    UserCreateInSchema,
    UserUpdateSchema,
)


class AsyncUserServiceInterface(ABC):
    """Интерфейс асинхронного сервиса для работы с пользователями"""

    @abstractmethod
    async def create(self, user: UserCreateInSchema) -> UserReadSchema:
        """Создать нового пользователя"""
        pass

    @abstractmethod
    async def update(self, updated_user: UserUpdateSchema) -> UserReadSchema:
        """Обновить пользователя"""
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        """Удалить пользователя"""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> UserReadSchema:
        """Получить пользователя по ID"""
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> UserReadSchema:
        """Получить пользователя по username"""
        pass

