from __future__ import annotations

"""Common orchestrator base class used across examples."""

from typing import Any, Dict, Type
import inspect

from agentic_core import EventBus, AsyncEventBus, run_sync, run_maybe_async
from .tools.metrics_tools.prometheus_tool import PrometheusPusher
from .config import settings
from .events import (
    LeadCaptureEvent,
    ChatbotEvent,
    CRMPipelineEvent,
    SegmentationEvent,
    IntegrationRequest,
)

from .memory_service.base import BaseMemoryService
import logging


logger = logging.getLogger(__name__)


class BaseOrchestrator:
    """Provide shared event dispatch logic for orchestrators."""

    def __init__(
        self,
        bus: EventBus | AsyncEventBus | None = None,
        memory: BaseMemoryService | None = None,
        *,
        metrics_job: str = "orchestrator",
    ) -> None:
        self.bus = bus or AsyncEventBus()
        self.memory = memory
        self.agents: Dict[str, Any] = {}
        self.token_usage: Dict[str, int] = {}
        self.loop_counts: Dict[str, int] = {}
        self.pusher = (
            PrometheusPusher(job=metrics_job)
            if settings.PROMETHEUS_PUSHGATEWAY
            else None
        )
        self.event_schemas: Dict[str, Type[Any]] = {
            "lead_capture": LeadCaptureEvent,
            "chatbot": ChatbotEvent,
            "crm_pipeline": CRMPipelineEvent,
            "segmentation": SegmentationEvent,
            "integration_request": IntegrationRequest,
        }

    def get_agent_by_skill(self, skill: str):
        """Return the first agent advertising ``skill`` or ``None``."""

        for agent in self.agents.values():
            if skill in getattr(agent, "skills", []):
                return agent
        return None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _estimate_tokens(self, payload: Any) -> int:
        """Return a rough token estimate for ``payload``.

        Agents may override this by implementing ``estimate_tokens``. In the
        absence of a custom implementation the fallback simply measures the
        length of the string representation which keeps the code free of heavy
        dependencies while providing deterministic budgets for tests.
        """

        if hasattr(payload, "estimate_tokens"):
            try:  # pragma: no cover - custom implementations may fail
                return int(payload.estimate_tokens())
            except Exception:
                pass
        return len(str(payload))

    async def handle_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Persist ``event`` if a memory service is available and dispatch it."""
        event_type = event.get("type")
        payload = event.get("payload", {})
        logger.info(f"Handling event type={event_type}")

        if self.memory:
            await run_maybe_async(self.memory.store, event_type or "unknown", payload)

        agent = self.agents.get(event_type)
        if not agent:
            logger.warning(f"Unknown event type: {event_type}")
            return {"status": "ignored"}

        schema = self.event_schemas.get(event_type)
        if schema:
            try:
                payload_obj = schema(**payload)
            except TypeError as exc:
                logger.warning(f"Invalid payload for {event_type}: {exc}")
                return {"status": "invalid"}
        else:
            payload_obj = payload

        agent_name = getattr(agent, "__class__").__name__
        self.loop_counts[agent_name] = self.loop_counts.get(agent_name, 0) + 1
        loops = self.loop_counts[agent_name]

        tokens = self._estimate_tokens(payload_obj)
        self.token_usage[agent_name] = self.token_usage.get(agent_name, 0) + tokens

        # Check budgets if defined
        loop_budget = getattr(agent, "loop_budget", None)
        token_budget = getattr(agent, "token_budget", None)
        if loop_budget is not None and loops > loop_budget:
            logger.warning(f"Loop budget exceeded for {agent_name}")
            return {"status": "terminated", "reason": "loop_budget_exceeded"}
        if token_budget is not None and self.token_usage[agent_name] > token_budget:
            logger.warning(f"Token budget exceeded for {agent_name}")
            return {"status": "terminated", "reason": "token_budget_exceeded"}

        if self.pusher:
            labels = {"agent": agent_name}
            try:  # pragma: no cover - metric push failures
                self.pusher.push_metric("agent_tokens_used", tokens, labels)
                self.pusher.push_metric("agent_loop_count", loops, labels)
            except Exception:
                logger.exception("Failed to push Prometheus metrics")

        result = agent.run(payload_obj)
        if inspect.isawaitable(result):
            result = await result
        return {"status": "done", "result": result}

    async def delegate_by_skill(
        self, skill: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Dispatch ``payload`` to the first agent advertising ``skill``."""

        logger.info(f"Delegating using skill={skill}")
        agent = self.get_agent_by_skill(skill)
        if not agent:
            logger.warning(f"No agent found with skill: {skill}")
            return {"status": "unhandled"}

        agent_name = getattr(agent, "__class__").__name__
        self.loop_counts[agent_name] = self.loop_counts.get(agent_name, 0) + 1
        loops = self.loop_counts[agent_name]

        tokens = self._estimate_tokens(payload)
        self.token_usage[agent_name] = self.token_usage.get(agent_name, 0) + tokens

        loop_budget = getattr(agent, "loop_budget", None)
        token_budget = getattr(agent, "token_budget", None)
        if loop_budget is not None and loops > loop_budget:
            logger.warning(f"Loop budget exceeded for {agent_name}")
            return {"status": "terminated", "reason": "loop_budget_exceeded"}
        if token_budget is not None and self.token_usage[agent_name] > token_budget:
            logger.warning(f"Token budget exceeded for {agent_name}")
            return {"status": "terminated", "reason": "token_budget_exceeded"}

        if self.pusher:
            labels = {"agent": agent_name}
            try:  # pragma: no cover - metric push failures
                self.pusher.push_metric("agent_tokens_used", tokens, labels)
                self.pusher.push_metric("agent_loop_count", loops, labels)
            except Exception:
                logger.exception("Failed to push Prometheus metrics")

        result = agent.run(payload)
        if inspect.isawaitable(result):
            result = await result
        return {"status": "done", "result": result}

    def handle_event_sync(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous wrapper around :meth:`handle_event`."""
        return run_sync(self.handle_event(event))

    def delegate_by_skill_sync(
        self, skill: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synchronous wrapper around :meth:`delegate_by_skill`."""

        return run_sync(self.delegate_by_skill(skill, payload))
