class DomainException(Exception):
    message: str = "Ошибка бизнес-логики"
    code: str = "domain_error"
    status_code: int = 500

    def __init__(self, message: str | None = None, **kwargs):
        self.message = message or self.message
        self.details = kwargs


class BadRequestException(DomainException):
    code = "bad_request"
    status_code = 400
    message = "Некорректный запрос"


class UnauthorizedException(DomainException):
    code = "unauthorized"
    status_code = 401
    message = "Ошибка авторизации"


class ForbiddenException(DomainException):
    code = "forbidden"
    status_code = 403
    message = "Недостаточно прав"


class NotFoundException(DomainException):
    message: str = "Объект не найден"
    code: str = "not_found"
    status_code: int = 404


class ConflictException(DomainException):
    message: str = "Конфликт при выполнении действия"
    code: str = "conflict"
    status_code: int = 409


class ValidationException(DomainException):
    code = "validation_failed"
    message = "Невалидные данные"
    status_code = 422


__all__ = [
    "DomainException",
    "BadRequestException",
    "UnauthorizedException",
    "ForbiddenException",
    "NotFoundException",
    "ConflictException",
    "ValidationException",
]
