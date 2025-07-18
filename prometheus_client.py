class CollectorRegistry:
    pass

class Gauge:
    def __init__(self, name, desc, labelnames=None, registry=None):
        self.name = name
        self.desc = desc
        self.labels = lambda **kw: self
    def set(self, value):
        self.value = value

def push_to_gateway(url, job=None, registry=None):
    pass
