from src.agents.analytics_agent import AnalyticsAgent


def test_analytics_agent_push(monkeypatch):
    calls = {}

    def fake_push_metric(self, name, value, labels=None):
        calls['name'] = name
        calls['value'] = value
        calls['labels'] = labels or {}

    monkeypatch.setattr(
        'src.tools.metrics_tools.prometheus_tool.PrometheusPusher.push_metric',
        fake_push_metric
    )

    agent = AnalyticsAgent()
    payload = {"metric": "requests_total", "value": 5, "labels": {"env": "test"}}
    result = agent.run(payload)

    assert result == {"status": "pushed"}
    assert calls == {
        "name": "requests_total",
        "value": 5,
        "labels": {"env": "test"}
    }
