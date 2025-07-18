import json
import types
import sys
from pathlib import Path

import pytest

from src.team_orchestrator import TeamOrchestrator
from src.agents.base_agent import BaseAgent


class DummyAgent(BaseAgent):
    def run(self, payload):
        return payload


def _write_team(tmp_path: Path, model_ref: str) -> Path:
    cfg = {
        "provider": "autogen.agentchat.teams.RoundRobinGroupChat",
        "config": {
            "participants": [
                {
                    "config": {
                        "name": "dummy_agent",
                        "model_client": {"config": {"model": model_ref}},
                    }
                }
            ]
        },
    }
    path = tmp_path / "team.json"
    path.write_text(json.dumps(cfg))
    return path


def test_model_policy_resolution(tmp_path: Path):
    team_cfg = _write_team(tmp_path, "$tier.premium")
    policy_path = tmp_path / "policy.json"
    policy_path.write_text(json.dumps({"cheap": "a", "balanced": "b", "premium": "c"}))

    mod = types.ModuleType("src.agents.dummy_agent")
    mod.DummyAgent = DummyAgent
    sys.modules["src.agents.dummy_agent"] = mod

    orch = TeamOrchestrator(str(team_cfg), policy_path=str(policy_path))
    model = orch.team_config["config"]["participants"][0]["config"]["model_client"][
        "config"
    ]["model"]
    assert model == "c"


def test_unknown_model_tier(tmp_path: Path):
    team_cfg = _write_team(tmp_path, "$tier.ultra")
    policy_path = tmp_path / "policy.json"
    policy_path.write_text(json.dumps({"cheap": "a"}))

    mod = types.ModuleType("src.agents.dummy_agent")
    mod.DummyAgent = DummyAgent
    sys.modules["src.agents.dummy_agent"] = mod

    with pytest.raises(ValueError):
        TeamOrchestrator(str(team_cfg), policy_path=str(policy_path))
