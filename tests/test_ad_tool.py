import sys
import types

sys.modules.setdefault(
    "requests",
    types.SimpleNamespace(
        post=lambda *a, **k: types.SimpleNamespace(
            ok=True, json=lambda: {}, raise_for_status=lambda: None
        ),
        HTTPError=Exception,
        RequestException=Exception,
    ),
)

import requests
from src.tools.ad_tool import AdTool


class DummyResponse:
    def __init__(self, data, exc=None):
        self._data = data
        self._exc = exc

    def json(self):
        return self._data

    def raise_for_status(self):
        if self._exc:
            raise self._exc


def test_create_facebook_campaign_success(monkeypatch):
    def fake_post(url, json=None, headers=None, timeout=10):
        return DummyResponse({"id": "fb123", "status": "CREATED"})

    monkeypatch.setattr("src.tools.ad_tool.requests.post", fake_post)
    tool = AdTool()
    result = tool.create_facebook_campaign("Test", [1, 2], 100)
    assert result == {
        "platform": "facebook",
        "campaign_id": "fb123",
        "status": "CREATED",
        "message": None,
    }


def test_create_facebook_campaign_error(monkeypatch):
    def fake_post(url, json=None, headers=None, timeout=10):
        return DummyResponse({}, exc=requests.HTTPError("bad"))

    monkeypatch.setattr("src.tools.ad_tool.requests.post", fake_post)
    tool = AdTool()
    result = tool.create_facebook_campaign("Oops", [], 50)
    assert result["platform"] == "facebook"
    assert result["campaign_id"] is None
    assert result["status"] == "error"
    assert "bad" in result["message"]


def test_create_google_campaign_success(monkeypatch):
    def fake_post(url, json=None, params=None, timeout=10):
        return DummyResponse({"id": "ga123", "status": "CREATED"})

    monkeypatch.setattr("src.tools.ad_tool.requests.post", fake_post)
    tool = AdTool()
    result = tool.create_google_campaign("MyCamp", ["kw"], 200)
    assert result == {
        "platform": "google",
        "campaign_id": "ga123",
        "status": "CREATED",
        "message": None,
    }


def test_create_google_campaign_error(monkeypatch):
    def fake_post(url, json=None, params=None, timeout=10):
        return DummyResponse({}, exc=requests.HTTPError("fail"))

    monkeypatch.setattr("src.tools.ad_tool.requests.post", fake_post)
    tool = AdTool()
    result = tool.create_google_campaign("Bad", [], 10)
    assert result["platform"] == "google"
    assert result["campaign_id"] is None
    assert result["status"] == "error"
    assert "fail" in result["message"]
