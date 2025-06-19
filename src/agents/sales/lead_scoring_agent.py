# src/agents/lead_scoring_agent.py

from ..base_agent import BaseAgent
from ...utils.logger import get_logger
from ...tools.scheduler_tool import SchedulerTool  # example import if needed

logger = get_logger(__name__)


class LeadScoringAgent(BaseAgent):
    def run(self, payload):
        """
        payload: {
            "email": str,
            "company_size": int,
            "industry": str,
            "annual_revenue": float
        }
        """
        score = 0
        # simple rule-based scoring
        if payload["company_size"] > 1000:
            score += 30
        if payload["annual_revenue"] > 1e6:
            score += 30
        if payload["industry"].lower() in ("software", "finance"):
            score += 20
        # engagement metric
        score += payload.get("engagement_level", 0)  # e.g. 0–20
        logger.info(f"Lead {payload['email']} scored {score}")
        return {"email": payload["email"], "score": score}
