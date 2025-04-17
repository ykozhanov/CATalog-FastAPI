from datetime import datetime, UTC, timedelta

from src.auth_service.app.interfaces import JWTServiceInterface
from src.auth_service.app.mixins import JWTMixin
from src.auth_service.app.enums import JWTType
from src.auth_service.app.core.config import settings
from src.auth_service.app.schemas.jwt_shemas import JWTPayloadSchema


class JWTService(JWTServiceInterface, JWTMixin):
    """Сервис для работы с JWT токенами"""

    def get_access_token(self, refresh_token: str) -> str:
        payload = self.decode_jwt(refresh_token)
        payload.type = JWTType.ACCESS
        payload.exp = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
        return self.encode_jwt(payload)

    def get_refresh_token(self, sub: str) -> str:
        payload = JWTPayloadSchema(
            sub=sub,
            exp=datetime.now(UTC) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE),
            type=JWTType.REFRESH,
        )
        return self.encode_jwt(payload)
