from fastapi import FastAPI

from src.auth_service.app.routers import auth_router, user_router


def add_routers(app: FastAPI) -> None:
    app.include_router(auth_router, prefix="/api/auth", tags=["Аутентификация"])
    app.include_router(user_router, prefix="/api/user", tags=["Пользователи"])
