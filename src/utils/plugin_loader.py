"""Utilities for loading agent classes from entry points or local modules."""

from __future__ import annotations

from importlib import import_module, metadata
from typing import Type, TypeVar

from ..agents.base_agent import BaseAgent
from ..plugins.base_plugin import BaseToolPlugin


ENTRY_POINT_GROUP = "brookside.agents"
ENTRY_POINT_PLUGINS = "brookside.plugins"

T = TypeVar("T")


def _iter_entry_points(group: str):
    """Return entry points for *group* across Python versions."""
    try:
        return metadata.entry_points(group=group)
    except TypeError:  # pragma: no cover - fallback for Python <3.10
        eps = metadata.entry_points()
        return eps.get(group, [])


def _load_component(name: str, group: str, package: str, base_cls: Type[T]) -> Type[T]:
    """Return a class named ``name`` either from entry points or ``package``.

    Parameters
    ----------
    name:
        Entry point name or module stem.
    group:
        Entry point group used for discovery.
    package:
        Package prefix searched when the entry point lookup fails.
    base_cls:
        Expected base class for validation.

    Returns
    -------
    Type[T]
        The resolved class implementing ``base_cls``.

    Raises
    ------
    ImportError
        If the module or class cannot be located.
    TypeError
        If the resolved object is not a subclass of ``base_cls``.
    """

    for ep in _iter_entry_points(group):
        if ep.name == name:
            cls = ep.load()
            if not isinstance(cls, type) or not issubclass(cls, base_cls):
                raise TypeError(
                    f"Entry point '{name}' does not resolve to a {base_cls.__name__} subclass"
                )
            return cls

    try:
        module = import_module(f"{package}.{name}")
    except ModuleNotFoundError as exc:
        raise ImportError(f"{base_cls.__name__} '{name}' not found") from exc

    last = name.rsplit(".", 1)[-1]
    class_name = "".join(word.capitalize() for word in last.split("_"))
    cls = getattr(module, class_name, None)
    if cls is None:
        raise ImportError(
            f"Class '{class_name}' not found in module '{package}.{name}'"
        )

    if not issubclass(cls, base_cls):
        raise TypeError(f"Class '{class_name}' is not a {base_cls.__name__} subclass")

    return cls


def load_agent(name: str) -> Type[BaseAgent]:
    """Load an agent class by ``name``.

    The loader first searches registered entry points under
    :data:`ENTRY_POINT_GROUP`. If ``name`` matches an entry point, the
    referenced class is returned. Otherwise the loader falls back to importing
    ``src.agents.<name>`` and resolving ``<CamelCase(last_segment)>`` within
    that module. ``name`` may include package separators (e.g.
    ``sales.lead_capture_agent``).
    module.

    Parameters
    ----------
    name:
        Entry point name or module stem of the agent.

    Returns
    -------
    Type[BaseAgent]
        The located agent class.

    Raises
    ------
    ImportError
        If no matching entry point or local module is found.
    TypeError
        If the resolved object is not a :class:`BaseAgent` subclass.
    """
    return _load_component(
        name,
        ENTRY_POINT_GROUP,
        "src.agents",
        BaseAgent,
    )


def load_plugin(name: str) -> Type[BaseToolPlugin]:
    """Load a tool plugin class by ``name``.

    The search order mirrors :func:`load_agent` but looks under the
    ``brookside.plugins`` entry point group and ``src.plugins`` package.
    """

    return _load_component(
        name,
        ENTRY_POINT_PLUGINS,
        "src.plugins",
        BaseToolPlugin,
    )
