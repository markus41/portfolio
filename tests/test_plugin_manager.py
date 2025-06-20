import importlib.metadata
import sys
import types

from src.plugin_manager import list_plugins, list_agents, get_plugin_details
from src.plugins.base_plugin import BaseToolPlugin


class DummyPlugin(BaseToolPlugin):
    """Dummy plugin used for discovery tests."""

    name = "dummy"

    def execute(self, payload):
        return True


def test_list_plugins_builtin():
    names = list_plugins()
    assert "email_plugin" in names


def test_list_plugins_entry_point(monkeypatch):
    mod = types.ModuleType("dummy_mod")
    mod.Tool = DummyPlugin
    sys.modules["dummy_mod"] = mod

    ep = importlib.metadata.EntryPoint(
        "dummy_entry", "dummy_mod:Tool", "brookside.plugins"
    )
    monkeypatch.setattr(importlib.metadata, "entry_points", lambda group=None: [ep])

    names = list_plugins()
    assert "dummy_entry" in names


def test_get_plugin_details(monkeypatch):
    mod = types.ModuleType("detail_mod")
    mod.Tool = DummyPlugin
    sys.modules["detail_mod"] = mod

    ep = importlib.metadata.EntryPoint("detail", "detail_mod:Tool", "brookside.plugins")
    monkeypatch.setattr(importlib.metadata, "entry_points", lambda group=None: [ep])

    info = get_plugin_details("detail")
    assert info["class"].endswith("DummyPlugin")
    assert info["name"] == "dummy"
    assert "dummy plugin" in info["doc"].lower()


def test_list_agents_builtin():
    names = list_agents()
    assert "sales.lead_capture_agent" in names


def test_list_agents_entry_point(monkeypatch):
    mod = types.ModuleType("dummy_agent_mod")

    class DummyAgent:
        pass

    mod.Agent = DummyAgent
    sys.modules["dummy_agent_mod"] = mod

    ep = importlib.metadata.EntryPoint(
        "dummy_agent", "dummy_agent_mod:Agent", "brookside.agents"
    )
    monkeypatch.setattr(importlib.metadata, "entry_points", lambda group=None: [ep])

    names = list_agents()
    assert "dummy_agent" in names
