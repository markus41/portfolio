"""Pluggable event bus implementations."""

from __future__ import annotations

import os
from typing import Any

from .base import BaseEventBus
from .in_memory import InMemoryEventBus, AsyncInMemoryEventBus
from .redis import RedisEventBus, AsyncRedisEventBus
from ..config import settings

__all__ = [
    "BaseEventBus",
    "InMemoryEventBus",
    "AsyncInMemoryEventBus",
    "RedisEventBus",
    "AsyncRedisEventBus",
    "create_event_bus",
]


def create_event_bus(async_mode: bool = True) -> BaseEventBus:
    """Factory returning an event bus based on configuration."""

    backend = os.getenv("EVENT_BUS_BACKEND", settings.EVENT_BUS_BACKEND)
    if backend == "redis":
        url = settings.REDIS_URL or "redis://localhost:6379/0"
        return AsyncRedisEventBus(url) if async_mode else RedisEventBus(url)

    return AsyncInMemoryEventBus() if async_mode else InMemoryEventBus()

