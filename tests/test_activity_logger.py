from pathlib import Path
from src.utils.activity_logger import ActivityLogger


def test_activity_logger(tmp_path: Path):
    log_file = tmp_path / "log.jsonl"
    logger = ActivityLogger(log_file)

    logger.log("agent", "did something", event_id="ev1")
    logger.log("agent", "second")

    entries = logger.tail(2)
    assert len(entries) == 2
    assert entries[0]["agent_id"] == "agent"
    assert entries[0]["summary"] == "did something"
    assert entries[0]["event_id"] == "ev1"
    assert "timestamp" in entries[0]
