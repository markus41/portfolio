# src/agents/outreach_agent.py

from ..base_agent import BaseAgent
from ...tools.email_tool import EmailTool
import logging

logger = logging.getLogger(__name__)


class OutreachAgent(BaseAgent):
    def __init__(self):
        self.email_tool = EmailTool()

    def run(self, payload):
        # payload: {"to": "...", "subject": "...", "body": "..."}
        logger.info(f"Outreach to {payload['to']}")
        success = self.email_tool.send_email(
            to_email=payload["to"],
            subject=payload["subject"],
            html_content=payload["body"],
        )
        return {"status": "sent" if success else "failed"}
