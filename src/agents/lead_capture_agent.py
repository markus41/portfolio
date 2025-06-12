# src/agents/lead_capture_agent.py

from .base_agent import BaseAgent
from ..utils.logger import get_logger
import re

logger = get_logger(__name__)

class LeadCaptureAgent(BaseAgent):
    def run(self, payload: dict) -> dict:
        """
        payload: {
          "form_data": { "Email": "...", "Name": "...", ... },
          "source": str
        }
        """
        data = payload["form_data"]
        email = data.get("Email") or data.get("email") or ""
        name  = data.get("Name") or data.get("name") or ""
        # normalize phone numbers
        phone = data.get("Phone", "")
        phone_norm = re.sub(r"\D", "", phone)
        captured = {"email": email.lower(), "name": name.strip(), "phone": phone_norm, "source": payload["source"]}
        logger.info(f"Captured lead {captured['email']} from {captured['source']}")
        return {"status": "captured", "lead": captured}
