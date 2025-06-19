import json
import sys
import types
from pathlib import Path

import pytest

from src.solution_orchestrator import SolutionOrchestrator
from src.markdown_tasks import load_goals_from_markdown
from src.agents.base_agent import BaseAgent


class DummyA(BaseAgent):
    def run(self, payload):
        return {"handled_by": "A", **payload}


class DummyB(BaseAgent):
    def run(self, payload):
        return {"handled_by": "B", **payload}


def _register_agents():
    mod_a = types.ModuleType("src.agents.dummy_a")
    mod_a.DummyA = DummyA
    sys.modules["src.agents.dummy_a"] = mod_a

    mod_b = types.ModuleType("src.agents.dummy_b")
    mod_b.DummyB = DummyB
    sys.modules["src.agents.dummy_b"] = mod_b


def _write_team(tmp_path: Path, agent_name: str) -> Path:
    cfg = {
        "responsibilities": [agent_name],
        "config": {"participants": [{"config": {"name": agent_name}}]},
    }
    path = tmp_path / f"{agent_name}.json"
    path.write_text(json.dumps(cfg))
    return path


def test_load_goals_from_markdown(tmp_path):
    md = tmp_path / "tasks.md"
    md.write_text(
        "\n".join(
            [
                "## Goal: demo",
                "- {\"team\": \"A\", \"event\": {\"type\": \"dummy_a\", \"payload\": {\"x\": 1}}}",
                "- {\"team\": \"B\", \"event\": {\"type\": \"dummy_b\", \"payload\": {\"y\": 2}}}",
            ]
        )
    )
    plans = load_goals_from_markdown(md)
    assert list(plans) == ["demo"]
    assert plans["demo"][0]["team"] == "A"


def test_run_markdown_plan(tmp_path):
    _register_agents()
    md = tmp_path / "tasks.md"
    md.write_text(
        "\n".join(
            [
                "## Goal: demo",
                "- {\"team\": \"A\", \"event\": {\"type\": \"dummy_a\", \"payload\": {}}}",
                "- {\"team\": \"B\", \"event\": {\"type\": \"dummy_b\", \"payload\": {}}}",
            ]
        )
    )
    team_a = _write_team(tmp_path, "dummy_a")
    team_b = _write_team(tmp_path, "dummy_b")
    plans = load_goals_from_markdown(md)
    orch = SolutionOrchestrator({"A": str(team_a), "B": str(team_b)}, planner_plans=plans)
    res = orch.execute_goal("demo")
    assert res["status"] == "complete"
    assert res["results"][0]["result"]["result"]["handled_by"] == "A"
    assert res["results"][1]["result"]["result"]["handled_by"] == "B"
