# src/tests/test_crm_pipeline_agent.py

import pytest
from src.agents.crm_pipeline_agent import CRMPipelineAgent

class DummyCRM:
    def get_deal(self, d): return {"stage":"Proposal Sent","next_action_date":{"dateTime":"2025-07-01T10:00:00","timeZone":"America/Los_Angeles"}}

class DummyScheduler:
    def create_event(self, cid, ev): return {"id":"evt123"}

def test_pipeline_agent(monkeypatch):
    monkeypatch.setattr("src.tools.crm_tools.crm_tool.CRMTool", DummyCRM)
    monkeypatch.setattr("src.tools.scheduler_tool.SchedulerTool", lambda: DummyScheduler())
    agent = CRMPipelineAgent()
    payload = {"deal_id":"d1","calendar_id":"cal1","followup_template":{"summary":"Follow-up","attendees":[{"email":"a@b.com"}]}}
    res = agent.run(payload)
    assert res["action"] == "followup_scheduled"
    assert res["event_id"] == "evt123"
