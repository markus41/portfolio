import json
import logging
from io import StringIO

from src.utils.logging_config import setup_logging


def test_json_log_formatting():
    root = logging.getLogger()
    for h in root.handlers[:]:
        root.removeHandler(h)
    stream = StringIO()
    setup_logging(stream=stream)
    logger = logging.getLogger("test")
    logger.info("hello %s", "world")
    data = json.loads(stream.getvalue().strip())
    assert data["message"] == "hello world"
    assert data["level"] == "INFO"
    assert data["name"] == "test"
    assert "timestamp" in data


def test_setup_logging_idempotent():
    root = logging.getLogger()
    for h in root.handlers[:]:
        root.removeHandler(h)
    stream1 = StringIO()
    setup_logging(stream=stream1)
    # second call should not add a second handler
    stream2 = StringIO()
    setup_logging(stream=stream2)

    logger = logging.getLogger("idempotent")
    logger.info("once")

    # only first stream should have data
    assert stream1.getvalue()
    assert not stream2.getvalue()
