from datetime import datetime, UTC

from sqlalchemy import String, TIMESTAMP, Index
from sqlalchemy.orm import Mapped, mapped_column

from src.auth_service.app.core.database import Base
from src.auth_service.app.enums import UserRoleEnum


class User(Base):
    """Модель пользователя"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    hashed_password: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(100))
    role: Mapped[UserRoleEnum] = mapped_column(default=UserRoleEnum.USER)

    is_active: Mapped[bool] = mapped_column(default=True)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )

    __table_args__ = (
        Index(
            "ix_active_users_username",
            "username",
            postgresql_where=(is_deleted == False),
        ),
    )

    def soft_delete(self) -> None:
        """Метод для мягкого удаления пользователя"""
        self.is_deleted = True
        self.deleted_at = datetime.now(UTC)
