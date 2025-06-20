from ..base_agent import BaseAgent
import importlib
import logging

logger = logging.getLogger(__name__)


class InventoryManagementAgent(BaseAgent):
    def __init__(self):
        InventoryTool = importlib.import_module(
            "src.tools.operations_tools.inventory_tool"
        ).InventoryTool
        self.inventory = InventoryTool()

    def run(self, payload: dict) -> dict:
        """Update inventory counts."""
        item_id = payload["item_id"]
        qty = int(payload.get("qty", 0))
        result = self.inventory.update_inventory(item_id, qty)
        logger.info(f"Inventory updated for {item_id}")
        return {"item_id": item_id, "status": "updated", "result": result}
