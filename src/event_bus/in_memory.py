from __future__ import annotations

"""In-memory event bus implementations."""

import asyncio
import inspect
from typing import Any, Callable, Dict, List

from .base import BaseEventBus


class InMemoryEventBus(BaseEventBus):
    """Very small synchronous pub/sub bus."""

    def __init__(self) -> None:
        self._subs: Dict[str, List[Callable[[dict], Any]]] = {}

    def subscribe(self, topic: str, fn: Callable[[dict], Any]) -> None:
        self._subs.setdefault(topic, []).append(fn)

    def publish(self, topic: str, payload: dict) -> None:
        for fn in self._subs.get(topic, []):
            fn(payload)


class AsyncInMemoryEventBus(InMemoryEventBus):
    """Asynchronous variant of :class:`InMemoryEventBus`."""

    async def publish(self, topic: str, payload: dict) -> None:
        tasks = []
        for fn in self._subs.get(topic, []):
            if inspect.iscoroutinefunction(fn):
                tasks.append(asyncio.create_task(fn(payload)))
            else:
                tasks.append(asyncio.create_task(asyncio.to_thread(fn, payload)))
        if tasks:
            await asyncio.gather(*tasks)

