from src.auth_service.app.interfaces import (
    AsyncUserRepositoryInterface,
    AsyncUserServiceInterface,
)
from src.auth_service.app.schemas.user_schemas import (
    UserCreateInSchema,
    UserReadSchema,
    UserCreateSchema,
    UserUpdateSchema,
)
from src.auth_service.app.mixins import HashPWMixin
from src.auth_service.app.exceptions import (
    UserNotFoundException,
    UserConflictExceptions,
)


class AsyncUserService(AsyncUserServiceInterface, HashPWMixin):
    """Асинхронный сервис для работы с пользователями"""

    def __init__(self, user_repo: AsyncUserRepositoryInterface):
        self.user_repo = user_repo

    async def create(self, user: UserCreateInSchema) -> UserReadSchema:
        await self._check_username_not_exists(user.username)
        hashed_password = self.hashpw(user.password)
        user = UserCreateSchema(
            username=user.username,
            hashed_password=hashed_password,
            email=user.email,
        )
        new_user = await self.user_repo.create(user)
        return UserReadSchema.model_validate(new_user)

    async def _check_username_not_exists(self, username: str) -> None:
        """Проверка на конфликт по username пользователя"""
        try:
            await self.user_repo.get_by_username(username)
            raise UserConflictExceptions("Пользователь с таким username уже существует")
        except UserNotFoundException:
            return

    async def update(self, updated_user: UserUpdateSchema) -> UserReadSchema:
        await self._check_username_not_exists(updated_user.username)
        user = await self.user_repo.update(updated_user)
        return UserReadSchema.model_validate(user)

    async def delete(self, user_id: int) -> None:
        await self.user_repo.delete(user_id)

    async def get_by_id(self, user_id: int) -> UserReadSchema:
        user = await self.user_repo.get_by_id(user_id)
        return UserReadSchema.model_validate(user)

    async def get_by_username(self, username: str) -> UserReadSchema:
        user = await self.user_repo.get_by_username(username)
        return UserReadSchema.model_validate(user)
