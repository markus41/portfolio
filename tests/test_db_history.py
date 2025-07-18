import time
from datetime import datetime
import json
import sqlite3

from src import db
from src.config import settings


def _insert_raw(path, team, event_type, ts):
    with sqlite3.connect(path) as conn:
        conn.execute(
            "INSERT INTO event_history (team, event_type, payload, result, timestamp) VALUES (?, ?, ?, ?, ?)",
            (team, event_type, json.dumps({}), json.dumps({}), ts),
        )
        conn.commit()


def test_history_order_and_pagination(tmp_path):
    settings.DB_CONNECTION_STRING = f"sqlite:///{tmp_path}/t.db"
    db.init_db()
    path = tmp_path / "t.db"

    t1 = datetime.utcnow().isoformat()
    time.sleep(0.01)
    t2 = datetime.utcnow().isoformat()
    time.sleep(0.01)
    t3 = datetime.utcnow().isoformat()

    _insert_raw(path, "demo", "A", t1)
    _insert_raw(path, "demo", "B", t2)
    _insert_raw(path, "other", "C", t3)

    rows = db.fetch_history(limit=10)
    assert len(rows) == 3
    assert rows[0]["timestamp"] > rows[1]["timestamp"] >= rows[2]["timestamp"]

    paged = db.fetch_history(limit=1, offset=1)
    assert len(paged) == 1
    assert paged[0]["timestamp"] == rows[1]["timestamp"]


def test_history_filters(tmp_path):
    settings.DB_CONNECTION_STRING = f"sqlite:///{tmp_path}/t.db"
    db.init_db()
    path = tmp_path / "t.db"
    _insert_raw(path, "sales", "alpha", datetime.utcnow().isoformat())
    _insert_raw(path, "marketing", "beta", datetime.utcnow().isoformat())
    _insert_raw(path, "sales", "beta", datetime.utcnow().isoformat())

    by_team = db.fetch_history(team="sales")
    assert {r["team"] for r in by_team} == {"sales"}

    by_event = db.fetch_history(event_type="beta")
    assert {r["event_type"] for r in by_event} == {"beta"}

    combo = db.fetch_history(team="sales", event_type="beta")
    assert len(combo) == 1
    assert combo[0]["team"] == "sales" and combo[0]["event_type"] == "beta"
