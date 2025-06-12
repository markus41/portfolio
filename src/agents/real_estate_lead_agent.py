"""Locate potential real-estate buyers or sellers."""

from .base_agent import BaseAgent
from ..tools.real_estate_tools.lead_finder import LeadFinder
from ..utils.logger import get_logger

logger = get_logger(__name__)

class RealEstateLeadAgent(BaseAgent):
    def __init__(self):
        self.finder = LeadFinder()

    def run(self, payload: dict) -> dict:
        """Find potential leads in a given city."""
        city = payload.get("city", "")
        # delegate to LeadFinder which performs the actual API call
        leads = self.finder.search_leads(city)
        return {"leads": leads}
