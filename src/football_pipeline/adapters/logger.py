import logging
import logging.config
import os
from typing import Protocol, runtime_checkable

import attrs

LOGGING_CONFIG = {  # constant, meaning it should not be changed after definition
    "version": 1,  # future-proofing in case of modifications to the logger class
    "disable_existing_loggers": False,  # (root logger is being used)
    "formatters": {
        "default_formatter": {"format": "%(asctime)s :: %(levelname)-8s :: %(message)s"}
    },
    "handlers": {
        "raw_log": {
            "class": "logging.handlers.TimedRotatingFileHandler",  # deletes logs after a specified time frame
            "level": "DEBUG",
            "formatter": "default_formatter",
            "filename": "./data/logs/001_raw_layer.log",
            "when": "midnight",  # rotate at midnight
            "interval": 1,  # once per day
            "backupCount": 7,  # keep a week's worth of logs
            "encoding": "utf-8",
        }
    },
    "root": {"level": "DEBUG", "handlers": ["raw_log"]},
}


@runtime_checkable
class LoggerProtocol(Protocol):
    def setup(self) -> bool: ...
    def debug(self, message: dict) -> None: ...
    def info(self, message: dict) -> None: ...
    def error(self, message: dict) -> None: ...


@attrs.define
class FakeLogger:
    file: str = attrs.field()
    log: list = attrs.field(default=attrs.Factory(list))
    configured: bool = attrs.field(default=False)

    def setup(self) -> bool:
        self.configured = True
        return True

    def debug(self, message: dict) -> None:
        self.log.append({"level": "debug", **message})

    def info(self, message: dict) -> None:
        self.log.append({"level": "info", **message})

    def error(self, message: dict) -> None:
        self.log.append({"level": "error", **message})


@attrs.define
class RealLogger:
    file: str = attrs.field()
    log: logging.Logger = attrs.field(init=False)

    def setup(self) -> bool:
        os.makedirs("./data/logs", exist_ok=True)
        logging.config.dictConfig(LOGGING_CONFIG)
        self.log = logging.getLogger(self.file)
        return True

    def debug(self, message: dict) -> None:
        self.log.debug(message)

    def info(self, message: dict) -> None:
        self.log.info(message)

    def error(self, message: dict) -> None:
        self.log.error(message)
