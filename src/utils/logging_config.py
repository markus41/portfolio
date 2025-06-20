import json
import logging
import os
import sys
from datetime import datetime
from typing import IO, Any


class JsonFormatter(logging.Formatter):
    """Format log records as JSON strings."""

    def format(self, record: logging.LogRecord) -> str:
        log_record: dict[str, Any] = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


def setup_logging(level: str | int | None = None, stream: IO[str] = sys.stdout) -> None:
    """Configure root logging to emit JSON formatted records.

    Parameters
    ----------
    level:
        Initial log level for the root logger. When omitted the ``LOG_LEVEL``
        environment variable is consulted and defaults to ``INFO``.
    stream:
        File-like object log output is written to. ``sys.stdout`` by default.

    This function is idempotent and safe to call multiple times.
    """
    root = logging.getLogger()
    if root.handlers:
        return

    if level is None:
        level = os.getenv("LOG_LEVEL", "INFO")
    root.setLevel(level)

    handler = logging.StreamHandler(stream)
    handler.setFormatter(JsonFormatter())
    root.addHandler(handler)
