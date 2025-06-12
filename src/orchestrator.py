# src/orchestrator.py

"""Simple event orchestrator coordinating agents and memory storage."""

from typing import Dict, Any

from .agents.lead_capture_agent import LeadCaptureAgent
from .agents.chatbot_agent import ChatbotAgent
from .agents.crm_pipeline_agent import CRMPipelineAgent
from .agents.segmentation_ad_targeting_agent import SegmentationAdTargetingAgent
from .memory_service import MemoryService
from .utils.logger import get_logger


logger = get_logger(__name__)


class Orchestrator:
    """Minimal orchestrator that routes events to specialised agents."""

    def __init__(self, memory_endpoint: str):
        self.memory = MemoryService(memory_endpoint)
        self.agents = {
            "lead_capture": LeadCaptureAgent(),
            "chatbot": ChatbotAgent(),
            "crm_pipeline": CRMPipelineAgent(),
            "segmentation": SegmentationAdTargetingAgent(),
        }

    def handle_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Persist the event and delegate to the appropriate agent."""
        event_type = event.get("type")
        payload = event.get("payload", {})
        logger.info(f"Handling event type={event_type}")
        self.memory.store(event_type or "unknown", payload)

        agent = self.agents.get(event_type)
        if not agent:
            logger.warning(f"Unknown event type: {event_type}")
            return {"status": "ignored"}

        result = agent.run(payload)
        return {"status": "done", "result": result}
