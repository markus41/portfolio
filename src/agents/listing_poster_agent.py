# src/agents/listing_poster_agent.py

from .base_agent import BaseAgent
from ..tools.real_estate_tools.listing_poster import ListingPoster
from ..utils.logger import get_logger

logger = get_logger(__name__)

class ListingPosterAgent(BaseAgent):
    def __init__(self):
        self.poster = ListingPoster()

    def run(self, payload: dict) -> dict:
        """Post a listing to major real estate portals."""
        res = self.poster.post(payload["listing"])
        return {"result": res}
