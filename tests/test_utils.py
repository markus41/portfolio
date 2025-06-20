import asyncio

from agentic_core import run_maybe_async, run_sync


async def _async_add(a, b):
    await asyncio.sleep(0.01)
    return a + b


def _sync_add(a, b):
    return a + b


def test_run_maybe_async_handles_sync_and_async():
    async def main():
        async_result = await run_maybe_async(_async_add, 1, 2)
        sync_result = await run_maybe_async(_sync_add, 3, 4)
        assert async_result == 3
        assert sync_result == 7

    asyncio.run(main())


def test_run_sync_executes_async_function():
    async def coro():
        await asyncio.sleep(0.01)
        return "done"

    result = run_sync(coro())
    assert result == "done"
