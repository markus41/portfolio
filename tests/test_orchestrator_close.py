import types
import sys

import pytest

from agentic_core import run_sync
from src.orchestrator import Orchestrator
from src.solution_orchestrator import SolutionOrchestrator
from src.memory_service.base import BaseMemoryService


class DummyAsyncMemory(BaseMemoryService):
    def __init__(self):
        self.closed = False

    async def store(self, key: str, payload: dict) -> bool:  # pragma: no cover - unused
        return True

    async def fetch(self, key: str, top_k: int = 5):  # pragma: no cover - unused
        return []

    async def aclose(self):
        self.closed = True


class DummyScheduler:
    def create_event(self, cid, ev):  # pragma: no cover - stub
        return {"id": "evt"}


@pytest.fixture
def dummy_memory(monkeypatch):
    memory = DummyAsyncMemory()
    monkeypatch.setattr(
        "src.orchestrator.AsyncRestMemoryService", lambda endpoint: memory
    )
    monkeypatch.setattr(
        "src.tools.scheduler_tool.SchedulerTool", lambda: DummyScheduler()
    )
    sys.modules.setdefault(
        "requests",
        types.SimpleNamespace(
            post=lambda *a, **k: types.SimpleNamespace(ok=True, json=lambda: {}),
            get=lambda *a, **k: types.SimpleNamespace(ok=True, json=lambda: {}),
        ),
    )
    return memory


def test_orchestrator_aclose_calls_memory(dummy_memory):
    orch = Orchestrator(memory_backend="rest_async", memory_endpoint="http://x")
    run_sync(orch.aclose())
    assert dummy_memory.closed is True


def test_orchestrator_close_sync(dummy_memory):
    orch = Orchestrator(memory_backend="rest_async", memory_endpoint="http://x")
    orch.close()
    assert dummy_memory.closed is True


def test_solution_orchestrator_aclose(monkeypatch):
    mem = DummyAsyncMemory()

    class DummyTeam:
        def __init__(self):
            self.memory = mem

        async def handle_event(self, event):  # pragma: no cover - unused
            return {}

    orch = SolutionOrchestrator({})
    orch.teams["demo"] = DummyTeam()
    run_sync(orch.aclose())
    assert mem.closed is True
