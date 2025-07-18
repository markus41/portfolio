"""In-memory similarity search backend using simple vector embeddings."""

from __future__ import annotations

import math
from collections import Counter
from typing import Any, Dict, List, Tuple

from .base import BaseMemoryService


class EmbeddingMemoryService(BaseMemoryService):
    """Store payloads and rank results using cosine similarity."""

    def __init__(self, text_key: str = "text") -> None:
        self.text_key = text_key
        self._store: List[Tuple[Dict[str, int], Dict[str, Any]]] = []

    def _embed(self, text: str) -> Dict[str, int]:
        tokens = text.lower().split()
        return Counter(tokens)

    def _cosine(self, v1: Dict[str, int], v2: Dict[str, int]) -> float:
        dot = sum(v1[t] * v2[t] for t in v1.keys() & v2.keys())
        norm1 = math.sqrt(sum(v * v for v in v1.values()))
        norm2 = math.sqrt(sum(v * v for v in v2.values()))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    def store(self, key: str, payload: Dict[str, Any]) -> bool:
        text = str(payload.get(self.text_key, ""))
        vector = self._embed(text)
        self._store.append((vector, payload))
        return True

    def fetch(self, key: str, top_k: int = 5) -> List[Dict[str, Any]]:
        query_vec = self._embed(key)
        ranked = sorted(
            self._store,
            key=lambda item: self._cosine(query_vec, item[0]),
            reverse=True,
        )
        return [payload for _, payload in ranked[:top_k]]

__all__ = ["EmbeddingMemoryService"]
