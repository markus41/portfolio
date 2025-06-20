import sys
import types
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


class DummyTemplate:
    """Simple stub for :class:`docxtpl.DocxTemplate` used when the real
    dependency is unavailable."""

    def __init__(self, template_path: str, events: dict):
        self.template_path = template_path
        self._events = events
        self._events["init"] = template_path

    def render(self, context: dict) -> None:
        self._events["context"] = context

    def save(self, output_path: str) -> None:
        self._events["save"] = output_path
        Path(output_path).write_text("generated")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_generate_renders_and_saves(monkeypatch, tmp_path):
    """Verify ``DocGenTool.generate`` renders context and writes a file."""

    events: dict[str, object] = {}

    # Ensure a docxtpl implementation is available; if the real library
    # is missing, provide a minimal stub via ``monkeypatch``.
    monkeypatch.setitem(
        sys.modules,
        "docxtpl",
        types.SimpleNamespace(DocxTemplate=lambda p: DummyTemplate(p, events)),
    )

    from importlib import reload
    from src.tools import docgen_tool

    reload(docgen_tool)  # ensure patched ``docxtpl`` is used on import

    template_path = tmp_path / "template.docx"
    template_path.write_text("unused")

    tool = docgen_tool.DocGenTool(str(template_path))
    output_path = tmp_path / "out.docx"

    result = tool.generate({"name": "Alice"}, str(output_path))

    assert result == str(output_path)
    assert output_path.exists()
    assert events == {
        "init": str(template_path),
        "context": {"name": "Alice"},
        "save": str(output_path),
    }
