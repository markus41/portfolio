# src/orchestrator.py

"""Event Orchestrator.

This module exposes a tiny :class:`Orchestrator` class used in the tests. The
class wires together a handful of example agents and a simple memory service.
The orchestrator receives events from the outside world, persists them to the
``MemoryService`` and then forwards the event payload to the appropriate agent
based on the event ``type`` field.  Each agent is responsible for performing a
very small piece of functionality such as lead capture or CRM pipeline
processing.

The goal of the example orchestrator is purely illustrative.  It shows how one
might hook up multiple agents without including any heavy framework code or
infrastructure specific details.
"""

from typing import Dict, Any

from .agents.lead_capture_agent import LeadCaptureAgent
from .agents.chatbot_agent import ChatbotAgent
from .agents.crm_pipeline_agent import CRMPipelineAgent
from .agents.segmentation_ad_targeting_agent import SegmentationAdTargetingAgent
from .memory_service import MemoryService
from .utils.logger import get_logger


logger = get_logger(__name__)


class Orchestrator:
    """Route incoming events to specialised agents.

    Parameters
    ----------
    memory_endpoint:
        URL of the memory service used to persist and retrieve events.
    """

    def __init__(self, memory_endpoint: str):
        # the in-memory storage (could be a vector DB or search engine)
        self.memory = MemoryService(memory_endpoint)

        # Register a very small set of agents keyed by event type.  In a real
        # system this might be configurable or use entry points/plugins.
        # fixed mapping of event types to agent instances used in tests
        self.agents = {
            "lead_capture": LeadCaptureAgent(),
            "chatbot": ChatbotAgent(),
            "crm_pipeline": CRMPipelineAgent(),
            "segmentation": SegmentationAdTargetingAgent(),
        }

    def handle_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Persist the event and delegate handling to an agent.

        Parameters
        ----------
        event:
            Dictionary describing the event.  It must contain a ``type`` key
            which determines the target agent and an optional ``payload`` key
            containing the data that should be processed by that agent.

        Returns
        -------
        dict
            ``{"status": "done", "result": ...}`` when an agent handled the
            event or ``{"status": "ignored"}`` for unknown events.
        """

        event_type = event.get("type")
        payload = event.get("payload", {})
        logger.info(f"Handling event type={event_type}")

        # store the raw event payload for auditing/debugging purposes
        self.memory.store(event_type or "unknown", payload)

        agent = self.agents.get(event_type)
        if not agent:
            logger.warning(f"Unknown event type: {event_type}")
            return {"status": "ignored"}

        # delegate to the specific agent instance
        result = agent.run(payload)
        return {"status": "done", "result": result}
