from __future__ import annotations

"""Abstract interface and helpers for event bus adapters."""

import abc
from typing import Any, Callable


class BaseEventBus(abc.ABC):
    """Define the minimal publish/subscribe API used across the project."""

    @abc.abstractmethod
    def subscribe(self, topic: str, fn: Callable[[dict], Any]) -> None:
        """Register ``fn`` as a callback for ``topic`` events."""

    @abc.abstractmethod
    def publish(self, topic: str, payload: dict) -> Any:
        """Emit ``payload`` to all subscribers of ``topic``."""

