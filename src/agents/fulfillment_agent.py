from .base_agent import BaseAgent
import importlib
from ..utils.logger import get_logger

logger = get_logger(__name__)

class FulfillmentAgent(BaseAgent):
    def __init__(self):
        EcommerceTool = importlib.import_module("src.tools.ecommerce_tool").EcommerceTool
        InventoryTool = importlib.import_module("src.tools.operations_tools.inventory_tool").InventoryTool
        self.ecommerce = EcommerceTool()
        self.inventory = InventoryTool()

    def run(self, payload: dict) -> dict:
        """Fulfill an e-commerce order."""
        order = self.ecommerce.get_order(payload["order_id"])
        for item in order.get("items", []):
            self.inventory.update_inventory(item["sku"], -item["qty"])
        logger.info(f"Fulfilled order {payload['order_id']}")
        return {"order_id": payload["order_id"], "status": "fulfilled"}
