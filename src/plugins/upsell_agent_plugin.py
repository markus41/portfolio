from typing import Any, Dict
from .base_plugin import BaseToolPlugin


class UpsellAgentPlugin(BaseToolPlugin):
    """Offer an upsell to an existing client."""

    name = "upsell_agent"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        client_id = payload.get("client_id")
        print(f"Sending upsell offer to {client_id}")
        return {"status": "upsell_sent", "client_id": client_id}
