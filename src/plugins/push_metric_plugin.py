from typing import Any, Dict
from .base_plugin import BaseToolPlugin


class PushMetricPlugin(BaseToolPlugin):
    """Log metric values to stdout."""

    name = "push_metric"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        metric = payload.get("metric")
        value = payload.get("value")
        labels = payload.get("labels")
        print({"metric": metric, "value": value, "labels": labels})
        return {"status": "queued"}
