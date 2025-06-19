# src/agents/lead_enrichment_agent.py

from ..base_agent import BaseAgent
import requests
from ...utils.logger import get_logger
from ...config import settings

logger = get_logger(__name__)


class LeadEnrichmentAgent(BaseAgent):
    def run(self, payload):
        # payload: {"email": "...", "name": "..."}
        logger.info(f"Enriching lead {payload.get('email')}")
        resp = requests.get(
            "https://person.clearbit.com/v2/people/find",
            params={"email": payload["email"]},
            headers={"Authorization": f"Bearer {settings.CLEARBIT_API_KEY}"},
        )
        if resp.status_code == 200:
            enriched = resp.json()
            return {"status": "enriched", "data": enriched}
        logger.warning("Enrichment failed or not found")
        return {"status": "not_found"}
