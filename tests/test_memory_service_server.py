from pathlib import Path

import pytest

from src.tools import memory_service_server
from src.tools.memory_service_server import StorePayload
from src.memory_service.file import FileMemoryService


def setup_mem(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    mem = FileMemoryService(tmp_path / "data.jsonl")
    monkeypatch.setattr(memory_service_server, "svc", mem)


def test_store_and_fetch(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    setup_mem(tmp_path, monkeypatch)

    payload = StorePayload(key="a", data={"foo": 1})
    memory_service_server.store(payload)
    assert memory_service_server.fetch("a", 1) == [{"foo": 1}]
    assert memory_service_server.fetch("missing", 5) == []
