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

from .agents.sales.lead_capture_agent import LeadCaptureAgent
from .agents.sales.chatbot_agent import ChatbotAgent
from .agents.sales.crm_pipeline_agent import CRMPipelineAgent
from .agents.sales.segmentation_ad_targeting_agent import SegmentationAdTargetingAgent
from .memory_service import RestMemoryService
from .memory_service.rest_async import AsyncRestMemoryService
from .memory_service.file import FileMemoryService
from .memory_service.redis import RedisMemoryService
from .memory_service.embedding import EmbeddingMemoryService
from .memory_service.base import BaseMemoryService
from .config import settings
import logging
from .agents.operations.support_agent import SupportAgent
from .agents.operations.procurement_agent import ProcurementAgent
from .agents.sales.revops_agent import RevOpsAgent
from .agents.integration_agent import IntegrationAgent


logger = logging.getLogger(__name__)

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

    def issue_refund(
        self, order_id: str, pct: int
    ) -> str:  # pragma: no cover - demo stub
        return "r1"

    def create_ticket(
        self, summary: str, customer_id: str
    ) -> str:  # pragma: no cover - demo stub
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

    def __init__(
        self,
        memory_endpoint: str | None = None,
        use_llm_planner: bool = False,
        config_path: str | None = None,
        *,
        memory_backend: str | None = None,
        memory_file: str | None = None,
    ) -> None:
        """Create a new orchestrator instance.

        Parameters
        ----------
        memory_endpoint:
            REST endpoint for the default :class:`RestMemoryService` backend.
        use_llm_planner:
            Enable GPT based planning callbacks.
        config_path:
            Optional path to a JSON mapping of event types to agent classes.
        memory_backend:
            Select the memory implementation: ``"rest"`` (default), ``"rest_async"``,
            ``"file"``, ``"redis"`` or ``"embedding"`` for in-memory similarity
            search.
        memory_file:
            Path used by the ``file`` backend if specified.
        """

        bus = AsyncEventBus()

        backend = memory_backend or settings.MEMORY_BACKEND
        if backend == "file":
            path = memory_file or settings.MEMORY_FILE_PATH
            memory: BaseMemoryService = FileMemoryService(path)
        elif backend == "redis":
            url = settings.MEMORY_REDIS_URL
            memory = RedisMemoryService(url)
        elif backend == "embedding":
            field = settings.MEMORY_EMBED_FIELD
            memory = EmbeddingMemoryService(text_key=field)
        elif backend == "rest_async":
            endpoint = memory_endpoint or settings.MEMORY_ENDPOINT
            memory = AsyncRestMemoryService(endpoint)
        else:
            endpoint = memory_endpoint or settings.MEMORY_ENDPOINT
            memory = RestMemoryService(endpoint)

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
                "integration_request": IntegrationAgent(
                    config_path="configs/integrations.yaml"
                ),
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

    # --- shutdown helpers -------------------------------------------------

    async def aclose(self) -> None:
        """Release resources held by the orchestrator."""
        if hasattr(self.memory, "aclose"):
            await self.memory.aclose()

    def close(self) -> None:
        """Synchronous wrapper around :meth:`aclose`."""
        if hasattr(self.memory, "aclose"):
            run_sync(self.memory.aclose())
