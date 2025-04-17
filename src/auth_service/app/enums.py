from enum import Enum


class UserRoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"


class JWTType(str, Enum):
    REFRESH = "refresh"
    ACCESS = "access"


__all__ = ["UserRoleEnum", "JWTType"]