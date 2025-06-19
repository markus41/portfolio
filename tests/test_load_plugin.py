import sys
import types
import importlib.metadata
import pytest

from src.utils.plugin_loader import load_plugin
from src.plugins.base_plugin import BaseToolPlugin


class DummyPlugin(BaseToolPlugin):
    def execute(self, payload):
        return payload


def test_load_plugin_from_entry_point(monkeypatch):
    mod = types.ModuleType("dummy_plugin_mod")
    mod.Tool = DummyPlugin
    sys.modules["dummy_plugin_mod"] = mod

    ep = importlib.metadata.EntryPoint(
        "dummy", "dummy_plugin_mod:Tool", "brookside.plugins"
    )
    monkeypatch.setattr(importlib.metadata, "entry_points", lambda group=None: [ep])
    monkeypatch.setattr(
        "src.utils.plugin_loader.import_module",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("import_module called")),
    )

    cls = load_plugin("dummy")
    assert cls is DummyPlugin


def test_load_plugin_fallback(monkeypatch):
    mod = types.ModuleType("src.plugins.fallback_plugin")
    mod.FallbackPlugin = DummyPlugin
    sys.modules["src.plugins.fallback_plugin"] = mod

    monkeypatch.setattr(importlib.metadata, "entry_points", lambda group=None: [])

    cls = load_plugin("fallback_plugin")
    assert cls is DummyPlugin


def test_load_plugin_invalid_entry_point(monkeypatch):
    class NotPlugin:
        pass

    mod = types.ModuleType("bad_plugin_mod")
    mod.NotPlugin = NotPlugin
    sys.modules["bad_plugin_mod"] = mod

    ep = importlib.metadata.EntryPoint(
        "bad", "bad_plugin_mod:NotPlugin", "brookside.plugins"
    )
    monkeypatch.setattr(importlib.metadata, "entry_points", lambda group=None: [ep])

    with pytest.raises(TypeError):
        load_plugin("bad")
