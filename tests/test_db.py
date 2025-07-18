from src import db
from src.config import settings
import sqlite3


def test_db_write_and_read(tmp_path):
    settings.DB_CONNECTION_STRING = f"sqlite:///{tmp_path}/t.db"
    db.init_db()
    db.insert_event("demo", "x", {"a": 1}, {"r": 2})
    db.insert_event("other", "y", {"b": 2}, {"s": 3})

    rows = db.fetch_history(limit=10)
    assert len(rows) == 2

    rows = db.fetch_history(team="demo")
    assert len(rows) == 1
    assert rows[0]["event_type"] == "x"

    rows = db.fetch_history(event_type="y")
    assert len(rows) == 1
    assert rows[0]["team"] == "other"


def test_db_index_creation(tmp_path):
    """Ensure indexes for efficient lookups exist after initialisation."""
    settings.DB_CONNECTION_STRING = f"sqlite:///{tmp_path}/t.db"
    db.init_db()

    with sqlite3.connect(tmp_path / "t.db") as conn:
        indexes = [row[1] for row in conn.execute("PRAGMA index_list('event_history')")]

    assert "idx_event_history_timestamp" in indexes
    assert "idx_event_history_team" in indexes
