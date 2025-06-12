"""HTTP client for fetching lead data from a real estate provider."""

try:
    import requests
except ImportError:  # pragma: no cover - optional dependency
    requests = None
from ...constants import RE_LEADS_API_URL, RE_LEADS_API_KEY
from ...utils.logger import get_logger

logger = get_logger(__name__)

class LeadFinder:
    """Fetch potential real estate leads from an external provider."""

    def search_leads(self, city: str) -> list[dict]:
        logger.info(f"Searching leads in {city}")
        if not requests:
            raise RuntimeError("requests package is not installed")
        resp = requests.get(
            RE_LEADS_API_URL,
            params={"city": city},
            headers={"Authorization": f"Bearer {RE_LEADS_API_KEY}"},
        )
        resp.raise_for_status()
        return resp.json().get("results", [])
