from ..base_agent import BaseAgent
import importlib
import logging

logger = logging.getLogger(__name__)


class OutboundAgent(BaseAgent):
    def __init__(self):
        TMSTool = importlib.import_module("src.tools.operations_tools.tms_tool").TMSTool
        InventoryTool = importlib.import_module(
            "src.tools.operations_tools.inventory_tool"
        ).InventoryTool
        self.tms = TMSTool()
        self.inventory = InventoryTool()

    def run(self, payload: dict) -> dict:
        """Process an outbound trailer and decrement inventory."""
        for item in payload.get("items", []):
            self.inventory.update_inventory(item["sku"], -item["qty"])
        shipment = self.tms.create_shipment(
            {"trailer_id": payload["trailer_id"], "direction": "outbound"}
        )
        logger.info(f"Processed outbound trailer {payload['trailer_id']}")
        return {"shipment_id": shipment.get("id"), "status": "outbound_processed"}
