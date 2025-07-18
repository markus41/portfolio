from typing import Any, Dict
from .base_plugin import BaseToolPlugin


class GenerateProposalPlugin(BaseToolPlugin):
    """Produce a proposal document for a client."""

    name = "generate_proposal"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        client_id = payload.get("client_id")
        deal_details = payload.get("deal_details")
        print(f"Generating proposal for {client_id} with {deal_details}")
        return {"status": "generated", "client_id": client_id}
