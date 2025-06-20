import sys
import tests.httpx_stub as httpx

sys.modules.setdefault("httpx", httpx)

import types

from src.orchestrator import Orchestrator
from src.memory_service.rest_async import AsyncRestMemoryService


class DummyScheduler:
    def create_event(self, cid, ev):
        return {"id": "evt"}


def test_orchestrator_rest_async_backend(monkeypatch):
    """Ensure orchestrator uses AsyncRestMemoryService when configured."""
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

    async def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/store":
            return httpx.Response(200)
        return httpx.Response(200, json=[])

    transport = httpx.MockTransport(handler)
    client = httpx.AsyncClient(transport=transport, base_url="http://mem")

    # patch constructor to inject custom client
    def factory(endpoint: str):
        return AsyncRestMemoryService(endpoint, client=client)

    monkeypatch.setattr("src.orchestrator.AsyncRestMemoryService", factory)

    orch = Orchestrator(memory_backend="rest_async", memory_endpoint="http://mem")

    payload = {"form_data": {}, "source": "web"}
    res = orch.handle_event_sync({"type": "lead_capture", "payload": payload})
    assert res["status"] == "done"

    client.close()
