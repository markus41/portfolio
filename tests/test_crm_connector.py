import types
import pytest

from src.crm_connector import fetch_deals, Deal
from src.config import settings


def test_fetch_deals_success(monkeypatch):
    data = {
        "results": [
            {
                "id": "1",
                "amount": 50,
                "stage": "New",
                "days_in_stage": 2,
                "last_touch": "2025-01-01",
                "probability": 0.3,
            },
            {
                "id": "2",
                "amount": 100,
                "stage": "Proposal",
                "days_in_stage": 5,
                "last_touch": "2025-01-02",
                "probability": 0.5,
            },
        ]
    }

    calls = {}

    def fake_get(url, params=None, headers=None):
        calls["url"] = url
        calls["params"] = params
        calls["headers"] = headers
        return types.SimpleNamespace(json=lambda: data, raise_for_status=lambda: None)

    monkeypatch.setattr(
        "src.crm_connector.requests", types.SimpleNamespace(get=fake_get)
    )
    monkeypatch.setattr(settings, "CRM_API_URL", "http://crm.example.com")
    monkeypatch.setattr(settings, "CRM_API_KEY", "abc")

    deals = fetch_deals("tenant1")

    assert calls["url"] == "http://crm.example.com/deals"
    assert calls["params"] == {"tenant_id": "tenant1"}
    assert calls["headers"] == {"Authorization": "Bearer abc"}
    assert deals == [
        Deal("1", 50.0, "New", 2, "2025-01-01", 0.3),
        Deal("2", 100.0, "Proposal", 5, "2025-01-02", 0.5),
    ]


def test_fetch_deals_no_requests(monkeypatch):
    monkeypatch.setattr("src.crm_connector.requests", None)
    assert fetch_deals("t1") == []
