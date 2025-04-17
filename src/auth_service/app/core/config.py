import logging
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from src.auth_service.app.core.logging_config import configure_logging, LOG_DIR

configure_logging()
logger = logging.getLogger("app")


class Settings(BaseSettings):
    DEBUG: bool = False
    TESTING: bool = False

    DATABASE_TEST_URL: str = "sqlite+aiosqlite:///:memory:"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    SERVICE_USERNAME: str
    SERVICE_PASSWORD: str

    ACCESS_TOKEN_EXPIRE: int | None = 15  # В минутах
    REFRESH_TOKEN_EXPIRE: int | None = 60 * 24 * 30  # В минутах
    JWT_PRIVATE_KEY: str
    JWT_PUBLIC_KEY: str
    JWT_ALGORITHM: str = "RS256"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent / ".env",
        env_file_encoding="utf-8",
    )

    def get_database_url(self, host: str | None = None) -> str:
        if self.TESTING:
            return self.DATABASE_TEST_URL
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{host or self.POSTGRES_HOST}:{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )


settings = Settings()

if not settings.TESTING:
    LOG_DIR.mkdir(exist_ok=True)

__all__ = [settings]
