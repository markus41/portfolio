from agentic_core import EventBus, AsyncEventBus
import asyncio
import pytest

from src.crm_connector import Deal
from src.agents.revops_agent import RevOpsAgent


def test_revops_agent(monkeypatch):
    bus = EventBus()
    reports = []
    bus.subscribe("RevOps.Report", reports.append)

    deals = [
        Deal("d1", 1000, "Negotiate", 5, "2025-06-01", 0.6),
        Deal("d2", 2000, "Proposal", 40, "2025-06-02", 0.5),
    ]
    monkeypatch.setattr("src.crm_connector.fetch_deals", lambda tid: deals)

    agent = RevOpsAgent(bus)
    monkeypatch.setattr(agent, "_ask_gpt", lambda prompt: {
        "forecast": "$3k",
        "risks": ["stall"],
        "actions": ["email"],
    })

    out = agent.run_sync({"tenant_id": "t1"})
    assert out["forecast"] == "$3k"
    assert reports[0]["actions"] == ["email"]


def test_revops_agent_async(monkeypatch):
    bus = AsyncEventBus()
    reports = []
    bus.subscribe("RevOps.Report", reports.append)

    deals = [
        Deal("d1", 1000, "Negotiate", 5, "2025-06-01", 0.6),
        Deal("d2", 2000, "Proposal", 40, "2025-06-02", 0.5),
    ]
    monkeypatch.setattr("src.crm_connector.fetch_deals", lambda tid: deals)

    agent = RevOpsAgent(bus)
    monkeypatch.setattr(agent, "_ask_gpt", lambda prompt: {
        "forecast": "$3k",
        "risks": ["stall"],
        "actions": ["email"],
    })

    async def main():
        out = await agent.run({"tenant_id": "t1"})
        assert out["forecast"] == "$3k"
        assert reports[0]["actions"] == ["email"]

    asyncio.run(main())

