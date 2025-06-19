"""Agent responsible for executing goal-based task plans."""

from __future__ import annotations

from typing import Any, Dict, List, TYPE_CHECKING

from .base_agent import BaseAgent
from ..utils.logger import get_logger

if TYPE_CHECKING:  # pragma: no cover - for type hints only
    from ..solution_orchestrator import SolutionOrchestrator

logger = get_logger(__name__)


class PlannerAgent(BaseAgent):
    """Sequence events across teams to accomplish high level goals.

    Parameters
    ----------
    orchestrator:
        :class:`~src.solution_orchestrator.SolutionOrchestrator` used to dispatch
        events.
    plans:
        Mapping of goal names to ordered lists of tasks. Each task must include a
        ``team`` key identifying the target team and an ``event`` dictionary
        compatible with :meth:`SolutionOrchestrator.handle_event_sync`.
    """

    def __init__(
        self,
        orchestrator: SolutionOrchestrator,
        plans: Dict[str, List[Dict[str, Any]]],
    ) -> None:
        self.orchestrator = orchestrator
        self.plans = plans

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the task sequence for ``payload['goal']``.

        Returns a dictionary with the results of each task. If the goal is not
        known ``{"status": "unknown_goal"}`` is returned.
        """
        goal = str(payload.get("goal", ""))
        tasks = self.plans.get(goal)
        if not tasks:
            logger.warning("Planner received unknown goal '%s'", goal)
            return {"status": "unknown_goal"}

        results = []
        for idx, task in enumerate(tasks):
            team = task.get("team")
            event = task.get("event", {})
            logger.info("Planner executing step %s for team %s", idx + 1, team)
            res = self.orchestrator.handle_event_sync(team, event)
            results.append({"team": team, "result": res})
        return {"status": "complete", "results": results}
