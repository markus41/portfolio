from __future__ import annotations

"""JSONL based activity logging utility."""

from collections import deque
from datetime import datetime, timezone
import json
from pathlib import Path
from threading import Lock
from typing import Any, Dict, List


class ActivityLogger:
    """Append structured records to a JSONL log file."""

    def __init__(self, log_path: str | Path) -> None:
        self.path = Path(log_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()

    def log(
        self,
        agent_id: str,
        summary: str,
        *,
        ts: datetime | None = None,
        event_id: str | None = None,
    ) -> None:
        """Write a single log entry.

        Parameters
        ----------
        agent_id:
            Identifier of the handling agent.
        summary:
            Short text describing the outcome.
        ts:
            Optional timestamp.  When omitted the current UTC time is used.
        event_id:
            Optional event identifier allowing logs to be correlated with
            metrics and SSE streams.
        """

        entry = {
            "timestamp": (ts or datetime.now(timezone.utc)).isoformat(),
            "agent_id": agent_id,
            "summary": summary,
        }
        if event_id is not None:
            entry["event_id"] = event_id
        line = json.dumps(entry)
        with self._lock:
            with self.path.open("a", encoding="utf-8") as fh:
                fh.write(line + "\n")

    def tail(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Return the most recent ``limit`` entries."""
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as fh:
            lines = list(deque(fh, maxlen=limit))
        return [json.loads(line) for line in lines]
