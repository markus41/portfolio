import json
import sys
import types
import pytest
from pathlib import Path

from src.base_orchestrator import BaseOrchestrator
from src.team_orchestrator import TeamOrchestrator, validate_team_config
from src.agents.base_agent import BaseAgent


class DummyAgent(BaseAgent):
    def run(self, payload):
        return {"echo": payload}


def _write_team(tmp_path: Path) -> Path:
    cfg = {
        "provider": "autogen.agentchat.teams.RoundRobinGroupChat",
        "responsibilities": ["dummy_agent"],
        "config": {"participants": [{"config": {"name": "dummy_agent"}}]},
    }
    path = tmp_path / "team.json"
    path.write_text(json.dumps(cfg))
    return path


def test_team_orchestrator_inherits(tmp_path):
    team_cfg = _write_team(tmp_path)
    mod = types.ModuleType("src.agents.dummy_agent")
    mod.DummyAgent = DummyAgent
    sys.modules["src.agents.dummy_agent"] = mod

    orch = TeamOrchestrator(str(team_cfg))
    assert issubclass(TeamOrchestrator, BaseOrchestrator)
    assert orch.memory is None
    out = orch.handle_event_sync({"type": "dummy_agent", "payload": {"foo": 1}})
    assert out["result"]["echo"]["foo"] == 1


def test_team_orchestrator_responsibility_check(tmp_path):
    cfg = {
        "responsibilities": ["other_agent"],
        "config": {"participants": [{"config": {"name": "dummy_agent"}}]},
    }
    path = tmp_path / "team.json"
    path.write_text(json.dumps(cfg))

    mod = types.ModuleType("src.agents.dummy_agent")
    mod.DummyAgent = DummyAgent
    sys.modules["src.agents.dummy_agent"] = mod

    with pytest.raises(ValueError):
        TeamOrchestrator(str(path))


def test_validate_team_config(tmp_path):
    valid = {
        "provider": "autogen.agentchat.teams.RoundRobinGroupChat",
        "config": {"participants": [{"config": {"name": "dummy"}}]},
    }
    validate_team_config(valid)

    invalid = {}
    with pytest.raises(Exception):
        validate_team_config(invalid)


def test_team_orchestrator_schema_failure(tmp_path):
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{}")
    with pytest.raises(ValueError):
        TeamOrchestrator(str(bad_file))
