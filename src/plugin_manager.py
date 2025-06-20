"""Utilities for discovering agents and tool plugins."""

from __future__ import annotations

import inspect
from importlib import metadata
from pathlib import Path
from typing import Any, Dict, List

from .utils.plugin_loader import (
    ENTRY_POINT_GROUP,
    ENTRY_POINT_PLUGINS,
    load_plugin,
)


def _iter_entry_points(group: str) -> List[str]:
    """Return entry point names registered under ``group``."""
    try:
        return [ep.name for ep in metadata.entry_points(group=group)]
    except TypeError:  # pragma: no cover - Python <3.10 fallback
        eps = metadata.entry_points()
        return [ep.name for ep in eps.get(group, [])]


def list_agents() -> List[str]:
    """Return available agent names.

    Agents can be provided via the ``brookside.agents`` entry point group
    or as modules under :mod:`src.agents`.
    """

    names = set(_iter_entry_points(ENTRY_POINT_GROUP))
    base = Path(__file__).resolve().parent / "agents"
    for path in base.rglob("*.py"):
        if path.name == "__init__.py" or path.name.startswith("_"):
            continue
        rel = path.relative_to(base).with_suffix("")
        names.add(".".join(rel.parts))
    return sorted(names)


def list_plugins() -> List[str]:
    """Return available tool plugin names."""

    names = set(_iter_entry_points(ENTRY_POINT_PLUGINS))
    base = Path(__file__).resolve().parent / "plugins"
    for path in base.glob("*.py"):
        if path.name in {"__init__.py", "base_plugin.py"} or path.name.startswith("_"):
            continue
        names.add(path.stem)
    return sorted(names)


def get_plugin_details(name: str) -> Dict[str, Any]:
    """Return metadata for the plugin identified by ``name``."""
    cls = load_plugin(name)
    return {
        "class": f"{cls.__module__}.{cls.__name__}",
        "name": getattr(cls, "name", ""),
        "doc": inspect.getdoc(cls) or "",
    }
