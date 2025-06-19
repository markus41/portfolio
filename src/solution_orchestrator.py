"""Orchestrator managing multiple agent teams."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional
from .utils import ActivityLogger

from .agents.planner_agent import PlannerAgent

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
    """

    def __init__(
        self,
        team_configs: Dict[str, str],
        planner_plans: Optional[Dict[str, List[Dict[str, Any]]]] = None,
        log_path: str | None = None,
    ) -> None:
        self.teams = {name: TeamOrchestrator(Path(path)) for name, path in team_configs.items()}
        self.history: list[dict] = []
        self.status: Dict[str, str] = {}
        self.planner: Optional[PlannerAgent] = None
        self.activity_logger = ActivityLogger(log_path) if log_path else None
        if planner_plans is not None:
            self.planner = PlannerAgent(self, planner_plans)

    async def handle_event(self, team: str, event: Dict[str, Any]) -> Dict[str, Any]:
        """Forward ``event`` to ``team`` and record the result."""
        orchestrator = self.teams.get(team)
        if not orchestrator:
            return {"status": "unknown_team"}
        result = await orchestrator.handle_event(event)
        self.history.append({"team": team, "event": event, "result": result})

        if self.activity_logger:
            agent_id = str(event.get("type", "unknown"))
            summary = str(result.get("result", result))
            self.activity_logger.log(agent_id, summary)

        return result

    def handle_event_sync(self, team: str, event: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous wrapper around :meth:`handle_event`."""
        from agentic_core import run_sync

        return run_sync(self.handle_event(team, event))

    def report_status(self, team: str, state: str) -> None:
        """Store status updates from team orchestrators."""
        self.status[team] = state

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
