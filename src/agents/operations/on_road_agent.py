from ..base_agent import BaseAgent
import importlib
from ...utils.logger import get_logger

logger = get_logger(__name__)

class OnRoadAgent(BaseAgent):
    def __init__(self):
        TMSTool = importlib.import_module("src.tools.operations_tools.tms_tool").TMSTool
        self.tms = TMSTool()

    def run(self, payload: dict) -> dict:
        """Update live location for a shipment."""
        shipment_id = payload["shipment_id"]
        location = payload["location"]
        result = self.tms.update_status(shipment_id, f"enroute:{location}")
        logger.info(f"Updated location for {shipment_id} -> {location}")
        return {"shipment_id": shipment_id, "status": "location_updated", "result": result}
