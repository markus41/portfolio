"""Agent that pulls listing data from the MLS."""

from .base_agent import BaseAgent
from ..tools.real_estate_tools.mls_client import MLSClient
from ..utils.logger import get_logger

logger = get_logger(__name__)

class MLSAgent(BaseAgent):
    def __init__(self):
        self.client = MLSClient()

    def run(self, payload: dict) -> dict:
        """Pull an MLS listing by ID."""
        # delegate to the real MLS client which does the HTTP call
        listing = self.client.pull_listing(payload["mls_id"])
        return {"listing": listing}
