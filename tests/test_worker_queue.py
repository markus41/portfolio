import asyncio
import json
import sys
import types
import asyncio
from pathlib import Path

from src.solution_orchestrator import SolutionOrchestrator
from src.agents.base_agent import BaseAgent


class SlowAgent(BaseAgent):
    async def run(self, payload):
        await asyncio.sleep(0.01)
        return payload


def _write_team(tmp_path: Path) -> Path:
    cfg = {
        "provider": "autogen.agentchat.teams.RoundRobinGroupChat",
        "responsibilities": ["slow_agent"],
        "config": {"participants": [{"config": {"name": "slow_agent"}}]},
    }
    path = tmp_path / "team.json"
    path.write_text(json.dumps(cfg))
    return path


def test_queue_limits_concurrency(tmp_path):
    team_cfg = _write_team(tmp_path)
    mod = types.ModuleType("src.agents.slow_agent")
    mod.SlowAgent = SlowAgent
    sys.modules["src.agents.slow_agent"] = mod

    orch = SolutionOrchestrator({"demo": str(team_cfg)}, max_workers=2)

    active = 0
    max_seen = 0
    lock = asyncio.Lock()

    original_run = SlowAgent.run

    async def wrapped(self, payload):
        nonlocal active, max_seen
        async with lock:
            active += 1
            if active > max_seen:
                max_seen = active
        try:
            return await original_run(self, payload)
        finally:
            async with lock:
                active -= 1

    SlowAgent.run = wrapped

    async def _run():
        return await asyncio.gather(
            *[
                orch.enqueue_event("demo", {"type": "slow_agent", "payload": {"i": i}})
                for i in range(5)
            ]
        )

    results = asyncio.run(_run())

    assert len(results) == 5
    assert max_seen <= 2

