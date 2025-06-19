import sys
import types
import importlib.metadata
import pytest

from src.utils.plugin_loader import load_agent
from src.agents.base_agent import BaseAgent


class DummyAgent(BaseAgent):
    def run(self, payload):
        return payload


def test_load_agent_from_entry_point(monkeypatch):
    mod = types.ModuleType("dummy_ep_mod")
    mod.PluginAgent = DummyAgent
    sys.modules["dummy_ep_mod"] = mod

    ep = importlib.metadata.EntryPoint(
        "dummy", "dummy_ep_mod:PluginAgent", "brookside.agents"
    )
    monkeypatch.setattr(importlib.metadata, "entry_points", lambda group=None: [ep])
    # ensure fallback import is not used
    monkeypatch.setattr(
        "src.utils.plugin_loader.import_module",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("import_module called")),
    )

    cls = load_agent("dummy")
    assert cls is DummyAgent


def test_load_agent_fallback_to_module(monkeypatch):
    mod = types.ModuleType("src.agents.fallback_agent")
    mod.FallbackAgent = DummyAgent
    sys.modules["src.agents.fallback_agent"] = mod

    monkeypatch.setattr(importlib.metadata, "entry_points", lambda group=None: [])

    cls = load_agent("fallback_agent")
    assert cls is DummyAgent


def test_load_agent_invalid_entry_point(monkeypatch):
    class NotAgent:
        pass

    bad_mod = types.ModuleType("bad_mod")
    bad_mod.NotAgent = NotAgent
    sys.modules["bad_mod"] = bad_mod

    ep = importlib.metadata.EntryPoint("bad", "bad_mod:NotAgent", "brookside.agents")
    monkeypatch.setattr(importlib.metadata, "entry_points", lambda group=None: [ep])

    with pytest.raises(TypeError):
        load_agent("bad")
