from typing import Any, Dict
from .base_plugin import BaseToolPlugin


class CsatCheckerAgentPlugin(BaseToolPlugin):
    """Send a customer satisfaction survey."""

    name = "csat_checker_agent"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        client_id = payload.get("client_id")
        print(f"CSAT survey for client {client_id}")
        return {"status": "csat_sent", "client_id": client_id}
