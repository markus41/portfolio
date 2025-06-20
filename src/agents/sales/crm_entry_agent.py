# src/agents/crm_entry_agent.py

from ..base_agent import BaseAgent
from ...tools.crm_tools.crm_tool import CRMTool
import logging

logger = logging.getLogger(__name__)


class CRMEntryAgent(BaseAgent):
    def run(self, payload):
        """
        payload: {
          "email": str,
          "first_name": str,
          "last_name": str,
          "company": str
        }
        """
        # check duplicate
        if CRMTool.find_duplicate(payload["email"]):
            logger.info("Duplicate found, updating record")
            # update flow here...
            contact = CRMTool.create_contact(payload)  # or update_contact
        else:
            logger.info("No duplicate, creating new contact")
            contact = CRMTool.create_contact(payload)
        return {"contact_id": contact.get("id"), "status": "created_or_updated"}
