"""QA agent validating SupportAgent conversations."""

from __future__ import annotations

import json
from agentic_core import (
    AbstractAgent,
    EventBus,
    AsyncEventBus,
    run_maybe_async,
    run_sync,
)
from .agents.support_agent import SupportAgent
from .utils.logger import get_logger

logger = get_logger(__name__)


class QAAgent(AbstractAgent):
    """Run scripted conversations and emit QA results."""

    def __init__(
        self, bus: EventBus | AsyncEventBus, support_agent: SupportAgent
    ) -> None:
        super().__init__("qa")
        self.bus = bus
        self.support = support_agent
        self.bus.subscribe("QA.Run", self.run)

    async def run(self, payload: dict) -> dict:
        scripts = payload.get("scripts", [])
        passed = True
        for msg in scripts:
            reply = await run_maybe_async(self.support.run, msg)
            try:
                json.dumps(reply)
            except Exception:
                passed = False
        result = {"passed": passed}
        await run_maybe_async(self.bus.publish, "QA.Report", result)
        return result

    def run_sync(self, payload: dict) -> dict:
        """Compatibility wrapper running :meth:`run` synchronously."""
        return run_sync(self.run(payload))
