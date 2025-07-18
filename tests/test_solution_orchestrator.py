import json
import sys
import types
import asyncio
from pathlib import Path

import pytest

from src.solution_orchestrator import SolutionOrchestrator
from src.agents.base_agent import BaseAgent
from src import db


class DummyAgentA(BaseAgent):
    def run(self, payload):
        return {"handled_by": "A", **payload}


class DummyAgentB(BaseAgent):
    def run(self, payload):
        return {"handled_by": "B", **payload}


def _write_team(tmp_path: Path, agent_name: str) -> Path:
    config = {
        "provider": "autogen.agentchat.teams.RoundRobinGroupChat",
        "responsibilities": [agent_name],
        "config": {"participants": [{"config": {"name": agent_name}}]},
    }
    team_file = tmp_path / f"{agent_name}.json"
    team_file.write_text(json.dumps(config))
    return team_file


def test_solution_orchestrator_routing(tmp_path, monkeypatch):
    team_a = _write_team(tmp_path, "dummy_agent_a")
    team_b = _write_team(tmp_path, "dummy_agent_b")

    mod_a = types.ModuleType("src.agents.dummy_agent_a")
    mod_a.DummyAgentA = DummyAgentA
    sys.modules["src.agents.dummy_agent_a"] = mod_a

    mod_b = types.ModuleType("src.agents.dummy_agent_b")
    mod_b.DummyAgentB = DummyAgentB
    sys.modules["src.agents.dummy_agent_b"] = mod_b

    orch = SolutionOrchestrator({"A": str(team_a), "B": str(team_b)})

    out_a = orch.handle_event_sync(
        "A", {"type": "dummy_agent_a", "payload": {"foo": 1}}
    )
    out_b = orch.handle_event_sync(
        "B", {"type": "dummy_agent_b", "payload": {"bar": 2}}
    )

    assert out_a["result"]["handled_by"] == "A"
    assert out_b["result"]["handled_by"] == "B"
    assert orch.history[0]["team"] == "A"
    assert orch.history[1]["team"] == "B"


def test_solution_orchestrator_logging(tmp_path, monkeypatch):
    team = _write_team(tmp_path, "dummy_agent_a")

    mod_a = types.ModuleType("src.agents.dummy_agent_a")
    mod_a.DummyAgentA = DummyAgentA
    sys.modules["src.agents.dummy_agent_a"] = mod_a

    log_path = tmp_path / "activity.jsonl"
    orch = SolutionOrchestrator({"A": str(team)}, log_path=str(log_path))

    orch.handle_event_sync("A", {"type": "dummy_agent_a", "payload": {"x": 1}})

    entries = orch.get_recent_activity()
    assert len(entries) == 1
    assert entries[0]["agent_id"] == "dummy_agent_a"
    assert "timestamp" in entries[0]


def test_solution_orchestrator_concurrent(tmp_path):
    team_a = _write_team(tmp_path, "dummy_agent_a")
    team_b = _write_team(tmp_path, "dummy_agent_b")

    mod_a = types.ModuleType("src.agents.dummy_agent_a")
    mod_a.DummyAgentA = DummyAgentA
    sys.modules["src.agents.dummy_agent_a"] = mod_a

    mod_b = types.ModuleType("src.agents.dummy_agent_b")
    mod_b.DummyAgentB = DummyAgentB
    sys.modules["src.agents.dummy_agent_b"] = mod_b

    orch = SolutionOrchestrator({"A": str(team_a), "B": str(team_b)})

    async def _run():
        return await asyncio.gather(
            orch.handle_event("A", {"type": "dummy_agent_a", "payload": {"v": 1}}),
            orch.handle_event("B", {"type": "dummy_agent_b", "payload": {"v": 2}}),
        )

    res_a, res_b = asyncio.run(_run())

    assert res_a["result"]["handled_by"] == "A"
    assert res_b["result"]["handled_by"] == "B"


def test_add_and_remove_team(tmp_path):
    team = _write_team(tmp_path, "dummy_agent_a")

    db.init_db()

    mod_a = types.ModuleType("src.agents.dummy_agent_a")
    mod_a.DummyAgentA = DummyAgentA
    sys.modules["src.agents.dummy_agent_a"] = mod_a

    orch = SolutionOrchestrator({})
    orch.add_team("demo", str(team))
    assert "demo" in orch.teams

    with pytest.raises(ValueError):
        orch.add_team("demo", str(team))

    out = orch.handle_event_sync("demo", {"type": "dummy_agent_a"})
    assert out["result"]["handled_by"] == "A"

    orch.remove_team("demo")
    assert "demo" not in orch.teams

    with pytest.raises(ValueError):
        orch.remove_team("demo")

    out = orch.handle_event_sync("demo", {"type": "dummy_agent_a"})
    assert out["status"] == "unknown_team"
