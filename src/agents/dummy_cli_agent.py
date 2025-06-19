"""Minimal agent used in CLI tests."""

from .base_agent import BaseAgent


class DummyCliAgent(BaseAgent):
    """Echo back the received payload."""

    def run(self, payload):
        return {"echo": payload}

