from pathlib import Path
import json
import pytest

from src.workflows.graph import GraphWorkflowDefinition


def _example_graph(tmp_path: Path) -> Path:
    path = tmp_path / "wf.json"
    data = {
        "name": "demo",
        "nodes": [
            {"id": "a", "type": "agent", "label": "A"},
            {"id": "b", "type": "tool", "label": "B"}
        ],
        "edges": [
            {"source": "a", "target": "b"}
        ]
    }
    path.write_text(json.dumps(data))
    return path


def test_load_and_save(tmp_path: Path):
    path = _example_graph(tmp_path)
    wf = GraphWorkflowDefinition.from_file(path)
    assert wf.name == "demo"
    assert len(wf.nodes) == 2
    assert wf.nodes[0].id == "a"
    new_path = tmp_path / "out.json"
    wf.save(new_path)
    loaded = json.loads(new_path.read_text())
    assert loaded["name"] == "demo"


def test_validation_error(tmp_path: Path):
    bad = tmp_path / "bad.json"
    bad.write_text("{}")
    with pytest.raises(ValueError):
        GraphWorkflowDefinition.from_file(bad)
