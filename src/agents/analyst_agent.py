"""Expose :class:`roles.AnalystAgent` for external loading."""

from .roles import AnalystAgent as _AnalystAgent


class AnalystAgent(_AnalystAgent):
    """Concrete subclass used by JSON templates."""

    pass
