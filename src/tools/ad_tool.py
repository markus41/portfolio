"""Utility for creating simple ad campaigns on Facebook and Google."""

import logging
from ..config import settings

logger = logging.getLogger(__name__)


class AdTool:
    def __init__(self):
        # real init would configure SDK clients
        self.facebook_token = settings.FACEBOOK_ACCESS_TOKEN
        self.google_key = settings.GOOGLE_ADS_API_KEY

    def create_facebook_campaign(
        self, name: str, audience_ids: list, budget: int
    ) -> dict:
        logger.info(f"Creating FB campaign {name} for audiences {audience_ids}")
        # TODO: call Facebook Marketing API here
        campaign_id = f"fb_{name.lower().replace(' ','_')}"
        return {"platform": "facebook", "campaign_id": campaign_id, "status": "created"}

    def create_google_campaign(self, name: str, keywords: list, budget: int) -> dict:
        logger.info(f"Creating Google Ads campaign {name} on keywords {keywords}")
        # TODO: call Google Ads API here
        campaign_id = f"ga_{name.lower().replace(' ','_')}"
        return {"platform": "google", "campaign_id": campaign_id, "status": "created"}
