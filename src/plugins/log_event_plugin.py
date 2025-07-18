from typing import Any, Dict
from .base_plugin import BaseToolPlugin


class LogEventPlugin(BaseToolPlugin):
    """Print event details to stdout for debugging."""

    name = "log_event"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        event_id = payload.get("event_id")
        step = payload.get("step")
        print({"event_id": event_id, "step": step, "payload": payload.get("payload")})
        return {"status": "logged"}
