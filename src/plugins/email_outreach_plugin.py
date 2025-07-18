from typing import Any, Dict
from .base_plugin import BaseToolPlugin


class EmailOutreachPlugin(BaseToolPlugin):
    """Pretend to send an outreach email."""

    name = "email_outreach"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        lead_id = payload.get("lead_id")
        print(f"Sending outreach email to lead {lead_id}")
        return {"status": "email_sent", "lead_id": lead_id}
