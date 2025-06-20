"""Memory service backends providing persistent storage for events."""

from .base import BaseMemoryService
from .rest import RestMemoryService
try:  # optional dependency
    from .rest_async import AsyncRestMemoryService
except Exception:  # pragma: no cover - httpx missing
    AsyncRestMemoryService = None  # type: ignore
from .file import FileMemoryService
from .redis import RedisMemoryService

__all__ = [
    "BaseMemoryService",
    "RestMemoryService",
    "AsyncRestMemoryService",
    "FileMemoryService",
    "RedisMemoryService",
]
