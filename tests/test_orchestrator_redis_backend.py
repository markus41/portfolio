import types
import sys

from src.orchestrator import Orchestrator
from src.memory_service.redis import redis as redis_module


class DummyRedis:
    def __init__(self):
        self.store = {}

    def rpush(self, key, value):
        self.store.setdefault(key, []).append(value)

    def lrange(self, key, start, end):
        data = self.store.get(key, [])
        if start < 0:
            start = len(data) + start
        if end == -1:
            end = None
        else:
            end += 1
        return data[start:end]

    def ping(self):
        return True


def test_orchestrator_redis_backend(monkeypatch):
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

    client = DummyRedis()
    monkeypatch.setattr(redis_module.Redis, "from_url", lambda *a, **k: client)
    monkeypatch.setenv("MEMORY_REDIS_URL", "redis://localhost")

    orch = Orchestrator(memory_backend="redis")

    payload = {"form_data": {}, "source": "web"}
    res = orch.handle_event_sync({"type": "lead_capture", "payload": payload})
    assert res["status"] == "done"

    assert len(client.store.get("lead_capture", [])) == 1
