"""
Dedupe some logging code
"""

from typing import Any


def configure_logging() -> dict[str, Any]:
    """Logging config in dict form, rather than yaml.

    Returns:
        dict[str, Any]: The logging configuration
    """
    logging_config: dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "standard": {"format": "[%(levelname)s] %(name)s: %(message)s"},
        },
        "handlers": {
            "default": {
                "level": "DEBUG",
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

    debug_level_modules: list[str] = [
        "__main__",
        "dedlin",
        "dedlin.document",
    ]

    info_level_modules: list[str] = []
    warn_level_modules: list[str] = [
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
