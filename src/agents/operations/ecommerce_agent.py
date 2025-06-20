from ..base_agent import BaseAgent
import importlib
import logging

logger = logging.getLogger(__name__)


class EcommerceAgent(BaseAgent):
    def __init__(self):
        EcommerceTool = importlib.import_module(
            "src.tools.ecommerce_tool"
        ).EcommerceTool
        self.ecommerce = EcommerceTool()

    def run(self, payload: dict) -> dict:
        """Create a new ecommerce order."""
        order = self.ecommerce.create_order(payload["order"])
        logger.info(f"Created ecommerce order {order.get('id')}")
        return {"order_id": order.get("id"), "status": "created"}
