"""Simple JSONL based memory service for local development."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from .base import BaseMemoryService
import logging

logger = logging.getLogger(__name__)


class FileMemoryService(BaseMemoryService):
    """Append events to a local JSONL file and read them back."""

    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.file_path.touch(exist_ok=True)

    def store(self, key: str, payload: Dict[str, Any]) -> bool:
        record = {"key": key, "data": payload}
        with self.file_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")
        logger.info(f"Stored event for key={key} in {self.file_path}")
        return True

    def fetch(self, key: str, top_k: int = 5) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        if not self.file_path.exists():
            return results
        with self.file_path.open("r", encoding="utf-8") as fh:
            for line in fh:
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("key") == key:
                    results.append(rec.get("data", {}))
        return results[-top_k:]
