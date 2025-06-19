import pytest

from src.utils.retry import retry_tool


def test_retry_success():
    attempts = {"count": 0}

    @retry_tool(retries=2)
    def flaky():
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise ValueError("fail")
        return "ok"

    result = flaky()
    assert result == "ok"
    assert attempts["count"] == 3


def test_retry_fallback():
    history = []

    def fallback(exc, args, kwargs):
        history.append("fallback")
        return "fb"

    @retry_tool(retries=1, fallback=fallback)
    def always_fail():
        history.append("call")
        raise RuntimeError("boom")

    assert always_fail() == "fb"
    assert history == ["call", "call", "fallback"]


def test_retry_raises():
    @retry_tool(retries=1)
    def boom():
        raise RuntimeError("kaboom")

    with pytest.raises(RuntimeError):
        boom()


def test_retry_delay(monkeypatch):
    recorded = []

    def fake_sleep(seconds):
        recorded.append(seconds)

    monkeypatch.setattr("src.utils.retry.sleep", fake_sleep)

    @retry_tool(retries=1, delay=0.2)
    def fail_once():
        raise ValueError("nope")

    with pytest.raises(ValueError):
        fail_once()

    assert recorded == [0.2]
