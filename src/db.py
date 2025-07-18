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
import secrets

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
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS api_keys (
                key TEXT PRIMARY KEY,
                tenant TEXT NOT NULL,
                scopes TEXT NOT NULL,
                created_at TEXT NOT NULL
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


# ---------------------------------------------------------------------------
# API key management helpers
# ---------------------------------------------------------------------------

def has_api_keys() -> bool:
    """Return ``True`` if at least one API key exists in the database."""

    path = _get_db_path()
    with sqlite3.connect(path) as conn:
        cur = conn.execute("SELECT COUNT(*) FROM api_keys")
        count = cur.fetchone()[0]
    return count > 0


def create_api_key(tenant: str, scopes: list[str]) -> str:
    """Create and store a new API key for ``tenant`` with ``scopes``.

    Returns the generated key string which should be presented to the client.
    """

    key = secrets.token_urlsafe(32)
    ts = datetime.utcnow().isoformat()
    path = _get_db_path()
    with sqlite3.connect(path) as conn:
        conn.execute(
            "INSERT INTO api_keys (key, tenant, scopes, created_at) VALUES (?, ?, ?, ?)",
            (key, tenant, ",".join(scopes), ts),
        )
        conn.commit()
    return key


def rotate_api_key(old_key: str) -> str:
    """Replace ``old_key`` with a new random key and return the new value."""

    path = _get_db_path()
    with sqlite3.connect(path) as conn:
        row = conn.execute(
            "SELECT tenant, scopes FROM api_keys WHERE key = ?",
            (old_key,),
        ).fetchone()
        if row is None:
            raise KeyError("unknown api key")
        new_key = secrets.token_urlsafe(32)
        ts = datetime.utcnow().isoformat()
        conn.execute(
            "UPDATE api_keys SET key = ?, created_at = ? WHERE key = ?",
            (new_key, ts, old_key),
        )
        conn.commit()
    return new_key


def validate_api_key(key: str, scope: str) -> bool:
    """Return ``True`` if ``key`` exists and grants ``scope`` access."""

    path = _get_db_path()
    with sqlite3.connect(path) as conn:
        row = conn.execute(
            "SELECT scopes FROM api_keys WHERE key = ?",
            (key,),
        ).fetchone()
        if row is None:
            return False
        scopes = row[0].split(",") if row[0] else []
    return scope in scopes or "*" in scopes

