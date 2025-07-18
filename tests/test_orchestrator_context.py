import asyncio
import sys
import types
from pathlib import Path
from typing import Any, Dict, List

import pytest

sys.modules.setdefault(
    "requests",
    types.SimpleNamespace(
        post=lambda *a, **k: types.SimpleNamespace(ok=True, json=lambda: {}),
        get=lambda *a, **k: types.SimpleNamespace(ok=True, json=lambda: {}),
    ),
)

from src.orchestrator import Orchestrator
from src.memory_service.base import BaseMemoryService
from src.solution_orchestrator import SolutionOrchestrator


class _SyncMem(BaseMemoryService):
    def __init__(self, flag: Dict[str, bool]):
        self.flag = flag

    def store(self, key: str, payload: Dict[str, Any]) -> bool:
        return True

    def fetch(self, key: str, top_k: int = 5) -> List[Dict[str, Any]]:
        return []

    def close(self) -> None:
        self.flag["closed"] = True


class _AsyncMem(BaseMemoryService):
    def __init__(self, flag: Dict[str, bool]):
        self.flag = flag

    async def store(self, key: str, payload: Dict[str, Any]) -> bool:
        return True

    async def fetch(self, key: str, top_k: int = 5) -> List[Dict[str, Any]]:
        return []

    async def aclose(self) -> None:
        self.flag["closed"] = True


def test_orchestrator_context_manager(monkeypatch):
    flag = {"closed": False}
    monkeypatch.setattr(
        "src.tools.scheduler_tool.SchedulerTool",
        lambda: types.SimpleNamespace(create_event=lambda cid, ev: {"id": "evt"}),
    )
    monkeypatch.setattr("src.orchestrator.RestMemoryService", lambda e: _SyncMem(flag))
    with Orchestrator("http://m") as orch:
        assert isinstance(orch.memory, _SyncMem)
    assert flag["closed"] is True


def test_orchestrator_async_context_manager(monkeypatch):
    flag = {"closed": False}
    monkeypatch.setattr(
        "src.tools.scheduler_tool.SchedulerTool",
        lambda: types.SimpleNamespace(create_event=lambda cid, ev: {"id": "evt"}),
    )
    monkeypatch.setattr(
        "src.orchestrator.AsyncRestMemoryService", lambda e: _AsyncMem(flag)
    )
    async def main():
        async with Orchestrator(memory_backend="rest_async", memory_endpoint="http://m") as orch:
            assert isinstance(orch.memory, _AsyncMem)

    asyncio.run(main())
    assert flag["closed"] is True


class _Team:
    def __init__(self, path: str) -> None:
        self.flag = {}

    async def handle_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        return {}

    def close(self) -> None:
        self.flag["closed"] = True


class _AsyncTeam(_Team):
    async def aclose(self) -> None:
        self.flag["closed"] = True


def test_solution_orchestrator_context_manager(monkeypatch, tmp_path: Path) -> None:
    path = tmp_path / "team.json"
    path.write_text("{}")
    closed = {}

    monkeypatch.setattr(
        "src.tools.scheduler_tool.SchedulerTool",
        lambda: types.SimpleNamespace(create_event=lambda cid, ev: {"id": "evt"}),
    )

    def factory(p: Path) -> _Team:
        team = _Team(str(p))
        team.flag = closed
        return team

    monkeypatch.setattr("src.solution_orchestrator.TeamOrchestrator", factory)
    with SolutionOrchestrator({"demo": str(path)}) as orch:
        assert "demo" in orch.teams
    assert closed.get("closed") is True


def test_solution_orchestrator_async_context_manager(monkeypatch, tmp_path: Path) -> None:
    path = tmp_path / "team.json"
    path.write_text("{}")
    closed = {}

    monkeypatch.setattr(
        "src.tools.scheduler_tool.SchedulerTool",
        lambda: types.SimpleNamespace(create_event=lambda cid, ev: {"id": "evt"}),
    )

    def factory(p: Path) -> _AsyncTeam:
        team = _AsyncTeam(str(p))
        team.flag = closed
        return team

    monkeypatch.setattr("src.solution_orchestrator.TeamOrchestrator", factory)

    async def main():
        async with SolutionOrchestrator({"demo": str(path)}) as orch:
            assert "demo" in orch.teams

    asyncio.run(main())
    assert closed.get("closed") is True
