# src/agents/segmentation_ad_targeting_agent.py

from .base_agent import BaseAgent
import importlib
from ..utils.logger import get_logger

logger = get_logger(__name__)

class SegmentationAdTargetingAgent(BaseAgent):
    def __init__(self):
        AdTool = importlib.import_module("src.tools.ad_tool").AdTool
        self.ad_tool = AdTool()

    def run(self, payload: dict) -> dict:
        """
        payload: {
          "segments": [
            {"name": str, "criteria": {...}},
            ...
          ],
          "budget_per_segment": int
        }
        """
        results = []
        for seg in payload["segments"]:
            name = seg["name"]
            crit = seg["criteria"]
            # choose platform per segment or both
            fb = self.ad_tool.create_facebook_campaign(name, crit.get("facebook_audiences", []), payload["budget_per_segment"])
            ga = self.ad_tool.create_google_campaign(name, crit.get("google_keywords", []), payload["budget_per_segment"])
            results.append({"segment": name, "facebook": fb, "google": ga})
        logger.info("Completed segmentation & ad targeting")
        return {"targeting_results": results}
