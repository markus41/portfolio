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

from typing import Dict, Any, List
import importlib
import json
from pathlib import Path

try:  # pragma: no cover - optional dependency
    import openai
except Exception:  # pragma: no cover - optional dependency
    openai = None

from agentic_core import EventBus, AsyncEventBus, run_maybe_async, run_sync

from .base_orchestrator import BaseOrchestrator

from .agents.lead_capture_agent import LeadCaptureAgent
from .agents.chatbot_agent import ChatbotAgent
from .agents.crm_pipeline_agent import CRMPipelineAgent
from .agents.segmentation_ad_targeting_agent import SegmentationAdTargetingAgent
from .memory_service import MemoryService
from .utils.logger import get_logger
from .agents.support_agent import SupportAgent
from .agents.procurement_agent import ProcurementAgent
from .agents.revops_agent import RevOpsAgent


logger = get_logger(__name__)

USE_LLM_PLANNER = False


def gpt_plan(goal: str, available_events: List[str]) -> str:
    """Plan next action using GPT given a goal and events."""
    if not openai:
        raise RuntimeError("openai package is not installed")
    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"{goal}\nEvents: {available_events}"}],
        timeout=10,
    )
    return resp.choices[0].message.content


class _SupportTools:
    """Minimal toolbox used for SupportAgent demos."""

    def lookup_order(self, order_id: str) -> dict:  # pragma: no cover - demo stub
        return {"status": "shipped", "days_delayed": 0}

    def issue_refund(self, order_id: str, pct: int) -> str:  # pragma: no cover - demo stub
        return "r1"

    def create_ticket(self, summary: str, customer_id: str) -> str:  # pragma: no cover - demo stub
        return "t1"


class Orchestrator(BaseOrchestrator):
    """Route incoming events to specialised agents.

    Parameters
    ----------
    memory_endpoint:
        URL of the memory service used to persist and retrieve events.
    config_path:
        Optional path to a JSON file mapping event types to agent classes.
    """

    def __init__(self, memory_endpoint: str, use_llm_planner: bool = False, config_path: str | None = None):
        bus = AsyncEventBus()
        memory = MemoryService(memory_endpoint)
        super().__init__(bus=bus, memory=memory)
        self.use_llm_planner = use_llm_planner

        if config_path:
            path = Path(config_path)
            with path.open() as fh:
                mapping = json.load(fh)
            self.agents = {}
            for event, target in mapping.items():
                module_name, class_name = target.rsplit(".", 1)
                module = importlib.import_module(module_name)
                agent_cls = getattr(module, class_name)
                self.agents[event] = agent_cls()
        else:
            # Register a very small set of agents keyed by event type.  In a real
            # system this might be configurable or use entry points/plugins.
            # fixed mapping of event types to agent instances used in tests
            self.agents = {
                "lead_capture": LeadCaptureAgent(),
                "chatbot": ChatbotAgent(),
                "crm_pipeline": CRMPipelineAgent(),
                "segmentation": SegmentationAdTargetingAgent(),
            }

        # Additional global agents used outside of handle_event
        self.support = SupportAgent(
            "demo", self.memory, self.bus, toolbox=_SupportTools()
        )
        self.procurement = ProcurementAgent(self.bus, suppliers=[])
        self.revops = RevOpsAgent(self.bus)

        # planning logic wiring
        self.bus.subscribe("Lead.Won", self._on_lead_won)
        self.bus.subscribe(
            "Project.MaterialsNeeded.Resolved", self._on_materials_resolved
        )

    # --- planning callbacks -------------------------------------------------

    async def _on_lead_won(self, payload: dict) -> None:
        """Trigger material planning after a lead is won."""
        if USE_LLM_PLANNER:
            try:
                gpt_plan("plan materials", ["Project.MaterialsNeeded"])
            except Exception as exc:  # pragma: no cover - network failures
                logger.warning(f"LLM planner failed: {exc}")
        await run_maybe_async(self.bus.publish, "Project.MaterialsNeeded", payload)

    async def _on_materials_resolved(self, payload: dict) -> None:
        """Schedule project kickoff once materials are procured."""
        await run_maybe_async(
            self.bus.publish,
            "Email.SendKickoff",
            {"project_id": payload.get("project_id")},
        )

    async def monthly_tick(self) -> None:
        """Emit the RevOps analysis cron event."""
        await run_maybe_async(self.bus.publish, "RevOps.Analyze", {"tenant_id": "demo"})

