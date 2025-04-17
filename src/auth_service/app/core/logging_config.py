from datetime import datetime
from logging.config import DictConfigurator
from pathlib import Path

LOG_DIR = Path("logs")


def configure_logging():
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": """
                    asctime: %(asctime)s
                    level: %(levelname)s
                    name: %(name)s
                    message: %(message)s
                    pathname: %(pathname)s
                    funcName: %(funcName)s
                    lineno: %(lineno)d
                    traceback: %(exc_info)s
                """,
            },
        },
        "handlers": {
            "file": {
                "class": "logging.handlers.ConcurrentRotatingFileHandler",
                "filename": LOG_DIR
                / f"auth_service_{datetime.now().strftime('%Y-%m-%d')}.log",
                "maxBytes": 1024 * 1024 * 10,
                "backupCount": 5,
                "formatter": "json",
                "encoding": "utf-8",
                "delay": True,
            },
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "simple",
                "level": "DEBUG",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "app": {
                "handlers": ["file", "console"],
                "level": "INFO",
                "propagate": False,
            },
            "app.debug": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
        "root": {"handlers": ["console"], "level": "WARNING"},
    }

    DictConfigurator(log_config)
