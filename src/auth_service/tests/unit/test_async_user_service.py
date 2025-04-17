import pytest

from src.auth_service.app.schemas.user_schemas import (
    UserCreateInSchema,
    UserUpdateSchema,
)
from src.auth_service.app.exceptions import (
    UserNotFoundException,
    UserConflictExceptions,
)


async def test_create_user_success(mock_user_service, mock_user_repo, user):
    mock_user_repo.get_by_username.side_effect = UserNotFoundException()
    mock_user_repo.create.return_value = user

    input_data = UserCreateInSchema(
        username=user.username,
        email=user.email,
        password=user.hashed_password,
    )

    result = await mock_user_service.create(input_data)

    assert result.username == input_data.username
    assert result.email == input_data.email

    mock_user_repo.create.assert_called_once()
    mock_user_repo.get_by_username.assert_called_once_with(user.username)


async def test_create_user_conflict(mock_user_service, mock_user_repo, user):
    mock_user_repo.get_by_username.return_value = user

    input_data = UserCreateInSchema(
        username=user.username,
        email=user.email,
        password=user.hashed_password,
    )

    with pytest.raises(UserConflictExceptions):
        await mock_user_service.create(input_data)


async def test_update_user_success(mock_user_service, mock_user_repo, user):
    mock_user_repo.get_by_username.side_effect = UserNotFoundException()
    mock_user_repo.update.return_value = user

    update_data = UserUpdateSchema(
        id=user.id,
        username=user.username,
        email=user.email,
        role=None,
    )

    result = await mock_user_service.update(update_data)

    assert result.username == user.username
    assert result.email == user.email


async def test_update_user_conflict(mock_user_service, mock_user_repo, user):
    mock_user_repo.get_by_username.return_value = user

    update_data = UserUpdateSchema(
        id=user.id + 1,
        username=user.username,
        email=user.email,
    )

    with pytest.raises(UserConflictExceptions):
        await mock_user_service.update(update_data)


async def test_delete_user(mock_user_service, mock_user_repo):
    await mock_user_service.delete(1)
    mock_user_repo.delete.assert_called_once_with(1)


async def test_get_by_id(mock_user_service, mock_user_repo, user):
    mock_user_repo.get_by_id.return_value = user

    result = await mock_user_service.get_by_id(user.id)

    assert result.username == user.username
    mock_user_repo.get_by_id.assert_called_once_with(user.id)


async def test_get_by_username(mock_user_service, mock_user_repo, user):
    mock_user_repo.get_by_username.return_value = user

    result = await mock_user_service.get_by_username(user.username)

    assert result.email == user.email
    assert result.username == user.username
    mock_user_repo.get_by_username.assert_called_once_with(user.username)
