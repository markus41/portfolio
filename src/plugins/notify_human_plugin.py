from typing import Any, Dict
from .base_plugin import BaseToolPlugin


class NotifyHumanPlugin(BaseToolPlugin):
    """Output a severity-tagged message for manual review."""

    name = "notify_human"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        severity = payload.get("severity", "info")
        message = payload.get("message", "")
        print(f"[{severity.upper()}] {message}")
        return {"status": "sent", "severity": severity}
