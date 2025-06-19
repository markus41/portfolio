import types
import sys

import pytest

from src.orchestrator import Orchestrator


def test_orchestrator_file_backend(tmp_path, monkeypatch):
    class DummyScheduler:
        def create_event(self, cid, ev):
            return {"id": "evt"}

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

    mem_file = tmp_path / "events.jsonl"
    orch = Orchestrator(
        memory_endpoint="http://unused",
        memory_backend="file",
        memory_file=str(mem_file),
    )

    payload = {"form_data": {}, "source": "web"}
    res = orch.handle_event_sync({"type": "lead_capture", "payload": payload})
    assert res["status"] == "done"

    # ensure event persisted to file
    contents = mem_file.read_text().strip().splitlines()
    assert len(contents) == 1
    assert "lead_capture" in contents[0]
