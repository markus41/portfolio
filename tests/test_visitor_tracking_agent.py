import logging
import sys
import types

# Provide a minimal 'requests' stub so importing the analytics client does not fail
sys.modules.setdefault(
    "requests",
    types.SimpleNamespace(
        post=lambda *a, **k: types.SimpleNamespace(
            ok=True, json=lambda: {}, raise_for_status=lambda: None
        )
    ),
)

from src.agents.sales.visitor_tracking_agent import VisitorTrackingAgent


class DummyAnalytics:
    def __init__(self):
        self.calls = []

    def track(self, data, retries: int = 3):
        self.calls.append(data)
        return True


def test_visitor_tracking_success(monkeypatch, caplog):
    dummy = DummyAnalytics()
    monkeypatch.setattr(
        "src.agents.sales.visitor_tracking_agent.AnalyticsClient", lambda: dummy
    )

    agent = VisitorTrackingAgent()
    payload = {"visitor_id": "v1", "page": "/", "timestamp": "t"}
    with caplog.at_level(logging.INFO):
        result = agent.run(payload)

    assert result["status"] == "logged"
    assert result["analytics_sent"] is True
    assert dummy.calls == [payload]
    assert any("Tracked visitor" in r.message for r in caplog.records)


class FailingAnalytics(DummyAnalytics):
    def track(self, data, retries: int = 3):
        raise RuntimeError("boom")


def test_visitor_tracking_failure(monkeypatch, caplog):
    dummy = FailingAnalytics()
    monkeypatch.setattr(
        "src.agents.sales.visitor_tracking_agent.AnalyticsClient", lambda: dummy
    )

    agent = VisitorTrackingAgent()
    payload = {"visitor_id": "v2", "page": "/err", "timestamp": "t"}
    with caplog.at_level(logging.ERROR):
        result = agent.run(payload)

    assert result["analytics_sent"] is False
    # should still include original payload
    assert result["visitor_id"] == "v2"
    assert any("Analytics client failure" in r.message for r in caplog.records)
