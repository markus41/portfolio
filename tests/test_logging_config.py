import json
import logging
import re
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


def test_plain_text_formatting():
    root = logging.getLogger()
    for h in root.handlers[:]:
        root.removeHandler(h)
    stream = StringIO()
    setup_logging(stream=stream, plain_text=True)
    logger = logging.getLogger("plain")
    logger.warning("simple")
    line = stream.getvalue().strip()
    pattern = (
        r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}\] \[WARNING\] plain: simple$"
    )
    assert re.match(pattern, line), f"Unexpected log format: {line}"


def test_file_output_json(tmp_path):
    root = logging.getLogger()
    for h in root.handlers[:]:
        root.removeHandler(h)
    log_file = tmp_path / "out.log"
    setup_logging(file_path=str(log_file))
    logger = logging.getLogger("filetest")
    logger.error("boom")
    data = json.loads(log_file.read_text().strip())
    assert data["message"] == "boom"
    assert data["level"] == "ERROR"
    assert data["name"] == "filetest"


def test_env_vars(monkeypatch, tmp_path):
    root = logging.getLogger()
    for h in root.handlers[:]:
        root.removeHandler(h)
    log_file = tmp_path / "env.log"
    monkeypatch.setenv("LOG_FILE", str(log_file))
    monkeypatch.setenv("LOG_PLAIN", "true")
    setup_logging()
    logger = logging.getLogger("env")
    logger.info("hi")
    content = log_file.read_text().strip()
    assert "env: hi" in content
    assert not content.startswith("{")
