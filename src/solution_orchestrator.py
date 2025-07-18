"""Orchestrator managing multiple agent teams."""

from __future__ import annotations

from pathlib import Path
from collections import defaultdict
from typing import Any, Dict, List, Optional
import asyncio
from .utils import ActivityLogger

from . import db

from .agents.planner_agent import PlannerAgent
from .workflows.graph import GraphWorkflowDefinition, GraphWorkflowEngine

from .team_orchestrator import TeamOrchestrator


class SolutionOrchestrator:
    """Route events across a registry of :class:`TeamOrchestrator`.

    Parameters
    ----------
    team_configs:
        Mapping of team names to JSON configuration files.
    planner_plans:
        Optional mapping used by :class:`PlannerAgent` to execute goal driven
        workflows.
    persist_history:
        If ``True`` processed events are written to the SQLite history database
        via :mod:`src.db`.
    """

    def __init__(
        self,
        team_configs: Dict[str, str],
        planner_plans: Optional[Dict[str, List[Dict[str, Any]]]] = None,
        log_path: str | None = None,
        persist_history: bool = True,
    ) -> None:
        self.teams = {
            name: TeamOrchestrator(Path(path)) for name, path in team_configs.items()
        }
        self.history: list[dict] = []
        self.status: Dict[str, str] = {}
        self._subscribers: dict[str, list[asyncio.Queue]] = defaultdict(list)
        self.planner: Optional[PlannerAgent] = None
        self.activity_logger = ActivityLogger(log_path) if log_path else None
        self.persist_history = persist_history
        if planner_plans is not None:
            self.planner = PlannerAgent(self, planner_plans)

    def subscribe(self, team: str) -> asyncio.Queue:
        """Return a queue receiving streaming updates for ``team``."""

        queue: asyncio.Queue = asyncio.Queue()
        self._subscribers[team].append(queue)
        return queue

    def unsubscribe(self, team: str, queue: asyncio.Queue) -> None:
        """Remove ``queue`` from the subscriber list for ``team``."""

        if queue in self._subscribers.get(team, []):
            self._subscribers[team].remove(queue)

    def _publish(self, team: str, message: dict) -> None:
        """Send ``message`` to all queues subscribed to ``team``."""

        for q in list(self._subscribers.get(team, [])):
            try:
                q.put_nowait(message)
            except asyncio.QueueFull:  # pragma: no cover - unlikely
                pass

    async def handle_event(self, team: str, event: Dict[str, Any]) -> Dict[str, Any]:
        """Forward ``event`` to ``team`` and record the result."""
        orchestrator = self.teams.get(team)
        if not orchestrator:
            return {"status": "unknown_team"}
        result = await orchestrator.handle_event(event)
        self.history.append({"team": team, "event": event, "result": result})

        if self.persist_history:
            db.insert_event(
                team,
                str(event.get("type")),
                event.get("payload", {}),
                result,
            )

        if self.activity_logger:
            agent_id = str(event.get("type", "unknown"))
            summary = str(result.get("result", result))
            self.activity_logger.log(agent_id, summary)

        self._publish(team, {"type": "activity", "event": event, "result": result})

        return result

    def handle_event_sync(self, team: str, event: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous wrapper around :meth:`handle_event`."""
        from agentic_core import run_sync

        return run_sync(self.handle_event(team, event))

    def report_status(self, team: str, state: str) -> None:
        """Store status updates from team orchestrators."""
        self.status[team] = state
        self._publish(team, {"type": "status", "status": state})

    def get_status(self, team: str) -> str | None:
        """Return last reported status for ``team`` if available."""
        return self.status.get(team)

    def get_recent_activity(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Return the most recent activity log entries."""
        if not self.activity_logger:
            return []
        return self.activity_logger.tail(limit)

    def execute_goal(self, goal: str) -> Dict[str, Any]:
        """Run the planner for the given ``goal``.

        Raises
        ------
        RuntimeError
            If the orchestrator was initialised without a planner.
        """

        if not self.planner:
            raise RuntimeError("Planner is not configured")
        return self.planner.run({"goal": goal})

    def execute_workflow(
        self, workflow: str | Path | GraphWorkflowDefinition
    ) -> Dict[str, Any]:
        """Execute a graph workflow definition.

        ``workflow`` may be a path to a JSON file or a pre-loaded
        :class:`GraphWorkflowDefinition` instance. Each node ``config`` must
        include ``team`` and ``event`` fields which are forwarded to
        :meth:`handle_event_sync`.
        """

        if isinstance(workflow, (str, Path)):
            definition = GraphWorkflowDefinition.from_file(workflow)
        else:
            definition = workflow

        engine = GraphWorkflowEngine(definition)
        return engine.run(self)

    # ------------------------------------------------------------------
    # Async context manager implementation
    # ------------------------------------------------------------------
    async def __aenter__(self) -> "SolutionOrchestrator":
        """Return ``self`` so the orchestrator can be used with ``async with``."""

        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        """Release resources such as async memory services on shutdown."""

        for team in self.teams.values():
            mem = getattr(team, "memory", None)
            if hasattr(mem, "aclose"):
                await mem.aclose()
