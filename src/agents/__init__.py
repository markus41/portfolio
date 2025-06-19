"""Aggregate access to all agent packages.

The :mod:`src.agents` package exposes sales, operations and real estate
subpackages. Attribute access is delegated to these subpackages so
imports written against the legacy flat layout continue to work::

    from src.agents import LeadCaptureAgent

For clarity and to reduce import overhead, prefer importing from the
specific subpackage going forward::

    from src.agents.sales import LeadCaptureAgent
"""

from .base_agent import BaseAgent
from . import sales, operations, real_estate

__all__ = ["BaseAgent", *sales.__all__, *operations.__all__, *real_estate.__all__]


def __getattr__(name: str):
    for pkg in (sales, operations, real_estate):
        if hasattr(pkg, name):
            attr = getattr(pkg, name)
            globals()[name] = attr
            return attr
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
