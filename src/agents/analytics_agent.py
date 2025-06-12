from .base_agent import BaseAgent
from ..tools.metrics_tools.prometheus_tool import PrometheusPusher
from ..utils.logger import get_logger

logger = get_logger(__name__)


class AnalyticsAgent(BaseAgent):
    """Push metrics to Prometheus via PrometheusPusher."""

    def __init__(self, job: str = "analytics"):
        self.pusher = PrometheusPusher(job)

    def run(self, payload: dict) -> dict:
        """Push a metric defined in the payload."""
        metric = payload.get("metric")
        value = payload.get("value", 1)
        labels = payload.get("labels", {})
        logger.info("AnalyticsAgent pushing metric %s=%s", metric, value)
        self.pusher.push_metric(metric, value, labels)
        return {"status": "pushed"}
