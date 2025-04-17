from pydantic import Field, EmailStr, ConfigDict

from pydantic import BaseModel

from src.auth_service.app.enums import UserRoleEnum


class UserResponseSchema(BaseModel):
    id: int
    username: str = Field(..., max_length=50)
    email: EmailStr = Field(..., max_length=100)
    role: UserRoleEnum
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )


class AuthResponseSchema(BaseModel):
    access_token: str
    refresh_token: str


class BaseResponseSchema(BaseModel):
    message: str


class ExceptionResponseSchema(BaseResponseSchema):
    details: dict | list


__all__ = ["UserResponseSchema", "AuthResponseSchema", "ExceptionResponseSchema", "BaseResponseSchema"]
