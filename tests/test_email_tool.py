import sys
import types

# Provide a minimal 'sendgrid' stub so importing EmailTool does not fail

class DummyClient:
    def __init__(self, api_key=None):
        self.api_key = api_key
    def send(self, message):
        return types.SimpleNamespace(status_code=202)

class DummyMail:
    def __init__(self, from_email=None, to_emails=None, subject=None, html_content=None):
        self.from_email = from_email
        self.to_emails = to_emails
        self.subject = subject
        self.html_content = html_content

sendgrid_mail = types.SimpleNamespace(Mail=DummyMail)
sendgrid_helpers = types.SimpleNamespace(mail=sendgrid_mail)
sendgrid_stub = types.SimpleNamespace(SendGridAPIClient=DummyClient, helpers=sendgrid_helpers)

sys.modules.setdefault("sendgrid", sendgrid_stub)
sys.modules.setdefault("sendgrid.helpers", sendgrid_helpers)
sys.modules.setdefault("sendgrid.helpers.mail", sendgrid_mail)

from src.tools.email_tool import EmailTool
from src.config import settings


def test_send_email_success(monkeypatch):
    """EmailTool.send_email should return True when the API responds with 2xx."""
    sent = []

    def fake_send(self, message):
        sent.append(message)
        return types.SimpleNamespace(status_code=202)

    monkeypatch.setattr("sendgrid.SendGridAPIClient.send", fake_send, raising=False)
    settings.SENDGRID_API_KEY = "key"

    tool = EmailTool()
    result = tool.send_email("u@example.com", "Hello", "<p>Hi</p>")

    assert result is True
    assert len(sent) == 1


def test_send_email_exception(monkeypatch):
    """EmailTool.send_email should return False if an exception occurs."""

    def fake_send(self, message):
        raise RuntimeError("boom")

    monkeypatch.setattr("sendgrid.SendGridAPIClient.send", fake_send, raising=False)
    settings.SENDGRID_API_KEY = "key"

    tool = EmailTool()
    result = tool.send_email("u@example.com", "Hello", "<p>Hi</p>")

    assert result is False

