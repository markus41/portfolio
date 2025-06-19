"""Redis based memory service implementation."""

from __future__ import annotations

import json
import types
from typing import Any, Dict, List

from .base import BaseMemoryService
from ..utils.logger import get_logger

try:  # optional dependency
    import redis  # type: ignore
except Exception:  # pragma: no cover - fallback when redis is missing
    redis = types.SimpleNamespace(
        Redis=types.SimpleNamespace(
            from_url=lambda *a, **k: types.SimpleNamespace(
                rpush=lambda *a, **k: None,
                lrange=lambda *a, **k: [],
                ping=lambda *a, **k: True,
            )
        )
    )

logger = get_logger(__name__)


class RedisMemoryService(BaseMemoryService):
    """Persist events in a Redis list per key."""

    def __init__(self, url: str) -> None:
        self.client = redis.Redis.from_url(url, decode_responses=True)
        try:  # pragma: no cover - network failure not relevant for unit tests
            self.client.ping()
        except Exception as exc:  # pragma: no cover - log only
            logger.warning(f"Redis ping failed: {exc}")

    def store(self, key: str, payload: Dict[str, Any]) -> bool:
        try:
            self.client.rpush(key, json.dumps(payload))
            logger.info(f"Stored event for key={key} in Redis")
            return True
        except Exception as exc:  # pragma: no cover - runtime errors
            logger.error(f"Redis store failed for key={key}: {exc}")
            return False

    def fetch(self, key: str, top_k: int = 5) -> List[Dict[str, Any]]:
        try:
            raw = self.client.lrange(key, -top_k, -1)
        except Exception as exc:  # pragma: no cover - runtime errors
            logger.error(f"Redis fetch failed for key={key}: {exc}")
            return []

        results: List[Dict[str, Any]] = []
        for item in raw:
            if isinstance(item, bytes):
                item = item.decode("utf-8")
            try:
                results.append(json.loads(item))
            except Exception:  # pragma: no cover - ignore malformed entries
                continue
        return results

