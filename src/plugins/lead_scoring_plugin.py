from typing import Any, Dict
from .base_plugin import BaseToolPlugin


class LeadScoringPlugin(BaseToolPlugin):
    """Return a static lead score."""

    name = "lead_scoring"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        lead_id = payload.get("lead_id")
        print(f"Scoring lead {lead_id}")
        return {"status": "scored", "lead_id": lead_id, "score": 80}
