from typing import Any, Dict
from .base_plugin import BaseToolPlugin


class LeadEnrichmentPlugin(BaseToolPlugin):
    """Mock enrichment step adding firmographic data."""

    name = "lead_enrichment"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        lead_id = payload.get("lead_id")
        print(f"Enriching lead {lead_id}")
        return {"status": "enriched", "lead_id": lead_id}
