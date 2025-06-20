# src/agents/negotiation_agent.py

from ..base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)


class NegotiationAgent(BaseAgent):
    def run(self, payload):
        """
        payload: {
          "quoted_price": float,
          "requested_discount_pct": float
        }
        """
        max_discount = 10  # maximum 10%
        approved = min(payload["requested_discount_pct"], max_discount)
        final_price = payload["quoted_price"] * (1 - approved / 100)
        logger.info(f"Approved discount: {approved}%, final price: {final_price}")
        return {"approved_discount_pct": approved, "final_price": final_price}
