import json
import sys
import types
from pathlib import Path

import pytest

from src.solution_orchestrator import SolutionOrchestrator
from src.agents.base_agent import BaseAgent
from src.workflows.graph import (
    GraphWorkflowDefinition,
    NodeDefinition,
    EdgeDefinition,
)


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
    path = tmp_path / f"{agent_name}.json"
    path.write_text(json.dumps(config))
    return path


def _register_agents():
    mod_a = types.ModuleType("src.agents.dummy_agent_a")
    mod_a.DummyAgentA = DummyAgentA
    sys.modules["src.agents.dummy_agent_a"] = mod_a

    mod_b = types.ModuleType("src.agents.dummy_agent_b")
    mod_b.DummyAgentB = DummyAgentB
    sys.modules["src.agents.dummy_agent_b"] = mod_b


def test_linear_graph_execution(tmp_path):
    _register_agents()
    team_a = _write_team(tmp_path, "dummy_agent_a")
    team_b = _write_team(tmp_path, "dummy_agent_b")

    orch = SolutionOrchestrator({"A": str(team_a), "B": str(team_b)})

    wf = GraphWorkflowDefinition(
        name="linear",
        nodes=[
            NodeDefinition(
                id="a",
                type="agent",
                label="A",
                config={
                    "team": "A",
                    "event": {"type": "dummy_agent_a", "payload": {"foo": 1}},
                },
            ),
            NodeDefinition(
                id="b",
                type="agent",
                label="B",
                config={
                    "team": "B",
                    "event": {"type": "dummy_agent_b", "payload": {"bar": 2}},
                },
            ),
        ],
        edges=[EdgeDefinition(source="a", target="b")],
    )

    result = orch.execute_workflow(wf)

    assert result["status"] == "complete"
    assert [r["team"] for r in result["results"]] == ["A", "B"]
    assert result["results"][0]["result"]["result"]["handled_by"] == "A"
    assert result["results"][1]["result"]["result"]["handled_by"] == "B"


def test_branching_graph_execution(tmp_path):
    _register_agents()
    team_a = _write_team(tmp_path, "dummy_agent_a")
    team_b = _write_team(tmp_path, "dummy_agent_b")

    orch = SolutionOrchestrator({"A": str(team_a), "B": str(team_b)})

    wf = GraphWorkflowDefinition(
        name="branching",
        nodes=[
            NodeDefinition(
                id="start",
                type="agent",
                label="Start",
                config={"team": "A", "event": {"type": "dummy_agent_a", "payload": {}}},
            ),
            NodeDefinition(
                id="a",
                type="agent",
                label="A",
                config={
                    "team": "A",
                    "event": {"type": "dummy_agent_a", "payload": {"a": 1}},
                },
            ),
            NodeDefinition(
                id="b",
                type="agent",
                label="B",
                config={
                    "team": "B",
                    "event": {"type": "dummy_agent_b", "payload": {"b": 2}},
                },
            ),
        ],
        edges=[
            EdgeDefinition(source="start", target="a"),
            EdgeDefinition(source="start", target="b"),
        ],
    )

    result = orch.execute_workflow(wf)

    assert result["status"] == "complete"
    assert len(result["results"]) == 3
    assert result["results"][0]["node"] == "start"
    teams = {r["team"] for r in result["results"]}
    assert teams == {"A", "B"}
