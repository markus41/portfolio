import sys
import types

# Provide a minimal 'requests' stub so importing the notifier modules does not
# fail if the library is missing in the test environment.
sys.modules.setdefault(
    "requests",
    types.SimpleNamespace(
        post=lambda *a, **k: types.SimpleNamespace(
            ok=True, json=lambda: {}, raise_for_status=lambda: None
        ),
        get=lambda *a, **k: types.SimpleNamespace(
            ok=True, json=lambda: {}, raise_for_status=lambda: None
        ),
    ),
)

from src.agents.notification_agent import NotificationAgent


def test_notification_agent_slack(monkeypatch):
    slack_calls = []
    teams_calls = []

    def fake_slack_send(self, channel, text):
        slack_calls.append((channel, text))
        return True

    def fake_teams_send(self, title, text):
        teams_calls.append((title, text))
        return True

    monkeypatch.setattr(
        "src.tools.notification_tools.slack_notifier.SlackNotifier.send",
        fake_slack_send,
    )
    monkeypatch.setattr(
        "src.tools.notification_tools.teams_notifier.TeamsNotifier.send",
        fake_teams_send,
    )

    agent = NotificationAgent()
    out = agent.run({"channel": "#general", "message": "hello", "platform": "slack"})

    assert out["status"] == "notified"
    assert slack_calls == [("#general", "hello")]
    assert teams_calls == []


def test_notification_agent_teams(monkeypatch):
    slack_calls = []
    teams_calls = []

    def fake_slack_send(self, channel, text):
        slack_calls.append((channel, text))
        return True

    def fake_teams_send(self, title, text):
        teams_calls.append((title, text))
        return True

    monkeypatch.setattr(
        "src.tools.notification_tools.slack_notifier.SlackNotifier.send",
        fake_slack_send,
    )
    monkeypatch.setattr(
        "src.tools.notification_tools.teams_notifier.TeamsNotifier.send",
        fake_teams_send,
    )

    agent = NotificationAgent()
    out = agent.run({"channel": "#general", "message": "hi", "platform": "teams"})

    assert out["status"] == "notified"
    assert slack_calls == []
    assert teams_calls == [("Notification", "hi")]
