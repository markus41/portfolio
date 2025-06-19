"""Utilities for loading agent classes from entry points or local modules."""

from __future__ import annotations

from importlib import import_module, metadata
from typing import Type

from ..agents.base_agent import BaseAgent


ENTRY_POINT_GROUP = "brookside.agents"


def _iter_entry_points(group: str):
    """Return entry points for *group* across Python versions."""
    try:
        return metadata.entry_points(group=group)
    except TypeError:  # pragma: no cover - fallback for Python <3.10
        eps = metadata.entry_points()
        return eps.get(group, [])


def load_agent(name: str) -> Type[BaseAgent]:
    """Load an agent class by ``name``.

    The loader first searches registered entry points under
    :data:`ENTRY_POINT_GROUP`. If ``name`` matches an entry point, the
    referenced class is returned. Otherwise the loader falls back to importing
    ``src.agents.<name>`` and resolving ``<CamelCase(name)>`` within that
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
    for ep in _iter_entry_points(ENTRY_POINT_GROUP):
        if ep.name == name:
            agent_cls = ep.load()
            if not isinstance(agent_cls, type) or not issubclass(agent_cls, BaseAgent):
                raise TypeError(
                    f"Entry point '{name}' does not resolve to a BaseAgent subclass"
                )
            return agent_cls

    try:
        module = import_module(f"src.agents.{name}")
    except ModuleNotFoundError as exc:
        raise ImportError(f"Agent '{name}' not found") from exc

    class_name = "".join(word.capitalize() for word in name.split("_"))
    agent_cls = getattr(module, class_name, None)
    if agent_cls is None:
        raise ImportError(f"Class '{class_name}' not found in module 'src.agents.{name}'")

    if not issubclass(agent_cls, BaseAgent):
        raise TypeError(f"Class '{class_name}' is not a BaseAgent subclass")

    return agent_cls
