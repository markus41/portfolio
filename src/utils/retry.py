"""Generic retry decorator for tools calling external services."""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable, Iterable, Tuple, Type

from .logger import get_logger

logger = get_logger(__name__)


DefExc = Tuple[Type[BaseException], ...]


def retry_tool(
    retries: int = 3,
    *,
    fallback: Callable[[BaseException, tuple, dict], Any] | None = None,
    exceptions: Iterable[Type[BaseException]] | None = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Retry decorator for tool methods that call external services.

    Parameters
    ----------
    retries:
        Number of attempts before giving up. A value of ``0`` disables retry.
    fallback:
        Optional handler invoked with ``(exception, args, kwargs)`` after the
        final failed attempt. If omitted the original exception is re-raised.
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
            attempt = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except exc_types as exc:  # pragma: no cover - hit via tests
                    attempt += 1
                    logger.warning(
                        "Attempt %s/%s for %s failed: %s",
                        attempt,
                        retries + 1,
                        func.__name__,
                        exc,
                    )
                    if attempt > retries:
                        if fallback:
                            logger.error(
                                "Max retries exceeded for %s; invoking fallback",
                                func.__name__,
                            )
                            return fallback(exc, args, kwargs)
                        raise
        return wrapper

    return decorator

