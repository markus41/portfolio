# src/agents/upsell_agent.py

from ..base_agent import BaseAgent
from ...tools.email_tool import EmailTool
import logging

logger = logging.getLogger(__name__)


class UpsellAgent(BaseAgent):
    def __init__(self):
        self.email = EmailTool()

    def run(self, payload):
        """
        payload: {
          "to": str,
          "product_suggestion": str,
          "reason": str
        }
        """
        body = f"We thought you might like {payload['product_suggestion']} because {payload['reason']}."
        sent = self.email.send_email(
            to_email=payload["to"], subject="Recommended for you", html_content=body
        )
        return {"status": "upsell_sent" if sent else "failed"}
