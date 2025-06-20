import sys
import types

# Provide a minimal 'requests' stub so importing the memory client does not fail
requests_stub = sys.modules.setdefault(
    "requests",
    types.SimpleNamespace(
        post=lambda *a, **k: types.SimpleNamespace(),
        HTTPError=Exception,
        RequestException=Exception,
    ),
)

from src.tools.memory_tools.memory_client import MemoryClient


class DummyResponse:
    """Simple stand-in for ``requests.Response`` used in tests."""

    def __init__(self, data=None):
        self.data = data or {}

    def json(self):
        return self.data


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _patch_post(monkeypatch, capture):
    def fake_post(url, json=None, headers=None):
        capture.append({'url': url, 'json': json, 'headers': headers})
        return DummyResponse({'ok': True})
    monkeypatch.setattr(
        'src.tools.memory_tools.memory_client.requests.post',
        fake_post,
        raising=False,
    )


def _patch_get(monkeypatch, capture):
    def fake_get(url, params=None, headers=None):
        capture.append({'url': url, 'params': params, 'headers': headers})
        return DummyResponse({'result': True})
    monkeypatch.setattr(
        'src.tools.memory_tools.memory_client.requests.get',
        fake_get,
        raising=False,
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_store(monkeypatch):
    calls = []
    _patch_post(monkeypatch, calls)
    client = MemoryClient('http://api', 'tok')

    resp = client.store('s3://x', {'a': 1})

    assert isinstance(resp, DummyResponse)
    assert calls == [
        {
            'url': 'http://api/store',
            'json': {'blob_uri': 's3://x', 'metadata': {'a': 1}},
            'headers': {'Authorization': 'Bearer tok'},
        }
    ]


def test_retrieve(monkeypatch):
    calls = []
    _patch_get(monkeypatch, calls)
    client = MemoryClient('http://api', 'tok')

    result = client.retrieve('cats', k=3, filters={'tag': 't'})

    assert result == {'result': True}
    assert calls == [
        {
            'url': 'http://api/retrieve',
            'params': {'query': 'cats', 'k': 3, 'filters': {'tag': 't'}},
            'headers': {'Authorization': 'Bearer tok'},
        }
    ]


def test_forget(monkeypatch):
    calls = []
    _patch_post(monkeypatch, calls)
    client = MemoryClient('http://api', 'tok')

    client.forget('id123')

    assert calls == [
        {
            'url': 'http://api/forget',
            'json': {'doc_id': 'id123'},
            'headers': {'Authorization': 'Bearer tok'},
        }
    ]


def test_push_fact(monkeypatch):
    calls = []
    _patch_post(monkeypatch, calls)
    client = MemoryClient('http://api', 'tok')

    fact = {'foo': 'bar'}
    client.push_fact(fact)

    assert calls == [
        {
            'url': 'http://api/push_fact',
            'json': fact,
            'headers': {'Authorization': 'Bearer tok'},
        }
    ]

