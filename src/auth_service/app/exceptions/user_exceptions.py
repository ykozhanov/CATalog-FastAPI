from .domain_exceptions import ConflictException, NotFoundException


class UserConflictExceptions(ConflictException):
    message = "Конфликт при работе с пользователем"


class UserNotFoundException(NotFoundException):
    message = "Пользователь не найден"


__all__ = ["UserConflictExceptions", "UserNotFoundException"]
