"""Utility helpers for obtaining a preconfigured :class:`logging.Logger`."""

import logging
import sys


def get_logger(name: str) -> logging.Logger:
    """Return a console logger with a simple formatter.

    The helper ensures that loggers are only configured once which prevents
    duplicate log lines when modules are reloaded during testing.
    """

    logger = logging.getLogger(name)
    if not logger.handlers:
        # Stream all logs to stdout so test runners can capture them
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
