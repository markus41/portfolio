from __future__ import annotations

"""Lightweight agent for reviewing text drafts.

The ``ReviewAgent`` checks a draft for banned terms and either approves it or
returns feedback comments. It can optionally subscribe to an
:class:`agentic_core.EventBus` to automatically review drafts published on the
``draft.created`` topic.
"""

from typing import Iterable, List

from agentic_core import EventBus

from .base_agent import BaseAgent


class ReviewAgent(BaseAgent):
    """Simple reviewer that approves or rejects drafts.

    Parameters
    ----------
    bus:
        Event bus used for communication. When provided, the agent subscribes to
        the ``draft.created`` topic and publishes results to ``draft.reviewed``.
    banned_words:
        Optional iterable of words that should trigger a rejection.
    """

    def __init__(
        self,
        bus: EventBus | None = None,
        banned_words: Iterable[str] | None = None,
    ) -> None:
        self.bus = bus
        self.banned_words = {w.lower() for w in (banned_words or {"fixme", "bad"})}
        if self.bus:
            self.bus.subscribe("draft.created", self._on_draft)

    def _on_draft(self, payload: dict) -> None:
        """EventBus callback for incoming drafts."""
        result = self.run(payload)
        if self.bus:
            self.bus.publish("draft.reviewed", result)

    def run(self, payload: dict) -> dict:
        """Examine a draft and return an approval decision."""
        draft = str(payload.get("draft", ""))
        comments: List[str] = []
        for word in self.banned_words:
            if word in draft.lower():
                comments.append(f"Remove forbidden term '{word}'.")

        status = "rejected" if comments else "approved"
        result = {"status": status}
        if comments:
            result["comments"] = comments
        return result
