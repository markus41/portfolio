import json
import sys
import types
from pathlib import Path

from src.team_orchestrator import TeamOrchestrator
from src.agents.base_agent import BaseAgent


class FooAgent(BaseAgent):
    skills = ["foo", "common"]

    def run(self, payload):
        return {"agent": "foo", **payload}


class BarAgent(BaseAgent):
    skills = ["bar", "common"]

    def run(self, payload):
        return {"agent": "bar", **payload}


def _write_team(tmp_path: Path) -> Path:
    cfg = {
        "config": {
            "participants": [
                {"config": {"name": "foo_agent"}},
                {"config": {"name": "bar_agent"}},
            ]
        }
    }
    path = tmp_path / "team.json"
    path.write_text(json.dumps(cfg))
    return path


def test_delegate_by_skill(tmp_path):
    team_cfg = _write_team(tmp_path)
    mod1 = types.ModuleType("src.agents.foo_agent")
    mod1.FooAgent = FooAgent
    sys.modules["src.agents.foo_agent"] = mod1
    mod2 = types.ModuleType("src.agents.bar_agent")
    mod2.BarAgent = BarAgent
    sys.modules["src.agents.bar_agent"] = mod2

    orch = TeamOrchestrator(str(team_cfg))

    res = orch.delegate_by_skill_sync("bar", {"val": 1})
    assert res["result"]["agent"] == "bar"

    res2 = orch.delegate_by_skill_sync("foo", {"val": 2})
    assert res2["result"]["agent"] == "foo"


def test_delegate_unknown_skill(tmp_path):
    team_cfg = _write_team(tmp_path)
    mod = types.ModuleType("src.agents.foo_agent")
    mod.FooAgent = FooAgent
    sys.modules["src.agents.foo_agent"] = mod
    mod2 = types.ModuleType("src.agents.bar_agent")
    mod2.BarAgent = BarAgent
    sys.modules["src.agents.bar_agent"] = mod2

    orch = TeamOrchestrator(str(team_cfg))

    res = orch.delegate_by_skill_sync("missing", {"v": 3})
    assert res["status"] == "unhandled"
