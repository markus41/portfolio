from src.agents.operations.inbound_agent import InboundAgent
from src.agents.operations.inventory_management_agent import InventoryManagementAgent
from src.agents.operations.tms_agent import TMSAgent


def test_inbound_agent(monkeypatch):
    class DummyTMS:
        def create_shipment(self, data):
            return {"id": "ship1"}
    class DummyInv:
        def update_inventory(self, item_id, qty):
            return {"id": item_id, "qty": qty}
    monkeypatch.setattr("src.tools.operations_tools.tms_tool.TMSTool", DummyTMS)
    monkeypatch.setattr("src.tools.operations_tools.inventory_tool.InventoryTool", DummyInv)
    agent = InboundAgent()
    out = agent.run({"trailer_id": "T1", "items": [{"sku": "A", "qty": 2}]})
    assert out["status"] == "inbound_processed"
    assert out["shipment_id"] == "ship1"


def test_inventory_management_agent(monkeypatch):
    class DummyInv:
        def update_inventory(self, item_id, qty):
            return {"id": item_id, "qty": qty}
    monkeypatch.setattr("src.tools.operations_tools.inventory_tool.InventoryTool", DummyInv)
    agent = InventoryManagementAgent()
    out = agent.run({"item_id": "A", "qty": 5})
    assert out["status"] == "updated"
    assert out["item_id"] == "A"


def test_tms_agent(monkeypatch):
    class DummyTMS:
        def update_status(self, sid, status):
            return {"ok": True}
    monkeypatch.setattr("src.tools.operations_tools.tms_tool.TMSTool", DummyTMS)
    agent = TMSAgent()
    out = agent.run({"shipment_id": "S1", "status": "delivered"})
    assert out["status"] == "updated"
    assert out["shipment_id"] == "S1"
