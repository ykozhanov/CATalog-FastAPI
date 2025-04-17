"""
Для генерации RSA ключей используйте команды:

`openssl genrsa -out jwt-private.pem 2048`
Эта команда генерирует закрытый ключ RSA длиной 2048 бит и сохраняет его в файл jwt-private.pem.

`openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem`
Эта команда извлекает открытый ключ из ранее сгенерированного закрытого ключа, который хранится в файле jwt-private.pem.
"""

import jwt
from src.auth_service.app.core.config import settings
from src.auth_service.app.exceptions.domain_exceptions import UnauthorizedException
from src.auth_service.app.schemas.jwt_shemas import JWTPayloadSchema


class JWTMixin:
    """**Миксин для работы с JSON Web Tokens (JWT)**

    Предоставляет методы для кодирования и декодирования JWT.
    Использует RSA ключи для подписи и проверки токенов.
    """

    @staticmethod
    def encode_jwt(payload: JWTPayloadSchema) -> str:
        """Кодирует данные в JWT"""
        return jwt.encode(
            payload=payload.model_dump(),
            key=settings.JWT_PRIVATE_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    @staticmethod
    def decode_jwt(token: str) -> JWTPayloadSchema:
        """Декодирует JWT"""
        try:
            payload = jwt.decode(
                jwt=token,
                key=settings.JWT_PUBLIC_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            return JWTPayloadSchema.model_validate(payload)
        except jwt.InvalidTokenError as e:
            raise UnauthorizedException("Токен некорректный или устарел", details=e)
