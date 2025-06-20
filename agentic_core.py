"""Foundation utilities for agent based systems.

This module exposes a minimal set of abstractions used by multiple agents.
It purposefully avoids external dependencies so it can be dropped into a
wide variety of small projects.
"""

from __future__ import annotations

import asyncio
import inspect
from typing import Any, Callable, Dict, Iterable, List


class EventBus:
    """Very small in-memory pub/sub bus.

    Example
    -------
    >>> bus = EventBus()
    >>> events: List[dict] = []
    >>> bus.subscribe("greet", lambda p: events.append(p))
    >>> bus.publish("greet", {"msg": "hi"})
    >>> events
    [{'msg': 'hi'}]
    """

    def __init__(self) -> None:
        self._subs: Dict[str, List[Callable[[dict], Any]]] = {}

    def subscribe(self, topic: str, fn: Callable[[dict], Any]) -> None:
        """Register ``fn`` to be called when ``topic`` is published."""
        self._subs.setdefault(topic, []).append(fn)

    def publish(self, topic: str, payload: dict) -> None:
        """Synchronously notify all subscribers of ``topic``."""
        for fn in self._subs.get(topic, []):
            fn(payload)


class AsyncEventBus(EventBus):
    """Asynchronous variant of :class:`EventBus` using ``asyncio``."""

    async def publish(self, topic: str, payload: dict) -> None:
        """Dispatch ``payload`` to subscribers as asyncio tasks."""
        tasks = []
        for fn in self._subs.get(topic, []):
            if inspect.iscoroutinefunction(fn):
                tasks.append(asyncio.create_task(fn(payload)))
            else:
                tasks.append(asyncio.create_task(asyncio.to_thread(fn, payload)))
        if tasks:
            await asyncio.gather(*tasks)


class MemoryService:
    """Trivial in-memory memory store.

    The implementation simply keeps everything in a dictionary.  Replace the
    in-process storage with a vector database or other persistent layer if
    required.

    Example
    -------
    >>> mem = MemoryService()
    >>> mem.store("notes", ["foo", "bar"])
    >>> mem.query("notes", "ba")
    ['bar']
    """

    def __init__(self) -> None:
        self._db: Dict[str, List[str]] = {}

    def query(self, namespace: str, text: str, top_k: int = 5) -> List[str]:
        """Return stored items containing ``text`` within ``namespace``."""
        haystack = self._db.get(namespace, [])
        matches = [item for item in haystack if text.lower() in item.lower()]
        return matches[:top_k]

    def store(self, namespace: str, items: Iterable[str]) -> None:
        """Append ``items`` to ``namespace``."""
        self._db.setdefault(namespace, []).extend(list(items))


def Tool(name: str | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator for registering a method as a toolbox entry."""

    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        setattr(fn, "_tool_name", name or fn.__name__)
        setattr(fn, "_is_tool", True)
        return fn

    return decorator


class AbstractAgent:
    """Base class for simple agents using :class:`EventBus`.

    Example
    -------
    >>> class EchoAgent(AbstractAgent):
    ...     def run(self, event: dict) -> dict:
    ...         return event
    >>> agent = EchoAgent("echo")
    >>> agent.run({"hello": "world"})
    {'hello': 'world'}
    """

    name: str
    toolbox: Dict[str, Callable[..., Any]]

    def __init__(self, name: str) -> None:
        self.name = name
        self.toolbox = {}
        # auto-register @Tool methods
        for attr in dir(self):
            maybe = getattr(self, attr)
            if callable(maybe) and getattr(maybe, "_is_tool", False):
                tool_name = getattr(maybe, "_tool_name", attr)
                self.toolbox[tool_name] = maybe

    def publish(self, event_bus: EventBus, event: dict) -> None:
        """Helper to publish ``event`` on ``event_bus``."""
        event_bus.publish(self.name, event)

    def run(self, event: dict) -> dict:
        """Handle ``event`` and return a response. Override in subclasses."""
        raise NotImplementedError


async def run_maybe_async(fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Call ``fn`` and await the result if it returns an awaitable."""
    result = fn(*args, **kwargs)
    if inspect.isawaitable(result):
        return await result
    return result


def run_sync(awaitable: Any) -> Any:
    """Execute ``awaitable`` synchronously using ``asyncio.run``."""
    return asyncio.run(awaitable)
