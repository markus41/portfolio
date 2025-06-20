import types
from agentic_core import EventBus
import src.debugger_agent as dbg
from src.debugger_agent import DebuggerAgent


def make_openai_stub(result: str):
    """Return an object mimicking the minimal OpenAI API used by DebuggerAgent."""
    message = types.SimpleNamespace(content=result)
    choice = types.SimpleNamespace(message=message)
    response = types.SimpleNamespace(choices=[choice])

    class StubChatCompletion:
        @staticmethod
        def create(*args, **kwargs):
            return response

    return types.SimpleNamespace(ChatCompletion=StubChatCompletion())


def test_run_opens_pr_and_uses_ask_gpt(monkeypatch):
    bus = EventBus()
    agent = DebuggerAgent(bus)

    monkeypatch.setattr(dbg, "openai", make_openai_stub("diff --git a b"))

    seen = []
    orig = agent._ask_gpt

    def wrapper(ctx: str) -> str:
        seen.append(ctx)
        return orig(ctx)

    monkeypatch.setattr(agent, "_ask_gpt", wrapper)

    pr_calls = []
    monkeypatch.setattr(dbg, "open_pr", lambda diff: pr_calls.append(diff))
    monkeypatch.setattr(dbg, "GITHUB_ENABLED", True)

    result = agent.run({"trace": "boom"})

    assert result == {"diff": "diff --git a b"}
    assert seen == ["boom"]
    assert pr_calls == ["diff --git a b"]


def test_run_handles_exception(monkeypatch):
    bus = EventBus()
    agent = DebuggerAgent(bus)

    class FailingChatCompletion:
        @staticmethod
        def create(*args, **kwargs):
            raise RuntimeError("bad")

    monkeypatch.setattr(dbg, "openai", types.SimpleNamespace(ChatCompletion=FailingChatCompletion()))

    seen = []
    orig = agent._ask_gpt

    def wrapper(ctx: str) -> str:
        seen.append(ctx)
        return orig(ctx)

    monkeypatch.setattr(agent, "_ask_gpt", wrapper)

    pr_calls = []
    monkeypatch.setattr(dbg, "open_pr", lambda diff: pr_calls.append(diff))
    monkeypatch.setattr(dbg, "GITHUB_ENABLED", True)

    result = agent.run({"trace": "boom"})

    assert result == {"diff": ""}
    assert seen == ["boom"]
    assert pr_calls == []


def test_run_without_github(monkeypatch):
    bus = EventBus()
    agent = DebuggerAgent(bus)

    monkeypatch.setattr(dbg, "openai", make_openai_stub("diff --git a b"))

    seen = []
    orig = agent._ask_gpt

    def wrapper(ctx: str) -> str:
        seen.append(ctx)
        return orig(ctx)

    monkeypatch.setattr(agent, "_ask_gpt", wrapper)

    pr_calls = []
    monkeypatch.setattr(dbg, "open_pr", lambda diff: pr_calls.append(diff))
    monkeypatch.setattr(dbg, "GITHUB_ENABLED", False)

    result = agent.run({"trace": "boom"})

    assert result == {"diff": "diff --git a b"}
    assert seen == ["boom"]
    assert pr_calls == []
