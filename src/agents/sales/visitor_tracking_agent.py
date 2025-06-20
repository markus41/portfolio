# src/agents/visitor_tracking_agent.py

from ..base_agent import BaseAgent
import logging
from ...tools.visitor_tracking_tools import AnalyticsClient

logger = logging.getLogger(__name__)


class VisitorTrackingAgent(BaseAgent):
    """Log visitor data and forward it to the configured analytics service."""

    def __init__(self) -> None:
        self.analytics = AnalyticsClient()

    def run(self, payload):
        """Process a visitor event.

        Parameters
        ----------
        payload: dict
            ``{"visitor_id": str, "page": str, "timestamp": str}``

        Returns
        -------
        dict
            Includes ``status`` and ``analytics_sent`` boolean flag.
        """

        logger.info(
            "Tracked visitor %s at %s", payload.get("visitor_id"), payload.get("page")
        )

        try:
            sent = self.analytics.track(payload)
        except Exception as exc:  # pragma: no cover - analytics client bug
            logger.error("Analytics client failure: %s", exc)
            sent = False

        return {"status": "logged", "analytics_sent": sent, **payload}
