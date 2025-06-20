"""Context manager for accessing per-request :class:`UserSettingsData`."""

from __future__ import annotations

from contextlib import contextmanager
import contextvars
from typing import Optional

from .user_settings import UserSettingsData

_current: contextvars.ContextVar[Optional[UserSettingsData]] = contextvars.ContextVar(
    "current_user_settings", default=None
)


def get_current() -> Optional[UserSettingsData]:
    """Return settings associated with the current request if any."""

    return _current.get()


@contextmanager
def use_settings(settings: Optional[UserSettingsData]):
    """Temporarily make ``settings`` active within the context."""

    token = _current.set(settings)
    try:
        yield
    finally:
        _current.reset(token)
