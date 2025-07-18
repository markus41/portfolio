"""Orchestrator managing multiple agent teams."""

from __future__ import annotations

from pathlib import Path
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple
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
    max_workers:
        Number of background worker tasks processing events concurrently.
    """

    def __init__(
        self,
        team_configs: Dict[str, str],
        planner_plans: Optional[Dict[str, List[Dict[str, Any]]]] = None,
        log_path: str | None = None,
        persist_history: bool = True,
        *,
        max_workers: int = 5,
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
        self._queue: asyncio.Queue[
            Tuple[str, Dict[str, Any], asyncio.Future]
        ] = asyncio.Queue()
        self._workers: list[asyncio.Task] = []
        self._max_workers = max_workers
        self._workers_started = False
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

    def _start_workers(self) -> None:
        """Launch background tasks consuming the internal event queue."""

        if self._workers_started:
            return
        self._workers_started = True
        for _ in range(self._max_workers):
            self._workers.append(asyncio.create_task(self._worker_loop()))

    async def _worker_loop(self) -> None:
        """Process queued events sequentially inside each worker."""

        while True:
            team, event, fut = await self._queue.get()
            try:
                result = await self.handle_event(team, event)
            except Exception as exc:  # pragma: no cover - defensive
                result = {"error": str(exc)}
            if not fut.cancelled():
                fut.set_result(result)
            self._queue.task_done()

    async def enqueue_event(self, team: str, event: Dict[str, Any]) -> Dict[str, Any]:
        """Add ``event`` to the processing queue and wait for the result."""

        self._start_workers()
        fut: asyncio.Future = asyncio.get_running_loop().create_future()
        await self._queue.put((team, event, fut))
        return await fut

    async def shutdown(self) -> None:
        """Cancel worker tasks and wait for termination."""

        for t in self._workers:
            t.cancel()
        for t in self._workers:
            try:
                await t
            except asyncio.CancelledError:  # pragma: no cover - graceful shutdown
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
