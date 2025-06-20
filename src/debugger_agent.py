"""Agent that proposes fixes when errors occur."""

from __future__ import annotations

import json
from agentic_core import AbstractAgent, EventBus
import logging

try:  # pragma: no cover - optional dependency
    import openai
except Exception:  # pragma: no cover - optional dependency
    openai = None

GITHUB_ENABLED = False
logger = logging.getLogger(__name__)


def open_pr(diff: str) -> None:  # pragma: no cover - placeholder
    if not GITHUB_ENABLED:
        return
    # Real implementation would call GitHub API
    logger.info("Would open PR with diff:\n%s", diff)


class DebuggerAgent(AbstractAgent):
    """Listen for ``*.Error`` events and suggest patches."""

    def __init__(self, bus: EventBus) -> None:
        super().__init__("debugger")
        self.bus = bus
        self.bus.subscribe("Error", self.run)

    def _ask_gpt(self, context: str) -> str:
        if not openai:
            raise RuntimeError("openai package is not installed")
        resp = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": context}],
            timeout=10,
        )
        return resp.choices[0].message.content

    def run(self, payload: dict) -> dict:
        context = payload.get("trace", "")
        try:
            diff = self._ask_gpt(context)
        except Exception as exc:  # pragma: no cover - network failures
            logger.warning(f"Debugger GPT failed: {exc}")
            diff = ""
        if GITHUB_ENABLED and diff:
            open_pr(diff)
        return {"diff": diff}
