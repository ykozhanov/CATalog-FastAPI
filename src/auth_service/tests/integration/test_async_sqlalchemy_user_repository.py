import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth_service.app.repositories import AsyncSQLAlchemyUserRepository
from src.auth_service.app.schemas.user_schemas import UserCreateSchema, UserUpdateSchema
from src.auth_service.app.exceptions.user_exceptions import UserNotFoundException


async def test_create_user(session: AsyncSession, init_db, user):
    repo = AsyncSQLAlchemyUserRepository(session)
    user_data = UserCreateSchema(
        username=user.username,
        hashed_password=user.hashed_password,
        email=user.email,
    )

    new_user = await repo.create(user_data)

    assert new_user.username == user_data.username
    assert new_user.email == user_data.email
    assert not new_user.is_deleted


async def test_get_by_id(session: AsyncSession, init_db, user):
    session.add(user)
    await session.commit()

    repo = AsyncSQLAlchemyUserRepository(session)
    fetched_user = await repo.get_by_id(user.id)

    assert fetched_user.id == user.id


async def test_get_by_id_not_found(session: AsyncSession, init_db):
    repo = AsyncSQLAlchemyUserRepository(session)

    with pytest.raises(UserNotFoundException):
        await repo.get_by_id(9999)


async def test_get_by_username(session: AsyncSession, init_db, user):
    session.add(user)
    await session.commit()

    repo = AsyncSQLAlchemyUserRepository(session)
    fetched_user = await repo.get_by_username(user.username)

    assert fetched_user.username == user.username


async def test_update_user(session: AsyncSession, init_db, user):
    new_email = "new@example.com"

    session.add(user)
    await session.commit()

    repo = AsyncSQLAlchemyUserRepository(session)
    update_data = UserUpdateSchema(id=user.id, email=new_email)

    updated_user = await repo.update(update_data)

    assert updated_user.email == new_email
    assert updated_user.username == user.username


async def test_delete_user(session: AsyncSession, init_db, user):
    session.add(user)
    await session.commit()

    repo = AsyncSQLAlchemyUserRepository(session)
    await repo.delete(user.id)

    with pytest.raises(UserNotFoundException):
        await repo.get_by_id(user.id)
