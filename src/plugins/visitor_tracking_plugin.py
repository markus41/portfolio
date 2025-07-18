from typing import Any, Dict
from .base_plugin import BaseToolPlugin


class VisitorTrackingPlugin(BaseToolPlugin):
    """Log visitor behaviour."""

    name = "visitor_tracking"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        print(f"Tracking visitor: {payload}")
        return {"status": "tracked", "visitor": payload}
