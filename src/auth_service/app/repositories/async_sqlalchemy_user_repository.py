from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth_service.app.interfaces import AsyncUserRepositoryInterface
from src.auth_service.app.models import User
from src.auth_service.app.schemas.user_schemas import UserCreateSchema, UserUpdateSchema
from src.auth_service.app.exceptions.user_exceptions import UserNotFoundException


class AsyncSQLAlchemyUserRepository(AsyncUserRepositoryInterface):
    """Асинхронный репозиторий для работы с пользователями через SQLAlchemy"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: int) -> User:
        user = await self.session.execute(
            select(User).filter(User.id == user_id, User.is_deleted == False)
        )
        user = user.scalar_one_or_none()
        if not user:
            raise UserNotFoundException()
        return user

    async def get_by_username(self, username: str) -> User:
        user = await self.session.execute(
            select(User).filter(User.username == username, User.is_deleted == False)
        )
        user = user.scalar_one_or_none()
        if not user:
            raise UserNotFoundException()
        return user

    async def create(self, user: UserCreateSchema) -> User:
        new_user = User(
            username=user.username,
            hashed_password=user.hashed_password,
            email=user.email,
        )
        self.session.add(new_user)
        await self.session.commit()
        return new_user

    async def update(self, updated_user: UserUpdateSchema) -> User:
        user = await self.get_by_id(updated_user.id)

        if updated_user.email:
            user.email = str(updated_user.email)
        if updated_user.username:
            user.username = updated_user.username
        if updated_user.role:
            user.role = updated_user.role

        await self.session.commit()
        return user

    async def delete(self, user_id: int) -> None:
        user = await self.get_by_id(user_id)
        user.soft_delete()
        await self.session.commit()
