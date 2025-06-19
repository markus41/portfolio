import requests
from ...config import settings
from ...utils.logger import get_logger

logger = get_logger(__name__)

class LeadEnrichmentTool:
    """Query Clearbit enrichment API."""

    def enrich(self, email: str) -> dict | None:
        logger.info(f"Enriching lead {email}")
        resp = requests.get(
            "https://person.clearbit.com/v2/people/find",
            params={"email": email},
            headers={"Authorization": f"Bearer {settings.CLEARBIT_API_KEY}"},
        )
        if resp.status_code == 200:
            return resp.json()
        logger.warning("Enrichment failed or not found")
        return None
