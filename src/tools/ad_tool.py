"""Utility for creating simple ad campaigns on Facebook and Google."""

import logging
from typing import Any, Dict, Optional

import requests
from ..config import settings

logger = logging.getLogger(__name__)


class AdTool:
    def __init__(self):
        # real init would configure SDK clients
        self.facebook_token = settings.FACEBOOK_ACCESS_TOKEN
        self.google_key = settings.GOOGLE_ADS_API_KEY

    def create_facebook_campaign(
        self, name: str, audience_ids: list, budget: int
    ) -> Dict[str, Optional[Any]]:
        """Create a basic Facebook campaign.

        Parameters
        ----------
        name:
            Human friendly campaign name.
        audience_ids:
            Facebook custom audience identifiers.
        budget:
            Daily budget in the smallest currency unit.

        Returns
        -------
        dict
            ``{"platform": "facebook", "campaign_id": str | None, "status": str, "message": str | None}``
        """

        logger.info(
            "Creating FB campaign %s for audiences %s", name, audience_ids
        )
        payload = {
            "name": name,
            "audience_ids": audience_ids,
            "daily_budget": budget,
        }
        headers = {"Authorization": f"Bearer {self.facebook_token}"}
        url = "https://graph.facebook.com/v17.0/campaigns"

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            campaign_id = data.get("id")
            status = data.get("status", "created")
            return {
                "platform": "facebook",
                "campaign_id": campaign_id,
                "status": status,
                "message": None,
            }
        except requests.RequestException as exc:
            logger.error("Facebook campaign creation failed: %s", exc)
            return {
                "platform": "facebook",
                "campaign_id": None,
                "status": "error",
                "message": str(exc),
            }

    def create_google_campaign(
        self, name: str, keywords: list, budget: int
    ) -> Dict[str, Optional[Any]]:
        """Create a basic Google Ads campaign.

        Parameters
        ----------
        name:
            Name for the new campaign.
        keywords:
            List of keywords to target.
        budget:
            Daily budget in micros.

        Returns
        -------
        dict
            ``{"platform": "google", "campaign_id": str | None, "status": str, "message": str | None}``
        """

        logger.info(
            "Creating Google Ads campaign %s on keywords %s", name, keywords
        )
        payload = {"name": name, "keywords": keywords, "daily_budget": budget}
        params = {"key": self.google_key}
        url = "https://googleads.googleapis.com/v14/campaigns"

        try:
            resp = requests.post(url, json=payload, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            campaign_id = data.get("id")
            status = data.get("status", "created")
            return {
                "platform": "google",
                "campaign_id": campaign_id,
                "status": status,
                "message": None,
            }
        except requests.RequestException as exc:
            logger.error("Google Ads campaign creation failed: %s", exc)
            return {
                "platform": "google",
                "campaign_id": None,
                "status": "error",
                "message": str(exc),
            }
