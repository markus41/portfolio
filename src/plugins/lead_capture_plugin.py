from typing import Any, Dict
from .base_plugin import BaseToolPlugin


class LeadCapturePlugin(BaseToolPlugin):
    """Capture raw lead data and return a simple acknowledgement."""

    name = "lead_capture"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        print(f"Captured lead: {payload}")
        return {"status": "captured", "lead": payload}
