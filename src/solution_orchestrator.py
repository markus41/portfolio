"""Orchestrator managing multiple agent teams."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from .team_orchestrator import TeamOrchestrator


class SolutionOrchestrator:
    """Route events across a registry of :class:`TeamOrchestrator`."""

    def __init__(self, team_configs: Dict[str, str]):
        """Initialise orchestrator with ``team_configs`` mapping names to JSON."""
        self.teams = {name: TeamOrchestrator(Path(path)) for name, path in team_configs.items()}
        self.history: list[dict] = []
        self.status: Dict[str, str] = {}

    def handle_event(self, team: str, event: Dict[str, Any]) -> Dict[str, Any]:
        """Forward ``event`` to ``team`` and record the result."""
        orchestrator = self.teams.get(team)
        if not orchestrator:
            return {"status": "unknown_team"}
        result = orchestrator.handle_event(event)
        self.history.append({"team": team, "event": event, "result": result})
        return result

    def report_status(self, team: str, state: str) -> None:
        """Store status updates from team orchestrators."""
        self.status[team] = state

    def get_status(self, team: str) -> str | None:
        """Return last reported status for ``team`` if available."""
        return self.status.get(team)
