# Tools/metrics_tools/prometheus_tool.py

import time
import logging
from ...config import settings

try:  # pragma: no cover - optional dependency
    from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
except Exception:  # pragma: no cover - allow running without package
    CollectorRegistry = Gauge = push_to_gateway = None

logger = logging.getLogger(__name__)


class PrometheusPusher:
    def __init__(self, job: str):
        self.registry = CollectorRegistry() if CollectorRegistry else None
        self.job = job

    def push_metric(self, name: str, value: float, labels: dict = None):
        labels = labels or {}
        if not all([Gauge, push_to_gateway, self.registry]):
            logger.warning("prometheus_client not available; skipping metric push")
            return
        gauge = Gauge(
            name,
            f"{name} gauge",
            labelnames=list(labels.keys()),
            registry=self.registry,
        )
        gauge.labels(**labels).set(value)
        timestamp = int(time.time())
        logger.info(f"Pushing metric {name}={value} to Prometheus (job={self.job})")
        push_to_gateway(
            settings.PROMETHEUS_PUSHGATEWAY, job=self.job, registry=self.registry
        )
