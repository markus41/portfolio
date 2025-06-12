"""Construct simple listing dictionaries for property data."""

from .base_agent import BaseAgent
from ..utils.logger import get_logger

logger = get_logger(__name__)

class ListingAgent(BaseAgent):
    def run(self, payload: dict) -> dict:
        """Create a property listing payload."""
        # normalise the listing fields we care about
        listing = {
            "address": payload["address"],
            "price": payload["price"],
            "details": payload.get("details", ""),
        }
        logger.info(f"Created listing for {listing['address']}")
        return {"listing": listing}
