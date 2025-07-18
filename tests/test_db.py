from src import db
from src.config import settings


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

    key = db.create_api_key("tenant", ["read"])
    assert db.has_api_keys() is True
    assert db.validate_api_key(key, "read")
    new_key = db.rotate_api_key(key)
    assert not db.validate_api_key(key, "read")
    assert db.validate_api_key(new_key, "read")
