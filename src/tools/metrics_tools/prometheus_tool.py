# Tools/metrics_tools/prometheus_tool.py

import time
import logging

try:  # pragma: no cover - optional dependency
    from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
except Exception:  # pragma: no cover - dependency missing
    CollectorRegistry = None
    Gauge = None
    push_to_gateway = None

from ...config import settings

logger = logging.getLogger(__name__)


class PrometheusPusher:
    def __init__(self, job: str):
        if CollectorRegistry is None:
            self.registry = None
        else:
            self.registry = CollectorRegistry()
        self.job = job

    def push_metric(self, name: str, value: float, labels: dict = None):
        if self.registry is None or Gauge is None or push_to_gateway is None:
            logger.debug("Prometheus client not available; skipping metric push")
            return

        labels = labels or {}
        gauge = Gauge(
            name,
            f"{name} gauge",
            labelnames=list(labels.keys()),
            registry=self.registry,
        )
        gauge.labels(**labels).set(value)
        timestamp = int(time.time())
        logger.info(
            f"Pushing metric {name}={value} to Prometheus (job={self.job})"
        )
        push_to_gateway(
            settings.PROMETHEUS_PUSHGATEWAY,
            job=self.job,
            registry=self.registry,
        )
