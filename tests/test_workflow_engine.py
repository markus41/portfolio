from pathlib import Path

import pytest

from src.workflows.engine import WorkflowEngine


EXAMPLE = Path("src/workflows/examples/content_creation.json")


def test_example_workflow_advances():
    engine = WorkflowEngine.from_file(EXAMPLE)

    assert engine.current == "Research"
    assert not engine.is_complete()

    assert engine.advance() == "Draft"
    assert engine.advance() == "Edit"
    assert engine.advance() == "Send"
    assert engine.is_complete()

    with pytest.raises(StopIteration):
        engine.advance()

    engine.reset()
    assert engine.current == "Research"
