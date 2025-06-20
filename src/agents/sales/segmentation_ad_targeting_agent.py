"""Create ad campaigns for multiple audience segments."""

from ..base_agent import BaseAgent
import importlib
import logging
from ...events import SegmentationEvent

logger = logging.getLogger(__name__)


class SegmentationAdTargetingAgent(BaseAgent):
    def __init__(self):
        AdTool = importlib.import_module("src.tools.ad_tool").AdTool
        self.ad_tool = AdTool()

    def run(self, payload: SegmentationEvent) -> dict:
        """Create campaigns for each audience segment."""

        results = []
        for seg in payload.segments:
            name = seg["name"]
            crit = seg["criteria"]
            # choose platform per segment or both
            # create campaigns on each advertising platform
            fb = self.ad_tool.create_facebook_campaign(
                name,
                crit.get("facebook_audiences", []),
                payload.budget_per_segment,
            )
            ga = self.ad_tool.create_google_campaign(
                name,
                crit.get("google_keywords", []),
                payload.budget_per_segment,
            )
            results.append({"segment": name, "facebook": fb, "google": ga})
        logger.info("Completed segmentation & ad targeting")
        return {"targeting_results": results}
