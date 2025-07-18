from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import sys
import types
import pytest

httpx = pytest.importorskip("httpx")
if getattr(httpx, "__name__", "").startswith("tests.httpx_stub"):
    pytest.skip("httpx package required", allow_module_level=True)
sys.modules.setdefault(
    "prometheus_client",
    types.SimpleNamespace(
        CollectorRegistry=lambda: object(),
        Gauge=lambda *a, **k: types.SimpleNamespace(labels=lambda **kw: types.SimpleNamespace(set=lambda v: None)),
        push_to_gateway=lambda *a, **k: None,
    ),
)
from fastapi.testclient import TestClient

import src.api as api
from src.solution_orchestrator import SolutionOrchestrator


def test_metrics_middleware_enabled(monkeypatch):
    api.settings.PROMETHEUS_PUSHGATEWAY = "http://example:9091"
    api.settings.API_AUTH_KEY = None

    with patch("src.api.PrometheusPusher") as MockPusher:
        instance = MockPusher.return_value
        app = api.create_app(SolutionOrchestrator({}))
        client = TestClient(app)

        response = client.get("/activity")
        assert response.status_code == 200

        labels = {"path": "/activity", "method": "GET"}
        instance.push_metric.assert_any_call("api_request_count", 1, labels)
        args, kwargs = instance.push_metric.call_args_list[1]
        assert args[0] == "api_request_latency_seconds"
        assert kwargs["labels"] == labels


def test_metrics_middleware_disabled(monkeypatch):
    api.settings.PROMETHEUS_PUSHGATEWAY = None

    app = api.create_app(SolutionOrchestrator({}))
    client = TestClient(app)
    response = client.get("/activity")
    assert response.status_code == 200
    assert not any(m.cls.__name__ == "MetricsMiddleware" for m in app.user_middleware)
