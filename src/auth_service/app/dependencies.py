from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth_service.app.core.database import get_session
from src.auth_service.app.services import AsyncUserService
from src.auth_service.app.repositories import AsyncSQLAlchemyUserRepository
from src.auth_service.app.services import JWTService
from src.auth_service.app.core.config import settings
from src.auth_service.app.exceptions.domain_exceptions import UnauthorizedException


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


def get_user_service(db: AsyncSession = Depends(get_session)) -> AsyncUserService:
    user_repo = AsyncSQLAlchemyUserRepository(db)
    return AsyncUserService(user_repo)


def get_jwt_service() -> JWTService:
    return JWTService()


def verify_service_credentials(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> None:
    if (
        form_data.username != settings.SERVICE_USERNAME
        or form_data.password != settings.SERVICE_PASSWORD
    ):
        raise UnauthorizedException()


__all__ = [
    "get_user_service",
    "get_jwt_service",
    "oauth2_scheme",
    "verify_service_credentials",
]
