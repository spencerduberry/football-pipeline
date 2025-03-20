import functools
import logging
import logging.config
import os
from collections.abc import Callable


def log_func(func: Callable) -> Callable:
    """Decorator function that prints input/output of logger functions.

    Args:
        func: The function that the input/output will be logged for.

    Returns:
        Callable: Wrapper of the original function with the args and kwargs, then the function's result.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(
            {
                "func": func.__name__,
                "args": args,
                "kwargs": kwargs,
            }
        )

        res = func(*args, **kwargs)

        logger.info(
            {
                "func": func.__name__,
                "res": res,
            }
        )
        return res

    return wrapper


os.makedirs("data/logs", exist_ok=True)
LOGGING_CONFIG = {  # constant, meaning it should not be changed after definition
    "version": 1,  # future-proofing in case of modifications to the logger class
    "disable_existing_loggers": False,  # (root logger is bieng used)
    "formatters": {
        "default_formatter": {
            "format": "%(asctime)s :: %(levelname)-8s :: [%(filename)s:%(lineno)-3s - %(funcName)-32s] :: %(message)s"
        }
    },
    "handlers": {
        "raw_log": {
            "class": "logging.handlers.TimedRotatingFileHandler",  # deletes logs after a specified time frame
            "level": "DEBUG",
            "formatter": "default_formatter",
            "filename": "001_raw_layer.log",
            "when": "midnight",  # rotate at midnight
            "interval": 1,  # once per day
            "backupCount": 7,  # keep a week's worth of logs
            "encoding": "utf-8",
        }
    },
    "filename": "data/logs/001_raw_layer.log",
    "root": {"level": "DEBUG", "handlers": ["raw_log"]},
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger()
