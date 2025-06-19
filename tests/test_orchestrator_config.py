import json
import sys
import types
from pathlib import Path

import pytest

from src.orchestrator import Orchestrator
from src.agents.base_agent import BaseAgent


class DummyAgentA(BaseAgent):
    def run(self, payload):
        return {"handled": "A"}


class DummyAgentB(BaseAgent):
    def run(self, payload):
        return {"handled": "B"}


def test_load_agents_from_config(tmp_path: Path):
    cfg = {
        "a": "src.agents.dummy_agent_a.DummyAgentA",
        "b": "src.agents.dummy_agent_b.DummyAgentB",
    }
    cfg_path = tmp_path / "cfg.json"
    cfg_path.write_text(json.dumps(cfg))

    mod_a = types.ModuleType("src.agents.dummy_agent_a")
    mod_a.DummyAgentA = DummyAgentA
    sys.modules["src.agents.dummy_agent_a"] = mod_a

    mod_b = types.ModuleType("src.agents.dummy_agent_b")
    mod_b.DummyAgentB = DummyAgentB
    sys.modules["src.agents.dummy_agent_b"] = mod_b

    orch = Orchestrator("http://mem", config_path=str(cfg_path))

    assert set(orch.agents.keys()) == {"a", "b"}
    assert isinstance(orch.agents["a"], DummyAgentA)
    assert isinstance(orch.agents["b"], DummyAgentB)

    out = orch.handle_event({"type": "a", "payload": {}})
    assert out["status"] == "done"
    assert out["result"] == {"handled": "A"}
