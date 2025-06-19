"""Generic retry decorator for tools calling external services."""

from __future__ import annotations

from functools import wraps
from time import sleep
from typing import Any, Callable, Iterable, Tuple, Type

from .logger import get_logger

logger = get_logger(__name__)


DefExc = Tuple[Type[BaseException], ...]


def retry_tool(
    retries: int = 3,
    *,
    delay: float = 0.0,
    fallback: Callable[[BaseException, tuple, dict], Any] | None = None,
    exceptions: Iterable[Type[BaseException]] | None = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Retry decorator for tool methods that call external services.

    Parameters
    ----------
    retries:
        Number of attempts before giving up. A value of ``0`` disables retry.
    delay:
        Optional pause between attempts in seconds. Defaults to ``0`` for no
        wait time.
    fallback:
        Optional handler invoked with ``(exception, args, kwargs)`` after the
        final failed attempt. If omitted, the original exception is re-raised.
    exceptions:
        Iterable of exception classes that should trigger a retry. Defaults to
        ``(Exception,)``.

    Examples
    --------
    >>> from src.utils.retry import retry_tool
    >>> @retry_tool(retries=2)
    ... def unreliable():
    ...     raise RuntimeError('fail')
    >>> unreliable()  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    RuntimeError: fail
    """

    exc_types: DefExc = tuple(exceptions) if exceptions else (Exception,)

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(retries + 1):
                try:
                    return func(*args, **kwargs)
                except exc_types as exc:  # pragma: no cover - hit via tests
                    if attempt == retries:
                        if fallback:
                            logger.error(
                                "Max retries exceeded for %s; invoking fallback",
                                func.__name__,
                            )
                            return fallback(exc, args, kwargs)
                        raise
                    logger.warning(
                        "Attempt %s/%s for %s failed: %s",
                        attempt + 1,
                        retries + 1,
                        func.__name__,
                        exc,
                    )
                    if delay > 0:
                        sleep(delay)
        return wrapper

    return decorator

