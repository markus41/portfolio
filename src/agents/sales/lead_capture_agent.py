"""Extract and normalise lead form submissions."""

from ..base_agent import BaseAgent
import logging
from ...events import LeadCaptureEvent
import re

logger = logging.getLogger(__name__)


class LeadCaptureAgent(BaseAgent):
    def run(self, payload: LeadCaptureEvent) -> dict:
        """Normalise lead capture fields."""

        data = payload.form_data
        email = data.get("Email") or data.get("email") or ""
        name = data.get("Name") or data.get("name") or ""
        # normalize phone numbers
        phone = data.get("Phone", "")
        phone_norm = re.sub(r"\D", "", phone)
        captured = {
            "email": email.lower(),
            "name": name.strip(),
            "phone": phone_norm,
            "source": payload.source,
        }
        logger.info(f"Captured lead {captured['email']} from {captured['source']}")
        return {"status": "captured", "lead": captured}
