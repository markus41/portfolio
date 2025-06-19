"""Abstract interface for memory service implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseMemoryService(ABC):
    """Define the storage API used by orchestrators and agents."""

    @abstractmethod
    def store(self, key: str, payload: Dict[str, Any]) -> bool:
        """Persist ``payload`` under ``key``."""

    @abstractmethod
    def fetch(self, key: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Return up to ``top_k`` records associated with ``key``."""
