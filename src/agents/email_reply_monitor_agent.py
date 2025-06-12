# src/agents/email_reply_monitor_agent.py

from .base_agent import BaseAgent
from ..tools.crm_tools.hubspot_tool import HubSpotTool
from ..utils.logger import get_logger

logger = get_logger(__name__)

class EmailReplyMonitorAgent(BaseAgent):
    def __init__(self):
        self.hubspot = HubSpotTool()

    def run(self, payload):
        """
        payload: {
          "contact_email": str
        }
        """
        email = payload["contact_email"]
        logger.info(f"Checking if {email} replied")
        contact = self.hubspot.get_contact_by_email(email)
        # stub logic — replace with real email/thread check
        replied = bool(contact and contact.get("properties", {}).get("last_email_reply") == "true")
        outcome = "positive_reply" if replied else "no_response"
        return {"outcome": outcome}
