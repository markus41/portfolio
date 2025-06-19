# src/agents/referral_agent.py

from ..base_agent import BaseAgent
from ...tools.email_tool import EmailTool
from ...utils.logger import get_logger

logger = get_logger(__name__)

class ReferralAgent(BaseAgent):
    def __init__(self):
        self.email = EmailTool()

    def run(self, payload):
        """
        payload: {
          "to": str,
          "referral_link": str
        }
        """
        html = f"Thanks for working with us! Share your experience: <a href='{payload['referral_link']}'>Refer a friend</a>"
        sent = self.email.send_email(to_email=payload["to"], subject="Refer & Earn", html_content=html)
        return {"status": "referral_sent" if sent else "failed"}
