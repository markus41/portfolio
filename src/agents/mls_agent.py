# src/agents/mls_agent.py

from .base_agent import BaseAgent
from ..tools.real_estate_tools.mls_client import MLSClient
from ..utils.logger import get_logger

logger = get_logger(__name__)

class MLSAgent(BaseAgent):
    def __init__(self):
        self.client = MLSClient()

    def run(self, payload: dict) -> dict:
        """Pull an MLS listing by ID."""
        listing = self.client.pull_listing(payload["mls_id"])
        return {"listing": listing}
