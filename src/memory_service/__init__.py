"""Memory service backends providing persistent storage for events."""

from .base import BaseMemoryService
from .async_base import AsyncBaseMemoryService
from .rest import RestMemoryService

try:  # optional dependency
    from .rest_async import AsyncRestMemoryService
except Exception:  # pragma: no cover - httpx missing
    AsyncRestMemoryService = None  # type: ignore
from .file import FileMemoryService
from .redis import RedisMemoryService
from .embedding import EmbeddingMemoryService

__all__ = [
    "BaseMemoryService",
    "AsyncBaseMemoryService",
    "RestMemoryService",
    "AsyncRestMemoryService",
    "FileMemoryService",
    "RedisMemoryService",
    "EmbeddingMemoryService",
]
