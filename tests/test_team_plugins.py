import json
import sys
import types
import importlib.metadata

import pytest

from src.team_orchestrator import TeamOrchestrator
from src.plugins.base_plugin import BaseToolPlugin
from src.agents.base_agent import BaseAgent


class DummyPlugin(BaseToolPlugin):
    def execute(self, payload):
        return {"ok": payload}


class DummyAgent(BaseAgent):
    def run(self, payload):
        return payload


def _write_cfg(tmp_path):
    cfg = {
        "provider": "autogen.agentchat.teams.RoundRobinGroupChat",
        "config": {
            "participants": [{"config": {"name": "dummy_agent"}}],
            "tools": [
                {
                    "provider": "autogen.tools.FunctionTool",
                    "config": {"name": "dummy", "plugin": "dummy"},
                }
            ],
        },
    }
    path = tmp_path / "team.json"
    path.write_text(json.dumps(cfg))
    return path


def test_plugin_attached(monkeypatch, tmp_path):
    path = _write_cfg(tmp_path)
    mod = types.ModuleType("src.agents.dummy_agent")
    mod.DummyAgent = DummyAgent
    sys.modules["src.agents.dummy_agent"] = mod

    plugin_mod = types.ModuleType("dummy_mod")
    plugin_mod.DummyPlugin = DummyPlugin
    sys.modules["dummy_mod"] = plugin_mod

    ep = importlib.metadata.EntryPoint(
        "dummy", "dummy_mod:DummyPlugin", "brookside.plugins"
    )
    monkeypatch.setattr(importlib.metadata, "entry_points", lambda group=None: [ep])

    orch = TeamOrchestrator(str(path))
    tool_cfg = orch.team_config["config"]["tools"][0]["config"]
    func = tool_cfg.get("function")
    assert callable(func)
    assert func({"x": 1}) == {"ok": {"x": 1}}
