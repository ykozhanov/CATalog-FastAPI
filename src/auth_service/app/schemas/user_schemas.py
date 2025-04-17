from pydantic import BaseModel, Field, EmailStr, ConfigDict
from src.auth_service.app.enums import UserRoleEnum


class UserCreateInSchema(BaseModel):
    username: str = Field(..., max_length=50)
    password: str = Field(..., max_length=50)
    email: EmailStr = Field(..., max_length=100)


class UserCreateSchema(BaseModel):
    username: str = Field(..., max_length=50)
    hashed_password: str = Field(..., max_length=128)
    email: EmailStr = Field(..., max_length=100)


class UserUpdateSchema(BaseModel):
    id: int
    username: str | None = Field(None, max_length=50)
    email: EmailStr | None = Field(None, max_length=100)
    role: UserRoleEnum | None = None


class UserReadSchema(UserCreateSchema):
    id: int
    is_active: bool
    role: UserRoleEnum

    model_config = ConfigDict(
        from_attributes=True,
    )


__all__ = [
    "UserCreateInSchema",
    "UserCreateSchema",
    "UserUpdateSchema",
    "UserReadSchema",
]
