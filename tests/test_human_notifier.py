import sys
import types

# Stub requests for notifier modules
sys.modules.setdefault(
    "requests",
    types.SimpleNamespace(
        post=lambda *a, **k: types.SimpleNamespace(ok=True, json=lambda: {}, raise_for_status=lambda: None),
        get=lambda *a, **k: types.SimpleNamespace(ok=True, json=lambda: {}, raise_for_status=lambda: None),
    ),
)

# Provide a minimal 'sendgrid' stub so importing EmailTool does not fail
class DummyClient:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def send(self, message):
        return types.SimpleNamespace(status_code=202)

sendgrid_mail = types.SimpleNamespace(Mail=lambda **kw: types.SimpleNamespace(**kw))
sendgrid_helpers = types.SimpleNamespace(mail=sendgrid_mail)
sendgrid_stub = types.SimpleNamespace(SendGridAPIClient=DummyClient, helpers=sendgrid_helpers)

sys.modules.setdefault("sendgrid", sendgrid_stub)
sys.modules.setdefault("sendgrid.helpers", sendgrid_helpers)
sys.modules.setdefault("sendgrid.helpers.mail", sendgrid_mail)

from src.tools.notification_tools import human_notifier
from src.config import settings


def test_notify_human_all_channels(monkeypatch):
    slack_calls = []
    teams_calls = []
    email_calls = []

    def fake_slack_send(self, channel, text):
        slack_calls.append((channel, text))
        return True

    def fake_teams_send(self, title, text):
        teams_calls.append((title, text))
        return True

    def fake_email(to_email, subject, html_content):
        email_calls.append((to_email, subject, html_content))
        return True

    monkeypatch.setattr(
        "src.tools.notification_tools.slack_notifier.SlackNotifier.send",
        fake_slack_send,
    )
    monkeypatch.setattr(
        "src.tools.notification_tools.teams_notifier.TeamsNotifier.send",
        fake_teams_send,
    )
    monkeypatch.setattr(
        "src.tools.email_tool.EmailTool.send_email",
        lambda self, to_email, subject, html_content: fake_email(
            to_email, subject, html_content
        ),
    )

    settings.SLACK_WEBHOOK_URL = "http://slack"
    settings.TEAMS_WEBHOOK_URL = "http://teams"
    settings.SENDGRID_API_KEY = "key"

    out = human_notifier.notify_human("critical", "something broke")

    assert out["status"] == "sent"
    assert slack_calls
    assert teams_calls
    assert email_calls


def test_notify_human_partial_failure(monkeypatch):
    monkeypatch.setattr(
        "src.tools.notification_tools.slack_notifier.SlackNotifier.send",
        lambda self, channel, text: (_ for _ in ()).throw(RuntimeError("boom")),
    )
    monkeypatch.setattr(
        "src.tools.notification_tools.teams_notifier.TeamsNotifier.send",
        lambda self, title, text: True,
    )
    monkeypatch.setattr(
        "src.tools.email_tool.EmailTool.send_email",
        lambda self, to_email, subject, html_content: True,
    )

    settings.SLACK_WEBHOOK_URL = "http://slack"
    settings.TEAMS_WEBHOOK_URL = "http://teams"
    settings.SENDGRID_API_KEY = "key"

    out = human_notifier.notify_human("warning", "partial")

    assert out["status"] == "sent"
