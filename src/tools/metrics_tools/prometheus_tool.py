class PrometheusPusher:
    """Simplified Prometheus pusher used for tests."""

    def __init__(self, job: str):
        self.job = job

    def push_metric(self, name: str, value: float, labels: dict | None = None):
        # Real implementation would push to Prometheus
        pass
