import asyncio

from src.base_orchestrator import BaseOrchestrator
from src.memory_service.async_base import AsyncBaseMemoryService


class DummyAsyncMemory(AsyncBaseMemoryService):
    """Minimal async memory service used to test orchestrator integration."""

    def __init__(self):
        self.stored = False
        self.closed = False

    async def store(self, key: str, payload: dict) -> bool:
        await asyncio.sleep(0)  # ensure coroutine execution
        self.stored = True
        return True

    async def fetch(self, key: str, top_k: int = 5):  # pragma: no cover - unused
        return []

    async def aclose(self) -> None:
        self.closed = True


def test_async_memory_usage() -> None:
    mem = DummyAsyncMemory()
    orch = BaseOrchestrator(memory=mem)

    res = orch.handle_event_sync({"type": "missing", "payload": {}})
    # event type is unknown but store should have been awaited
    assert res["status"] == "ignored"
    assert mem.stored is True

    async def _run():
        async with orch:
            pass

    asyncio.run(_run())
    assert mem.closed is True
