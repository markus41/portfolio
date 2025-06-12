from src.agents.analytics_agent import AnalyticsAgent

class DummyPusher:
    def __init__(self, job="test"):
        self.calls = []
    def push_metric(self, name, value, labels=None):
        self.calls.append((name, value, labels))
        return {"status": "queued"}

def test_analytics_push(monkeypatch):
    monkeypatch.setattr("src.agents.analytics_agent.PrometheusPusher", DummyPusher)
    agent = AnalyticsAgent()
    agent.run({"metric": "leads", "value": 5, "labels": {"stage": "new"}})
    assert agent.pusher.calls == [("leads", 5.0, {"stage": "new"})]
