from ..base_agent import BaseAgent
import importlib
from ...utils.logger import get_logger

logger = get_logger(__name__)


class TMSAgent(BaseAgent):
    def __init__(self):
        TMSTool = importlib.import_module("src.tools.operations_tools.tms_tool").TMSTool
        self.tms = TMSTool()

    def run(self, payload: dict) -> dict:
        """Update shipment status in the TMS."""
        shipment_id = payload["shipment_id"]
        status = payload["status"]
        result = self.tms.update_status(shipment_id, status)
        logger.info(f"Shipment {shipment_id} updated to {status}")
        return {"shipment_id": shipment_id, "status": "updated", "result": result}
