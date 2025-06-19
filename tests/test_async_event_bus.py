import asyncio
from agentic_core import AsyncEventBus


def test_async_event_bus_publish():
    bus = AsyncEventBus()
    called = []

    async def handler(payload):
        await asyncio.sleep(0.01)
        called.append(payload)

    async def main():
        bus.subscribe("t", handler)
        await bus.publish("t", {"x": 1})

    asyncio.run(main())
    assert called == [{"x": 1}]
