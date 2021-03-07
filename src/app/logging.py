import sys
import os
import logging
from loguru import logger

from .config import LOG_LEVEL


def get_ancestors(logger_name):
    segments = logger_name.split(".")
    return [".".join(segments[0:n+1]) for n in range(len(segments))]


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage())


def configure_logging():
    logging.root.setLevel(LOG_LEVEL)
    logging.root.handlers = [InterceptHandler()]
