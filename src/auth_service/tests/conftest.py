from dotenv import load_dotenv

# Подгружаем переменные из .env
load_dotenv()

import pytest
from httpx import AsyncClient, ASGITransport

from unittest.mock import AsyncMock

from src.auth_service.app.main import app
from src.auth_service.app.core.database import Base, engine, AsyncSessionLocal

from src.auth_service.app.models import *

from src.auth_service.tests.factories import UserFactory
from src.auth_service.app.services import AsyncUserService, JWTService


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c


@pytest.fixture
async def session():
    async with AsyncSessionLocal() as s:
        yield s


@pytest.fixture
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def user() -> UserFactory:
    return UserFactory()


@pytest.fixture
def mock_user_repo():
    return AsyncMock()


@pytest.fixture
def mock_user_service(mock_user_repo):
    return AsyncUserService(user_repo=mock_user_repo)


@pytest.fixture
def jwt_service():
    return JWTService()
