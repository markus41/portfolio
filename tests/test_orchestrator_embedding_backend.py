import types
import sys

from src.orchestrator import Orchestrator
from src.memory_service.embedding import EmbeddingMemoryService


class DummyScheduler:
    def create_event(self, cid, ev):
        return {"id": "evt"}


def test_orchestrator_embedding_backend(monkeypatch):
    monkeypatch.setattr(
        "src.tools.scheduler_tool.SchedulerTool",
        lambda: DummyScheduler(),
    )
    sys.modules.setdefault(
        "requests",
        types.SimpleNamespace(
            post=lambda *a, **k: types.SimpleNamespace(ok=True, json=lambda: {}),
            get=lambda *a, **k: types.SimpleNamespace(ok=True, json=lambda: {}),
        ),
    )

    orch = Orchestrator(memory_backend="embedding")
    assert isinstance(orch.memory, EmbeddingMemoryService)

    payload = {"form_data": {}, "source": "web"}
    res = orch.handle_event_sync({"type": "lead_capture", "payload": payload})
    assert res["status"] == "done"
