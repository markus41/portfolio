from __future__ import annotations

"""Common orchestrator base class used across examples."""

from typing import Any, Dict, Type
import inspect

from agentic_core import (
    EventBus,
    AsyncEventBus,
    create_event_bus,
    run_sync,
    run_maybe_async,
)
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
    ) -> None:
        self.bus = bus or create_event_bus(async_mode=True)
        self.memory = memory
        self.agents: Dict[str, Any] = {}
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
