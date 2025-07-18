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


def setup_logging(
    level: str | int | None = None,
    stream: IO[str] = sys.stdout,
    file_path: str | None = None,
    plain_text: bool | None = None,
) -> None:
    """Configure root logging with optional file output and formatting mode.

    Parameters
    ----------
    level:
        Initial log level for the root logger. When omitted the ``LOG_LEVEL``
        environment variable is consulted and defaults to ``INFO``.
    stream:
        File-like object log output is written to when ``file_path`` is not
        supplied. ``sys.stdout`` by default.
    file_path:
        Location to write log records. When omitted the ``LOG_FILE`` environment
        variable is used. If provided, ``stream`` is ignored.
    plain_text:
        Emit logs in plain text format when ``True``. When omitted the
        ``LOG_PLAIN`` environment variable controls the mode.

    This function is idempotent and safe to call multiple times.
    """
    root = logging.getLogger()
    if root.handlers:
        return

    if level is None:
        level = os.getenv("LOG_LEVEL", "INFO")
    root.setLevel(level)

    if file_path is None:
        file_path = os.getenv("LOG_FILE")

    if plain_text is None:
        env_value = os.getenv("LOG_PLAIN", "false").lower()
        plain_text = env_value in {"1", "true", "yes"}

    if file_path:
        handler: logging.Handler = logging.FileHandler(file_path)
    else:
        handler = logging.StreamHandler(stream)

    if plain_text:
        formatter: logging.Formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
        )
    else:
        formatter = JsonFormatter()

    handler.setFormatter(formatter)
    root.addHandler(handler)
