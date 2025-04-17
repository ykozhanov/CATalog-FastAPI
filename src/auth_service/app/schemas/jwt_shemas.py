from datetime import datetime

from pydantic import BaseModel

from src.auth_service.app.enums import JWTType


class JWTPayloadSchema(BaseModel):
    sub: str
    exp: datetime
    type: JWTType


__all__ = ["JWTPayloadSchema"]
