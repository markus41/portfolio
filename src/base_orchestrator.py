from __future__ import annotations

"""Common orchestrator base class used across examples."""

from typing import Any, Dict, Type

from agentic_core import EventBus
from .events import (
    LeadCaptureEvent,
    ChatbotEvent,
    CRMPipelineEvent,
    SegmentationEvent,
)

from .memory_service import MemoryService
from .utils.logger import get_logger


logger = get_logger(__name__)


class BaseOrchestrator:
    """Provide shared event dispatch logic for orchestrators."""

    def __init__(
        self, bus: EventBus | None = None, memory: MemoryService | None = None
    ) -> None:
        self.bus = bus or EventBus()
        self.memory = memory
        self.agents: Dict[str, Any] = {}
        self.event_schemas: Dict[str, Type[Any]] = {
            "lead_capture": LeadCaptureEvent,
            "chatbot": ChatbotEvent,
            "crm_pipeline": CRMPipelineEvent,
            "segmentation": SegmentationEvent,
        }

    def handle_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Persist ``event`` if a memory service is available and dispatch it."""
        event_type = event.get("type")
        payload = event.get("payload", {})
        logger.info(f"Handling event type={event_type}")

        if self.memory:
            self.memory.store(event_type or "unknown", payload)

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
        return {"status": "done", "result": result}
