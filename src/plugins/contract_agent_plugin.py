from typing import Any, Dict
from .base_plugin import BaseToolPlugin


class ContractAgentPlugin(BaseToolPlugin):
    """Send a contract for signature."""

    name = "contract_agent"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        email = payload.get("contact_email")
        print(f"Sending contract to {email}")
        return {"status": "contract_sent", "contact_email": email}
