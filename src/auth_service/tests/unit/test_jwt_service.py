import pytest
import jwt
from datetime import datetime, timedelta, UTC
from freezegun import freeze_time

from src.auth_service.app.enums import JWTType
from src.auth_service.app.exceptions.domain_exceptions import UnauthorizedException
from src.auth_service.app.core.config import settings


def test_get_refresh_token_contains_correct_payload(jwt_service, user):
    token = jwt_service.get_refresh_token(str(user.id))
    decoded = jwt.decode(
        token,
        settings.JWT_PUBLIC_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )

    assert decoded.get("sub") == str(user.id)
    assert decoded.get("type") == JWTType.REFRESH
    assert "exp" in decoded


@freeze_time("2025-01-01 12:00:00", tz_offset=0)
def test_get_access_token_updates_payload_type_and_exp(jwt_service, user):
    refresh_token = jwt_service.get_refresh_token(str(user.id))
    access_token = jwt_service.get_access_token(refresh_token)
    decoded = jwt.decode(
        access_token,
        settings.JWT_PUBLIC_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )

    assert decoded.get("sub") == str(user.id)
    assert decoded.get("type") == JWTType.ACCESS
    assert decoded.get("exp") == int(
        (
            datetime(2025, 1, 1, 12, 0, 0, tzinfo=UTC)
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
        ).timestamp()
    )


def test_decode_jwt_invalid_token_raises(jwt_service):
    invalid_token = "not.a.valid.token"

    with pytest.raises(UnauthorizedException):
        jwt_service.decode_jwt(invalid_token)
