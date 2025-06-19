# Tools/metrics_tools/prometheus_tool.py

import time
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from ...utils.logger import get_logger
from ...config import settings

logger = get_logger(__name__)

class PrometheusPusher:
    def __init__(self, job: str):
        self.registry = CollectorRegistry()
        self.job = job

    def push_metric(self, name: str, value: float, labels: dict = None):
        labels = labels or {}
        gauge = Gauge(name, f"{name} gauge", labelnames=list(labels.keys()), registry=self.registry)
        gauge.labels(**labels).set(value)
        timestamp = int(time.time())
        logger.info(f"Pushing metric {name}={value} to Prometheus (job={self.job})")
        push_to_gateway(settings.PROMETHEUS_PUSHGATEWAY, job=self.job, registry=self.registry)
