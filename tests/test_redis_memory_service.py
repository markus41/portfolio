import types

from src.memory_service.redis import RedisMemoryService, redis as redis_module

class DummyRedis:
    def __init__(self):
        self.store = {}
    def rpush(self, key, value):
        self.store.setdefault(key, []).append(value)
    def lrange(self, key, start, end):
        data = self.store.get(key, [])
        if start < 0:
            start = len(data) + start
        if end == -1:
            end = None
        else:
            end += 1
        return data[start:end]
    def ping(self):
        return True

def test_store_and_fetch(monkeypatch):
    client = DummyRedis()
    monkeypatch.setattr(redis_module.Redis, 'from_url', lambda *a, **k: client)
    svc = RedisMemoryService('redis://localhost')

    assert svc.store('a', {'foo': 1})
    assert svc.store('a', {'bar': 2})
    assert svc.store('b', {'baz': 3})

    assert svc.fetch('a') == [{'foo': 1}, {'bar': 2}]
    assert svc.fetch('a', top_k=1) == [{'bar': 2}]
    assert svc.fetch('missing') == []

