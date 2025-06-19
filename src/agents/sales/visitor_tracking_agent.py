# src/agents/visitor_tracking_agent.py

from ..base_agent import BaseAgent
from ...utils.logger import get_logger

logger = get_logger(__name__)


class VisitorTrackingAgent(BaseAgent):
    def run(self, payload):
        # payload: { "visitor_id": "...", "page": "...", "timestamp": "..." }
        logger.info(f"Tracked visitor {payload['visitor_id']} at {payload['page']}")
        # TODO: integrate FingerprintJS or analytics SDK
        return {"status": "logged", **payload}
