import sys
import types
import logging

# Stub prometheus_client to satisfy optional dependency
sys.modules.setdefault(
    "prometheus_client",
    types.SimpleNamespace(
        CollectorRegistry=lambda: object(),
        Gauge=lambda *a, **k: types.SimpleNamespace(
            labels=lambda **kw: types.SimpleNamespace(set=lambda v: None)
        ),
        push_to_gateway=lambda *a, **k: None,
    ),
)

from src.base_orchestrator import BaseOrchestrator
from src.agents.base_agent import BaseAgent

class BudgetAgent(BaseAgent):
    token_budget = 10
    loop_budget = 1

    def run(self, payload):
        return {"payload": payload}


def test_token_budget_termination(monkeypatch):
    orch = BaseOrchestrator()
    orch.agents = {"budget": BudgetAgent()}

    res = orch.handle_event_sync({"type": "budget", "payload": "x" * 20})

    assert res["status"] == "terminated"
    assert res["reason"] == "token_budget_exceeded"


def test_loop_budget_termination(monkeypatch):
    orch = BaseOrchestrator()
    orch.agents = {"budget": BudgetAgent()}

    ok = orch.handle_event_sync({"type": "budget", "payload": "ok"})
    assert ok["status"] == "done"

    res = orch.handle_event_sync({"type": "budget", "payload": "again"})
    assert res["status"] == "terminated"
    assert res["reason"] == "loop_budget_exceeded"


def test_usage_metrics(monkeypatch):
    pushed = []

    class DummyPusher:
        def __init__(self, job="test"):
            pass
        def push_metric(self, name, value, labels=None):
            pushed.append((name, value, labels))

    monkeypatch.setattr("src.base_orchestrator.PrometheusPusher", DummyPusher)
    # Force metrics even without environment variable
    monkeypatch.setattr("src.base_orchestrator.settings.PROMETHEUS_PUSHGATEWAY", "http://gw")

    orch = BaseOrchestrator()
    orch.agents = {"budget": BudgetAgent()}

    orch.handle_event_sync({"type": "budget", "payload": "short"})

    assert any(m[0] == "agent_tokens_used" for m in pushed)
    assert any(m[0] == "agent_loop_count" for m in pushed)
