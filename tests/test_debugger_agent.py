from agentic_core import EventBus
import src.debugger_agent as dbg
from src.debugger_agent import DebuggerAgent


def test_debugger_agent_success(monkeypatch):
    bus = EventBus()
    agent = DebuggerAgent(bus)
    monkeypatch.setattr(agent, "_ask_gpt", lambda ctx: "diff --git a b")
    calls = []
    monkeypatch.setattr(dbg, "open_pr", lambda diff: calls.append(diff))
    monkeypatch.setattr(dbg, "GITHUB_ENABLED", True)
    out = agent.run({"trace": "boom"})
    assert out == {"diff": "diff --git a b"}
    assert calls == ["diff --git a b"]


def test_debugger_agent_failure(monkeypatch):
    bus = EventBus()
    agent = DebuggerAgent(bus)

    def boom(ctx):
        raise RuntimeError("bad")

    monkeypatch.setattr(agent, "_ask_gpt", boom)
    calls = []
    monkeypatch.setattr(dbg, "open_pr", lambda diff: calls.append(diff))
    monkeypatch.setattr(dbg, "GITHUB_ENABLED", True)

    out = agent.run({"trace": "boom"})
    assert out == {"diff": ""}
    assert calls == []
