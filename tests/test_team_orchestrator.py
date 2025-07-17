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


def _write_team(tmp_path: Path, ext: str = "json") -> Path:
    """Write a minimal team configuration to ``tmp_path`` with *ext*."""

    cfg = {
        "provider": "autogen.agentchat.teams.RoundRobinGroupChat",
        "responsibilities": ["dummy_agent"],
        "config": {"participants": [{"config": {"name": "dummy_agent"}}]},
    }
    path = tmp_path / f"team.{ext}"
    if ext == "json":
        path.write_text(json.dumps(cfg))
    else:
        yaml = pytest.importorskip("yaml")
        path.write_text(yaml.safe_dump(cfg))
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


def test_yaml_and_json_equivalent(tmp_path):
    """YAML and JSON team configs should produce identical orchestrators."""

    yaml = pytest.importorskip("yaml")

    json_cfg = _write_team(tmp_path, "json")
    yaml_cfg = _write_team(tmp_path, "yaml")

    mod = types.ModuleType("src.agents.dummy_agent")
    mod.DummyAgent = DummyAgent
    sys.modules["src.agents.dummy_agent"] = mod

    orch_json = TeamOrchestrator(str(json_cfg))
    orch_yaml = TeamOrchestrator(str(yaml_cfg))

    assert orch_json.team_config == orch_yaml.team_config
    assert list(orch_json.agents.keys()) == list(orch_yaml.agents.keys())
