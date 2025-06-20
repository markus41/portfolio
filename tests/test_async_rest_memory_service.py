import sys
import tests.httpx_stub as httpx

sys.modules.setdefault("httpx", httpx)

from src.memory_service.rest_async import AsyncRestMemoryService
from agentic_core import run_sync


def test_store_and_fetch(monkeypatch):
    """Verify AsyncRestMemoryService uses httpx.AsyncClient correctly."""

    events = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/store":
            events["method"] = request.method
            events["json"] = request.json()
            return httpx.Response(200)
        if request.url.path == "/fetch":
            return httpx.Response(200, json=[{"foo": 1}])
        return httpx.Response(404)

    transport = httpx.MockTransport(handler)
    client = httpx.AsyncClient(transport=transport, base_url="http://x")
    svc = AsyncRestMemoryService("http://x", client=client)

    assert run_sync(svc.store("a", {"foo": 1})) is True
    assert events == {"method": "POST", "json": {"key": "a", "data": {"foo": 1}}}

    res = run_sync(svc.fetch("a", 5))
    assert res == [{"foo": 1}]

    client.close()
