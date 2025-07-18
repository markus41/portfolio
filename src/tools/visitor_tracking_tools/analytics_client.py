# Tools/visitor_tracking_tools/analytics_client.py
"""Simple HTTP client for forwarding visitor data to an analytics service."""

from __future__ import annotations

import time
from typing import Any

import requests

from ...config import settings
import logging

logger = logging.getLogger(__name__)


class AnalyticsClient:
    """Send visitor tracking data to an external analytics endpoint."""

    def __init__(self) -> None:
        self.endpoint = settings.VISITOR_ANALYTICS_URL
        self.api_key = settings.VISITOR_ANALYTICS_KEY

    def track(self, data: dict[str, Any], retries: int = 3) -> bool:
        """POST ``data`` to the configured endpoint.

        Parameters
        ----------
        data:
            Visitor payload to forward.
        retries:
            Number of attempts before giving up. Sleeps one second between
            attempts.

        Returns
        -------
        bool
            ``True`` if the request succeeded, ``False`` otherwise.
        """

        if not self.endpoint:
            logger.warning("VISITOR_ANALYTICS_URL not configured; skipping send")
            return False

        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}

        for attempt in range(1, retries + 1):
            try:
                resp = requests.post(
                    self.endpoint, json=data, headers=headers, timeout=5
                )
                resp.raise_for_status()
                logger.info("Visitor analytics sent successfully (attempt %s)", attempt)
                return True
            except Exception as exc:  # pragma: no cover - network failures
                logger.error("Analytics send failed on attempt %s: %s", attempt, exc)
                time.sleep(1)
        return False
