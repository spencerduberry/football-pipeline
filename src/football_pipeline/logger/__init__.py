import logging
import logging.config

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
    "root": {"level": "DEBUG", "handlers": ["raw_log"]},
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger()
