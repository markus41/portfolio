"""Minimal agent used in CLI tests."""

from __future__ import annotations

from typing import Any, Dict

from ..base_agent import BaseAgent


class DummyCliAgent(BaseAgent):
    """Echo back the received payload."""

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Return the input payload for testing."""
        return {"echo": payload}
