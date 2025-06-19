import logging
import sys
import types

# Provide a minimal 'prometheus_client' stub so importing the agent does not fail
sys.modules.setdefault(
    "prometheus_client",
    types.SimpleNamespace(
        CollectorRegistry=lambda: object(),
        Gauge=lambda *a, **k: types.SimpleNamespace(labels=lambda **kw: types.SimpleNamespace(set=lambda v: None)),
        push_to_gateway=lambda *a, **k: None,
    ),
)

from src.agents.analytics_agent import AnalyticsAgent


def test_analytics_agent_push(monkeypatch, caplog):
    pushed = []

    def fake_push_metric(self, name, value, labels=None):
        pushed.append((name, value, labels))

    monkeypatch.setattr(
        "src.tools.metrics_tools.prometheus_tool.PrometheusPusher.push_metric",
        fake_push_metric,
    )

    agent = AnalyticsAgent()
    with caplog.at_level(logging.INFO):
        result = agent.run({"metric": "sales", "value": 100, "labels": {"region": "us"}})

    assert result == {"status": "pushed"}
    assert pushed == [("sales", 100.0, {"region": "us"})]
    assert any("Pushed metric sales=100.0" in r.message for r in caplog.records)
