"""REST based memory service used for demos and tests."""

from __future__ import annotations

from typing import Any, Dict, List
import types

from .base import BaseMemoryService
import logging

try:  # optional dependency
    import requests  # type: ignore
except Exception:  # pragma: no cover - test environment fallback
    requests = types.SimpleNamespace(
        post=lambda *a, **k: types.SimpleNamespace(ok=True, json=lambda: {}),
        get=lambda *a, **k: types.SimpleNamespace(ok=True, json=lambda: {}),
    )

logger = logging.getLogger(__name__)


class RestMemoryService(BaseMemoryService):
    """Thin wrapper around a REST API for persisting events."""

    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint

    def store(self, key: str, payload: Dict[str, Any]) -> bool:
        logger.info(f"Storing memory for key={key}")
        response = requests.post(
            f"{self.endpoint}/store", json={"key": key, "data": payload}
        )
        return response.ok

    def fetch(self, key: str, top_k: int = 5) -> List[Dict[str, Any]]:
        logger.info(f"Fetching top {top_k} memories for key={key}")
        response = requests.get(
            f"{self.endpoint}/fetch", params={"key": key, "top_k": top_k}
        )
        return response.json() if response.ok else []
