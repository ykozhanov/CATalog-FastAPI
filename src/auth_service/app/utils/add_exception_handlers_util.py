from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from src.auth_service.app.exceptions import DomainException
from src.auth_service.app.schemas import ExceptionResponseSchema, BaseResponseSchema
from src.auth_service.app.core.config import logger


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        """Кастомные исключения"""
        logger.exception(
            f"Исключение: {exc.code}\n"
            f"Статус код: {exc.status_code}\n"
            f"Сообщение: {exc.message}\n"
            f"Детали: {exc.details}\n",
            exc_info=True,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=dict(
                ExceptionResponseSchema(message=exc.message, details=exc.details)
            ),
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """Ошибки валидации Pydantic при запросе"""
        logger.exception(
            f"Исключение: RequestValidationError:\n"
            f"Статус код: 422\n"
            f"Детали: {exc.errors()}\n",
            exc_info=True,
        )
        return JSONResponse(
            status_code=422,
            content=ExceptionResponseSchema(
                message="Невалидные входные данные",
                details=exc.errors(),
            ).model_dump(),
        )

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        """Ошибки валидации Pydantic при работе с данными"""
        logger.exception(
            f"Исключение: ValidationError:\n"
            f"Статус код: 422\n"
            f"Детали: {exc.errors()}\n"
        )
        return JSONResponse(
            status_code=422,
            content=ExceptionResponseSchema(
                message="Некорректные данные",
                details=exc.errors(),
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def other_exception_handler(request: Request, exc: Exception):
        """Все остальные исключения"""
        logger.error(
            f"Исключение: Exception\n" f"Статус код: 500\n" f"Детали: {str(exc)}\n",
            exc_info=True,
        )
        return JSONResponse(
            status_code=500,
            content=dict(BaseResponseSchema(message="Внутренняя ошибка сервера")),
        )
