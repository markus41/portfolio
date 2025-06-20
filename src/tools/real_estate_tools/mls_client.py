"""Client for retrieving MLS data via REST."""

try:
    import requests
except ImportError:  # pragma: no cover - optional dependency
    requests = None
from ...config import settings
import logging

logger = logging.getLogger(__name__)


class MLSClient:
    """Client for querying MLS data."""

    def pull_listing(self, mls_id: str) -> dict:
        logger.info(f"Pulling MLS listing {mls_id}")
        if not requests:
            raise RuntimeError("requests package is not installed")
        resp = requests.get(
            f"{settings.MLS_API_URL}/listings/{mls_id}",
            headers={"Authorization": f"Bearer {settings.MLS_API_KEY}"},
        )
        resp.raise_for_status()
        return resp.json()
