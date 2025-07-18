import multiprocessing
import time

from src.event_bus.redis import redis as redis_module
from src.event_bus import RedisEventBus


class DummyServer:
    """Cross-process pub/sub store using a shared queue."""

    def __init__(self, manager):
        self.queue = manager.Queue()

    def publish(self, channel, message):
        self.queue.put((channel, message))

    def listen(self, channels):
        while True:
            channel, message = self.queue.get()
            if channel in channels:
                yield {"type": "message", "channel": channel, "data": message}


class DummyRedis:
    def __init__(self, server):
        self.server = server

    def ping(self):
        return True

    def publish(self, channel, message):
        self.server.publish(channel, message)

    def pubsub(self, ignore_subscribe_messages=True):
        server = self.server
        class PS:
            def __init__(self):
                self.channels = []
            def subscribe(self, *chs):
                self.channels.extend(chs)
            def listen(self):
                return server.listen(self.channels)
        return PS()


def _publish(url, server):
    redis_module.Redis.from_url = lambda *a, **k: DummyRedis(server)
    bus = RedisEventBus(url)
    bus.publish("demo", {"x": 1})
    time.sleep(0.2)


def test_cross_process_publish(monkeypatch):
    manager = multiprocessing.Manager()
    server = DummyServer(manager)
    monkeypatch.setattr(redis_module.Redis, "from_url", lambda *a, **k: DummyRedis(server))

    bus = RedisEventBus("redis://x")
    received = []
    bus.subscribe("demo", lambda p: received.append(p))

    p = multiprocessing.Process(target=_publish, args=("redis://x", server))
    p.start()
    p.join(timeout=3)
    assert p.exitcode == 0

    deadline = time.time() + 2
    while not received and time.time() < deadline:
        time.sleep(0.05)

    assert received == [{"x": 1}]

