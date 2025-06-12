from .base_agent import BaseAgent
from ..tools.metrics_tools.prometheus_tool import PrometheusPusher
from ..utils.logger import get_logger

logger = get_logger(__name__)

class AnalyticsAgent(BaseAgent):
    def __init__(self):
        self.pusher = PrometheusPusher(job="sales_analytics")

    def run(self, payload: dict) -> dict:
        """Push a metric to Prometheus via the PrometheusPusher tool.

        payload: {"metric": str, "value": float, "labels": {str: str}}
        """
        metric = payload.get("metric")
        value = float(payload.get("value", 0))
        labels = payload.get("labels", {})
        self.pusher.push_metric(metric, value, labels)
        logger.info(f"Pushed metric {metric}={value}")
        return {"status": "pushed"}
