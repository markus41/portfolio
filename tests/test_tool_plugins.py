import sys
import types
import importlib

import pytest

from src.config import settings


def test_crm_plugin_execute(monkeypatch):
    calls = {}

    def fake_post(url, json=None, headers=None, timeout=5):
        calls["url"] = url
        calls["json"] = json
        calls["headers"] = headers
        return types.SimpleNamespace(
            json=lambda: {"ok": True}, raise_for_status=lambda: None
        )

    crm_mod = importlib.reload(importlib.import_module("src.plugins.crm_plugin"))
    monkeypatch.setattr(crm_mod, "requests", types.SimpleNamespace(post=fake_post))
    crm_mod.settings.CRM_API_URL = "http://crm"
    crm_mod.settings.CRM_API_KEY = "key"
    plugin = crm_mod.CRMPlugin()
    res = plugin.execute({"action": "record", "data": {"name": "Bob"}})

    assert res == {"ok": True}
    assert calls["url"] == "http://crm/record"
    assert calls["json"] == {"name": "Bob"}
    assert calls["headers"] == {"Authorization": "Bearer key"}


def test_crm_plugin_missing_requests(monkeypatch):
    crm_mod = importlib.reload(importlib.import_module("src.plugins.crm_plugin"))
    monkeypatch.setattr(crm_mod, "requests", None)
    crm_mod.settings.CRM_API_URL = "http://crm"
    crm_mod.settings.CRM_API_KEY = "key"
    assert crm_mod.CRMPlugin().execute({"action": "x"}) == {}


class DummyClient:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def send(self, message):
        DummyClient.sent.append(message)
        return types.SimpleNamespace(status_code=202)


DummyClient.sent = []


def setup_sendgrid(monkeypatch):
    sendgrid_mail = types.SimpleNamespace(Mail=lambda **kw: types.SimpleNamespace(**kw))
    sendgrid_helpers = types.SimpleNamespace(mail=sendgrid_mail)
    sendgrid_stub = types.SimpleNamespace(
        SendGridAPIClient=DummyClient, helpers=sendgrid_helpers
    )
    sys.modules["sendgrid"] = sendgrid_stub
    sys.modules["sendgrid.helpers"] = sendgrid_helpers
    sys.modules["sendgrid.helpers.mail"] = sendgrid_mail


def test_email_plugin_execute(monkeypatch):
    setup_sendgrid(monkeypatch)
    monkeypatch.setattr(settings, "SENDGRID_API_KEY", "k")
    monkeypatch.setattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com")

    email_mod = importlib.reload(importlib.import_module("src.plugins.email_plugin"))
    plugin = email_mod.EmailPlugin()
    res = plugin.execute({"to": "u@example.com", "subject": "Hi", "html": "<p>hi</p>"})

    assert res is True
    assert DummyClient.sent and DummyClient.sent[0].to_emails == "u@example.com"


def test_scraping_plugin_execute(monkeypatch):
    calls = {}

    def fake_get(url, headers=None, timeout=5):
        calls["url"] = url
        calls["headers"] = headers
        return types.SimpleNamespace(text="<html>", raise_for_status=lambda: None)

    scraping_mod = importlib.reload(
        importlib.import_module("src.plugins.scraping_plugin")
    )
    monkeypatch.setattr(scraping_mod, "requests", types.SimpleNamespace(get=fake_get))
    scraping_mod.settings.SCRAPER_USER_AGENT = "AgentBot"
    html = scraping_mod.ScrapingPlugin().execute({"url": "http://example.com"})

    assert html == "<html>"
    assert calls["headers"] == {"User-Agent": "AgentBot"}


def test_scraping_plugin_missing_requests(monkeypatch):
    scraping_mod = importlib.reload(
        importlib.import_module("src.plugins.scraping_plugin")
    )
    monkeypatch.setattr(scraping_mod, "requests", None)
    scraping_mod.settings.SCRAPER_USER_AGENT = "AgentBot"
    assert scraping_mod.ScrapingPlugin().execute({"url": "http://x"}) == ""


def test_cloud_docs_plugin_execute(monkeypatch):
    calls = {}

    def fake_post(url, json=None, headers=None, timeout=5):
        calls["url"] = url
        calls["json"] = json
        calls["headers"] = headers
        return types.SimpleNamespace(
            json=lambda: {"id": "1"}, raise_for_status=lambda: None
        )

    cloud_mod = importlib.reload(
        importlib.import_module("src.plugins.cloud_docs_plugin")
    )
    monkeypatch.setattr(cloud_mod, "requests", types.SimpleNamespace(post=fake_post))
    cloud_mod.settings.CLOUD_DOCS_API_URL = "http://docs"
    cloud_mod.settings.CLOUD_DOCS_API_KEY = "token"
    result = cloud_mod.CloudDocsPlugin().execute(
        {"action": "upload", "data": {"name": "a"}}
    )

    assert result == {"id": "1"}
    assert calls["url"] == "http://docs/upload"
    assert calls["json"] == {"name": "a"}
    assert calls["headers"] == {"Authorization": "Bearer token"}


def test_cloud_docs_plugin_missing_requests(monkeypatch):
    cloud_mod = importlib.reload(
        importlib.import_module("src.plugins.cloud_docs_plugin")
    )
    monkeypatch.setattr(cloud_mod, "requests", None)
    cloud_mod.settings.CLOUD_DOCS_API_URL = "http://docs"
    cloud_mod.settings.CLOUD_DOCS_API_KEY = "token"
    assert cloud_mod.CloudDocsPlugin().execute({"action": "x"}) == {}
