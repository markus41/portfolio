from typing import Any, Dict
from .base_plugin import BaseToolPlugin


class ReferralAgentPlugin(BaseToolPlugin):
    """Request a referral from a client."""

    name = "referral_agent"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        client_id = payload.get("client_id")
        print(f"Requesting referral from {client_id}")
        return {"status": "referral_requested", "client_id": client_id}
