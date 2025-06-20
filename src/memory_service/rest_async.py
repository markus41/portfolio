"""Asynchronous REST backend for memory service operations."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
import types

try:  # optional dependency
    import httpx  # type: ignore
except Exception:  # pragma: no cover - test environment fallback
    async def _ok(*args, **kwargs):
        return types.SimpleNamespace(status_code=200, json=lambda: [])

    httpx = types.SimpleNamespace(
        AsyncClient=lambda *a, **k: types.SimpleNamespace(
            post=_ok, get=_ok, aclose=lambda: None
        ),
        Response=types.SimpleNamespace,
        Request=types.SimpleNamespace,
        MockTransport=None,
    )

from .base import BaseMemoryService
from ..utils.logger import get_logger

logger = get_logger(__name__)


class AsyncRestMemoryService(BaseMemoryService):
    """Persist events by calling a REST API asynchronously via ``httpx``."""

    def __init__(self, endpoint: str, *, client: Optional[httpx.AsyncClient] = None) -> None:
        self.endpoint = endpoint.rstrip("/")
        self._client = client or httpx.AsyncClient(base_url=self.endpoint)

    async def store(self, key: str, payload: Dict[str, Any]) -> bool:
        logger.info(f"Storing memory for key={key}")
        try:
            resp = await self._client.post("/store", json={"key": key, "data": payload})
        except Exception as exc:  # pragma: no cover - network failure
            logger.error(f"Async REST store failed for key={key}: {exc}")
            return False
        return resp.status_code < 400

    async def fetch(self, key: str, top_k: int = 5) -> List[Dict[str, Any]]:
        logger.info(f"Fetching top {top_k} memories for key={key}")
        try:
            resp = await self._client.get("/fetch", params={"key": key, "top_k": top_k})
        except Exception as exc:  # pragma: no cover - network failure
            logger.error(f"Async REST fetch failed for key={key}: {exc}")
            return []
        if resp.status_code >= 400:
            return []
        return resp.json()

    async def aclose(self) -> None:
        """Close the underlying ``httpx`` client."""
        await self._client.aclose()
