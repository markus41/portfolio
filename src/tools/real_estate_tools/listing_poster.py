"""Post property listings to an external portal."""

try:
    import requests
except ImportError:  # pragma: no cover - optional dependency
    requests = None
from ...config import settings
from ...utils.logger import get_logger

logger = get_logger(__name__)


class ListingPoster:
    """Post real estate listings to major websites."""

    def post(self, listing: dict) -> dict:
        logger.info("Posting listing to portals")
        if not requests:
            raise RuntimeError("requests package is not installed")
        resp = requests.post(
            settings.LISTING_POST_API_URL,
            json=listing,
            headers={"Authorization": f"Bearer {settings.LISTING_POST_API_KEY}"},
        )
        resp.raise_for_status()
        return resp.json()
