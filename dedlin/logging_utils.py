"""
Dedupe some logging code
"""
from typing import Any


def configure_logging() -> dict[str, Any]:
    """Basic style"""
    logging_config: dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "standard": {"format": "[%(levelname)s] %(name)s: %(message)s"},
        },
        "handlers": {
            "default": {
                "level": "INFO",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",  # Default is stderr
            },
        },
        "loggers": {
            # root logger can capture too much
            "": {  # root logger
                "handlers": ["default"],
                "level": "WARNING",
                "propagate": False,
            },
        },
    }

    debug_level_modules = [
        "__main__",
        "dedlin",
        "dedlin.document",
    ]

    info_level_modules = [
    ]
    warn_level_modules = [
        "psycopg2",
    ]

    for name in debug_level_modules:
        logging_config["loggers"][name] = {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": False,
        }

    for name in info_level_modules:
        logging_config["loggers"][name] = {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        }

    for name in warn_level_modules:
        logging_config["loggers"][name] = {
            "handlers": ["default"],
            "level": "WARNING",
            "propagate": False,
        }
    return logging_config
