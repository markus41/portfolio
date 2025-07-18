from __future__ import annotations

"""Redis based event bus implementations."""

import asyncio
import inspect
import json
import threading
import types
from typing import Any, Callable, Dict, List, Optional

from .base import BaseEventBus
import logging

try:  # optional dependency
    import redis  # type: ignore
except Exception:  # pragma: no cover - fallback when redis is missing
    redis = types.SimpleNamespace(
        Redis=types.SimpleNamespace(
            from_url=lambda *a, **k: types.SimpleNamespace(
                publish=lambda *a, **k: None,
                pubsub=lambda *a, **k: types.SimpleNamespace(
                    subscribe=lambda *a, **k: None,
                    listen=lambda: iter(()),
                ),
                ping=lambda *a, **k: True,
            )
        )
    )

logger = logging.getLogger(__name__)


class RedisEventBus(BaseEventBus):
    """Publish/subscribe using Redis channels."""

    def __init__(self, url: str, *, client: Any | None = None) -> None:
        self.client = client or redis.Redis.from_url(url, decode_responses=True)
        self.pubsub = self.client.pubsub(ignore_subscribe_messages=True)
        self._subs: Dict[str, List[Callable[[dict], Any]]] = {}
        self._thread = threading.Thread(target=self._listen, daemon=True)
        self._thread.start()
        try:  # pragma: no cover - network failure not relevant for unit tests
            self.client.ping()
        except Exception as exc:  # pragma: no cover - log only
            logger.warning(f"Redis ping failed: {exc}")

    def subscribe(self, topic: str, fn: Callable[[dict], Any]) -> None:
        first = topic not in self._subs
        self._subs.setdefault(topic, []).append(fn)
        if first:
            self.pubsub.subscribe(topic)

    def publish(self, topic: str, payload: dict) -> None:
        try:
            self.client.publish(topic, json.dumps(payload))
        except Exception as exc:  # pragma: no cover - runtime errors
            logger.error(f"Redis publish failed: {exc}")

    def _handle_message(self, topic: str, payload: dict) -> None:
        for fn in self._subs.get(topic, []):
            if inspect.iscoroutinefunction(fn):
                asyncio.run(fn(payload))
            else:
                fn(payload)

    def _listen(self) -> None:
        for msg in self.pubsub.listen():
            if msg.get("type") != "message":
                continue
            try:
                data = json.loads(msg["data"])
            except Exception:
                continue
            topic = msg["channel"]
            self._handle_message(topic, data)


class AsyncRedisEventBus(RedisEventBus):
    """Async wrapper around :class:`RedisEventBus`."""

    def __init__(self, url: str, *, client: Any | None = None, loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
        self.loop = loop or asyncio.get_event_loop()
        super().__init__(url, client=client)

    def _handle_message(self, topic: str, payload: dict) -> None:
        for fn in self._subs.get(topic, []):
            if inspect.iscoroutinefunction(fn):
                self.loop.create_task(fn(payload))
            else:
                self.loop.create_task(asyncio.to_thread(fn, payload))

    async def publish(self, topic: str, payload: dict) -> None:
        await asyncio.to_thread(super().publish, topic, payload)

