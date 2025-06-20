import logging
import re

from src.utils.logger import get_logger


def test_get_logger_emits_to_stdout_with_single_handler(capsys):
    """Ensure ``get_logger`` configures a single handler and logs are formatted."""
    root = logging.getLogger()
    for handler in root.handlers[:]:
        root.removeHandler(handler)

    logger = logging.getLogger("demo")
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    first = get_logger("demo")
    second = get_logger("demo")

    # Both calls should return the same logger with only one handler configured
    assert first is second
    assert len(first.handlers) == 1

    first.info("hello")
    captured = capsys.readouterr().out.strip()

    # Log should be emitted once to stdout with the expected format
    assert captured
    lines = captured.splitlines()
    assert len(lines) == 1
    log_line = lines[0]
    pattern = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}\] \[INFO\] demo: hello$"
    assert re.match(pattern, log_line), f"Unexpected log format: {log_line}"
