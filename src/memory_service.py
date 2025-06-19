"""Simple REST based memory service used by the orchestrator.

In a production system this component would likely talk to a vector database or
some other specialised storage.  For the purposes of the examples and tests we
fake this by sending HTTP requests to a configurable endpoint.
"""

from typing import List, Dict, Any
import types

try:  # optional dependency
    import requests  # type: ignore
except Exception:  # pragma: no cover - test environment fallback
    requests = types.SimpleNamespace(
        post=lambda *a, **k: types.SimpleNamespace(ok=True, json=lambda: {}),
        get=lambda *a, **k: types.SimpleNamespace(ok=True, json=lambda: {}),
    )
from .utils.logger import get_logger

logger = get_logger(__name__)


class MemoryService:
    """Thin wrapper around a REST API used for storing and retrieving events."""

    def __init__(self, endpoint: str):
        # base URL of the REST service (e.g. http://localhost:8000)
        self.endpoint = endpoint

    def store(self, key: str, payload: Dict[str, Any]) -> bool:
        """Persist a payload under ``key``.

        Parameters
        ----------
        key:
            Identifier for the memory entry.
        payload:
            Arbitrary JSON serialisable dictionary to store.
        """

        logger.info(f"Storing memory for key={key}")
        # In a real implementation this would be a vector DB or search-engine
        # call.  Here we just POST to a simple REST endpoint.
        response = requests.post(
            f"{self.endpoint}/store", json={"key": key, "data": payload}
        )
        return response.ok

    def fetch(self, key: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve the ``top_k`` most relevant memories for ``key``."""
        logger.info(f"Fetching top {top_k} memories for key={key}")
        response = requests.get(
            f"{self.endpoint}/fetch", params={"key": key, "top_k": top_k}
        )
        # graceful fallback on network errors or empty responses
        return response.json() if response.ok else []
