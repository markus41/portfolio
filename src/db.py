from __future__ import annotations

"""Simple SQLite-based persistence layer.

This module provides helper functions to record events handled by the
:class:`SolutionOrchestrator` and to fetch these records for display in the
dashboard. It intentionally avoids third-party dependencies so the
application can run in restricted environments without internet access.
"""

from datetime import datetime
from pathlib import Path
import json
import sqlite3

from .config import settings


# ---------------------------------------------------------------------------
# Database initialisation
# ---------------------------------------------------------------------------


def _get_db_path() -> Path:
    """Return the path to the SQLite database file based on settings."""
    url = settings.DB_CONNECTION_STRING
    if url and url.startswith("sqlite:///"):
        return Path(url.replace("sqlite:///", ""))
    return Path("data.db")


def init_db() -> None:
    """Create database tables if they do not yet exist."""
    path = _get_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS event_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team TEXT NOT NULL,
                event_type TEXT NOT NULL,
                payload TEXT NOT NULL,
                result TEXT,
                timestamp TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                timestamp TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT,
                response TEXT,
                timestamp TEXT
            )
            """
        )


# ---------------------------------------------------------------------------
# Data access helpers
# ---------------------------------------------------------------------------


def insert_event(team: str, event_type: str, payload: dict, result: dict) -> None:
    """Insert a single event entry into the history table."""
    path = _get_db_path()
    ts = datetime.utcnow().isoformat()
    with sqlite3.connect(path) as conn:
        conn.execute(
            "INSERT INTO event_history (team, event_type, payload, result, timestamp)\n"
            "VALUES (?, ?, ?, ?, ?)",
            (team, event_type, json.dumps(payload), json.dumps(result), ts),
        )
        conn.commit()


def fetch_history(
    limit: int = 10,
    offset: int = 0,
    *,
    team: str | None = None,
    event_type: str | None = None,
) -> list[dict]:
    """Return history records ordered by timestamp descending.

    Parameters
    ----------
    limit:
        Maximum number of records to return.
    offset:
        Number of records to skip from the start of the result set.
    team:
        Optional team name to filter by.
    event_type:
        Optional event type to filter by.
    """

    path = _get_db_path()
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row

        query = (
            "SELECT id, team, event_type, payload, result, timestamp\n"
            "FROM event_history"
        )

        filters: list[str] = []
        params: list = []
        if team is not None:
            filters.append("team = ?")
            params.append(team)
        if event_type is not None:
            filters.append("event_type = ?")
            params.append(event_type)
        if filters:
            query += " WHERE " + " AND ".join(filters)

        query += " ORDER BY datetime(timestamp) DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        cur = conn.execute(query, params)
        rows = cur.fetchall()
    history: list[dict] = []
    for row in rows:
        history.append(
            {
                "id": row["id"],
                "team": row["team"],
                "event_type": row["event_type"],
                "payload": json.loads(row["payload"]),
                "result": json.loads(row["result"]) if row["result"] else None,
                "timestamp": row["timestamp"],
            }
        )
    return history
