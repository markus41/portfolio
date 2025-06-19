"""Agent that posts real estate listings to external portals."""

from ..base_agent import BaseAgent
from ...tools.real_estate_tools.listing_poster import ListingPoster
from ...utils.logger import get_logger

logger = get_logger(__name__)


class ListingPosterAgent(BaseAgent):
    """Use :class:`ListingPoster` to publish property listings."""

    def __init__(self):
        # ListingPoster wraps the actual API calls to the real estate portals
        self.poster = ListingPoster()

    def run(self, payload: dict) -> dict:
        """Publish ``payload['listing']`` using :class:`ListingPoster`."""
        # delegate posting to the underlying ListingPoster helper
        res = self.poster.post(payload["listing"])
        return {"result": res}
