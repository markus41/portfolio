"""Asynchronous memory service interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class AsyncBaseMemoryService(ABC):
    """Define an asynchronous storage API used by orchestrators and agents."""

    @abstractmethod
    async def store(self, key: str, payload: Dict[str, Any]) -> bool:
        """Persist ``payload`` under ``key`` asynchronously."""

    @abstractmethod
    async def fetch(self, key: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Return up to ``top_k`` records associated with ``key`` asynchronously."""

    async def aclose(self) -> None:  # pragma: no cover - optional hook
        """Release any underlying resources."""
        return None


__all__ = ["AsyncBaseMemoryService"]
