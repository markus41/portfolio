# src/agents/csat_checker_agent.py

from .base_agent import BaseAgent
from ..tools.email_tool import EmailTool
from ..utils.logger import get_logger

logger = get_logger(__name__)

class CSATCheckerAgent(BaseAgent):
    def __init__(self):
        self.email = EmailTool()

    def run(self, payload):
        """
        payload: {
          "to": str,
          "survey_link": str
        }
        """
        html = f"Please fill our CSAT survey: <a href='{payload['survey_link']}'>here</a>"
        sent = self.email.send_email(to_email=payload["to"], subject="How did we do?", html_content=html)
        logger.info(f"CSAT sent: {sent}")
        return {"status": "survey_sent" if sent else "failed"}
