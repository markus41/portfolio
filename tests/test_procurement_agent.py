from decimal import Decimal

from agentic_core import EventBus

from src.suppliers import BaseSupplierAdapter, Quote
from src.agents.procurement_agent import ProcurementAgent, MAX_AUTO_APPROVAL


class DummySupplier(BaseSupplierAdapter):
    def __init__(self, supplier_id: str, price: str, days: int) -> None:
        self.supplier_id = supplier_id
        self._price = Decimal(price)
        self._days = days

    def get_quote(self, item: str, qty: int) -> Quote:
        return Quote(self.supplier_id, self._price * qty, self._days)


def test_auto_order(monkeypatch):
    bus = EventBus()
    ordered = []
    bus.subscribe("Procurement.Ordered", ordered.append)

    s1 = DummySupplier("s1", "100", 5)
    s2 = DummySupplier("s2", "120", 6)
    agent = ProcurementAgent(bus, [s1, s2])
    monkeypatch.setattr(agent, "_gpt_decide", lambda prompt: {
        "supplier_id": "s1",
        "reason": "lowest",
        "requires_approval": False,
    })

    result = agent.run({"item": "cement", "qty": 10, "target_days": 7})
    assert result["status"] == "ordered"
    assert ordered[0]["supplier_id"] == "s1"


def test_needs_approval(monkeypatch):
    bus = EventBus()
    pending = []
    bus.subscribe("Procurement.PendingApproval", pending.append)

    s1 = DummySupplier("s1", "6000", 5)
    agent = ProcurementAgent(bus, [s1])
    monkeypatch.setattr(agent, "_gpt_decide", lambda prompt: {
        "supplier_id": "s1",
        "reason": "expensive",
        "requires_approval": True,
    })

    result = agent.run({"item": "steel", "qty": 10, "target_days": 7})
    assert result["status"] == "pending_approval"
    assert Decimal(pending[0]["price"]) > MAX_AUTO_APPROVAL
