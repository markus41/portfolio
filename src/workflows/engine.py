from __future__ import annotations

"""Simple workflow engine implemented as a sequential state machine."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - PyYAML is optional
    yaml = None


@dataclass
class WorkflowDefinition:
    """Representation of a workflow loaded from JSON or YAML."""

    name: str
    steps: List[str]


class WorkflowEngine:
    """State machine that walks through a series of steps."""

    def __init__(self, definition: WorkflowDefinition) -> None:
        if not definition.steps:
            raise ValueError("Workflow must contain at least one step")
        self.definition = definition
        self._index = 0

    @classmethod
    def from_file(cls, path: str | Path) -> "WorkflowEngine":
        """Load a workflow definition from a JSON or YAML file."""

        path = Path(path)
        text = path.read_text()
        if path.suffix in {".yaml", ".yml"}:
            if yaml is None:
                raise ModuleNotFoundError(
                    "PyYAML is required to load YAML workflow definitions"
                )
            data = yaml.safe_load(text)
        else:
            data = json.loads(text)
        name = data.get("name", path.stem)
        steps = data.get("steps")
        if not isinstance(steps, list) or not all(isinstance(s, str) for s in steps):
            raise ValueError(
                "Invalid workflow definition: 'steps' must be a list of strings"
            )
        definition = WorkflowDefinition(name=name, steps=steps)
        return cls(definition)

    @property
    def current(self) -> str:
        """Return the current step name."""

        return self.definition.steps[self._index]

    def advance(self) -> str:
        """Move to the next step and return its name."""

        if self.is_complete():
            raise StopIteration("Workflow already finished")
        self._index += 1
        return self.current

    def reset(self) -> None:
        """Restart the workflow from the first step."""

        self._index = 0

    def is_complete(self) -> bool:
        """Return ``True`` if the workflow has reached the last step."""

        return self._index >= len(self.definition.steps) - 1
