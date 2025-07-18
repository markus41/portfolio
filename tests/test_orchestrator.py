# tests/test_orchestrator.py

import sys
import types
import pytest

# Provide a minimal 'requests' stub so importing the orchestrator does not
# fail if the library is missing in the test environment.
sys.modules.setdefault(
    "requests",
    types.SimpleNamespace(
        post=lambda *a, **k: types.SimpleNamespace(ok=True, json=lambda: {}),
        get=lambda *a, **k: types.SimpleNamespace(ok=True, json=lambda: {}),
    ),
)

from src.orchestrator import Orchestrator
from src.base_orchestrator import BaseOrchestrator
from src.events import (
    LeadCaptureEvent,
    ChatbotEvent,
    CRMPipelineEvent,
    SegmentationEvent,
)


def test_orchestrator_is_base_class():
    assert issubclass(Orchestrator, BaseOrchestrator)


@pytest.mark.parametrize(
    "event_type",
    [
        "lead_capture",
        "chatbot",
        "crm_pipeline",
        "segmentation",
    ],
)
def test_known_event_types(monkeypatch, event_type):
    class DummyScheduler:
        def create_event(self, cid, ev):
            return {"id": "evt"}

    # avoid optional dependency errors when CRMPipelineAgent is constructed
    monkeypatch.setattr(
        "src.tools.scheduler_tool.SchedulerTool",
        lambda: DummyScheduler(),
    )

    orch = Orchestrator("http://memory")

    store_calls = {}

    def fake_store(key, payload):
        store_calls["key"] = key
        store_calls["payload"] = payload
        return True

    monkeypatch.setattr(orch.memory, "store", fake_store)

    run_payload = {}

    def fake_run(payload):
        run_payload["payload"] = payload
        return {"handled": event_type}

    monkeypatch.setattr(orch.agents[event_type], "run", fake_run)

    event_classes = {
        "lead_capture": LeadCaptureEvent,
        "chatbot": ChatbotEvent,
        "crm_pipeline": CRMPipelineEvent,
        "segmentation": SegmentationEvent,
    }
    payloads = {
        "lead_capture": {"form_data": {}, "source": "web"},
        "chatbot": {"messages": []},
        "crm_pipeline": {
            "deal_id": "d1",
            "calendar_id": "c1",
            "followup_template": {"summary": "s"},
        },
        "segmentation": {"segments": [], "budget_per_segment": 1},
    }

    payload = payloads[event_type]
    res = orch.handle_event_sync({"type": event_type, "payload": payload})

    assert store_calls == {"key": event_type, "payload": payload}
    expected_cls = event_classes[event_type]
    assert run_payload["payload"] == expected_cls(**payload)
    assert res["status"] == "done"
    assert res["result"] == {"handled": event_type}


def test_unknown_event_type(monkeypatch):
    class DummyScheduler:
        def create_event(self, cid, ev):
            return {"id": "evt"}

    monkeypatch.setattr(
        "src.tools.scheduler_tool.SchedulerTool",
        lambda: DummyScheduler(),
    )

    orch = Orchestrator("http://memory")

    store_calls = {}

    def fake_store(key, payload):
        store_calls["key"] = key
        store_calls["payload"] = payload
        return True

    monkeypatch.setattr(orch.memory, "store", fake_store)

    called = []

    # ensure none of the agents are invoked
    for name, agent in orch.agents.items():

        def make_fake(n):
            def fake_run(payload):
                called.append(n)
                return {}

            return fake_run

        monkeypatch.setattr(agent, "run", make_fake(name))

    payload = {"foo": "bar"}
    res = orch.handle_event_sync({"type": "unknown", "payload": payload})

    assert res == {"status": "ignored"}
    assert store_calls == {"key": "unknown", "payload": payload}
    assert called == []


def test_invalid_event_payload(monkeypatch):
    """Invalid payloads should result in an ``invalid`` status."""

    class DummyScheduler:
        def create_event(self, cid, ev):
            return {"id": "evt"}

    monkeypatch.setattr(
        "src.tools.scheduler_tool.SchedulerTool",
        lambda: DummyScheduler(),
    )

    orch = Orchestrator("http://memory")

    # missing required field 'source' for LeadCaptureEvent
    payload = {"form_data": {}}
    res = orch.handle_event_sync({"type": "lead_capture", "payload": payload})

    assert res["status"] == "invalid"
