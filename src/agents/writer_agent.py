"""Thin wrapper to expose :class:`roles.WriterAgent` via plugin loader."""

from .roles import WriterAgent as _WriterAgent


class WriterAgent(_WriterAgent):
    """Concrete subclass used by JSON templates."""

    pass
