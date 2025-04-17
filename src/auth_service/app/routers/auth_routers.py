from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth_service.app.dependencies import (
    get_user_service,
    get_jwt_service,
    oauth2_scheme,
)
from src.auth_service.app.schemas import UserCreateInSchema, AuthResponseSchema
from src.auth_service.app.interfaces import (
    AsyncUserServiceInterface,
    JWTServiceInterface,
)

router = APIRouter()


@router.post("/register", status_code=201)
async def auth_register(
    user_data: UserCreateInSchema,
    user_service: AsyncUserServiceInterface = Depends(get_user_service),
    jwt_service: JWTServiceInterface = Depends(get_jwt_service),
) -> AuthResponseSchema:
    """Регистрация нового пользователя"""
    new_user = await user_service.create(user_data)
    refresh_token = jwt_service.get_refresh_token(str(new_user.id))
    return AuthResponseSchema(
        refresh_token=refresh_token,
        access_token=jwt_service.get_access_token(refresh_token),
    )


@router.post("/login")
async def auth_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: AsyncUserServiceInterface = Depends(get_user_service),
    jwt_service: JWTServiceInterface = Depends(get_jwt_service),
):
    """Вход для существующего пользователя"""
    user = await user_service.get_by_username(form_data.username)
    refresh_token = jwt_service.get_refresh_token(str(user.id))
    return AuthResponseSchema(
        refresh_token=refresh_token,
        access_token=jwt_service.get_access_token(refresh_token),
    )


@router.post("/token")
async def auth_token(
    refresh_token: str = Depends(oauth2_scheme),
    jwt_service: JWTServiceInterface = Depends(get_jwt_service),
) -> AuthResponseSchema:
    """Получить пару (refresh и access) JWT токенов на основе Refresh JWT токена"""
    return AuthResponseSchema(
        refresh_token=refresh_token,
        access_token=jwt_service.get_access_token(refresh_token),
    )
