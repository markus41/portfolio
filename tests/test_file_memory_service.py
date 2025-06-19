import json
from pathlib import Path

from src.memory_service.file import FileMemoryService


def test_store_and_fetch(tmp_path):
    file_path = tmp_path / "mem.jsonl"
    svc = FileMemoryService(file_path)

    assert svc.store("a", {"foo": 1})
    assert svc.store("a", {"bar": 2})
    assert svc.store("b", {"baz": 3})

    all_a = svc.fetch("a")
    assert all_a == [{"foo": 1}, {"bar": 2}]

    last_a = svc.fetch("a", top_k=1)
    assert last_a == [{"bar": 2}]

    none = svc.fetch("missing")
    assert none == []
