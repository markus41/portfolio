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

    def log(self, agent_id: str, summary: str, *, ts: datetime | None = None) -> None:
        """Write a single log entry with ``agent_id`` and ``summary``."""
        entry = {
            "timestamp": (ts or datetime.now(timezone.utc)).isoformat(),
            "agent_id": agent_id,
            "summary": summary,
        }
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
