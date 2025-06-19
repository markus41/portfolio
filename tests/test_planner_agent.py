import json
import sys
import types
from pathlib import Path

import pytest

from src.solution_orchestrator import SolutionOrchestrator
from src.agents.base_agent import BaseAgent


class DummyAgentA(BaseAgent):
    def run(self, payload):
        return {"handled_by": "A", **payload}


class DummyAgentB(BaseAgent):
    def run(self, payload):
        return {"handled_by": "B", **payload}


def _write_team(tmp_path: Path, agent_name: str) -> Path:
    cfg = {
        "responsibilities": [agent_name],
        "config": {"participants": [{"config": {"name": agent_name}}]},
    }
    path = tmp_path / f"{agent_name}.json"
    path.write_text(json.dumps(cfg))
    return path


def _register_agents():
    mod_a = types.ModuleType("src.agents.dummy_agent_a")
    mod_a.DummyAgentA = DummyAgentA
    sys.modules["src.agents.dummy_agent_a"] = mod_a

    mod_b = types.ModuleType("src.agents.dummy_agent_b")
    mod_b.DummyAgentB = DummyAgentB
    sys.modules["src.agents.dummy_agent_b"] = mod_b


def test_execute_goal(tmp_path):
    _register_agents()
    team_a = _write_team(tmp_path, "dummy_agent_a")
    team_b = _write_team(tmp_path, "dummy_agent_b")

    plans = {
        "demo": [
            {"team": "A", "event": {"type": "dummy_agent_a", "payload": {"foo": 1}}},
            {"team": "B", "event": {"type": "dummy_agent_b", "payload": {"bar": 2}}},
        ]
    }

    orch = SolutionOrchestrator({"A": str(team_a), "B": str(team_b)}, planner_plans=plans)

    result = orch.execute_goal("demo")
    assert result["status"] == "complete"
    assert result["results"][0]["result"]["result"]["handled_by"] == "A"
    assert result["results"][1]["result"]["result"]["handled_by"] == "B"


def test_missing_goal(tmp_path):
    _register_agents()
    team_a = _write_team(tmp_path, "dummy_agent_a")
    orch = SolutionOrchestrator({"A": str(team_a)}, planner_plans={})

    result = orch.execute_goal("missing")
    assert result["status"] == "unknown_goal"


def test_dry_run(tmp_path, monkeypatch):
    _register_agents()
    team_a = _write_team(tmp_path, "dummy_agent_a")
    team_b = _write_team(tmp_path, "dummy_agent_b")

    plans = {
        "demo": [
            {"team": "A", "event": {"type": "dummy_agent_a", "payload": {"foo": 1}}},
            {"team": "B", "event": {"type": "dummy_agent_b", "payload": {"bar": 2}}},
        ]
    }

    orch = SolutionOrchestrator({"A": str(team_a), "B": str(team_b)}, planner_plans=plans)

    called: list[tuple[str, dict]] = []

    def fake_handle(team: str, event: dict) -> dict:
        called.append((team, event))
        return {}

    monkeypatch.setattr(orch, "handle_event_sync", fake_handle)

    result = orch.execute_goal("demo", dry_run=True)

    assert called == []
    assert result["status"] == "planned"
    assert result["sequence"] == [
        {"team": "A", "event": "dummy_agent_a"},
        {"team": "B", "event": "dummy_agent_b"},
    ]
