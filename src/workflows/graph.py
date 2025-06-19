from __future__ import annotations

"""Utilities for loading and saving graph-based workflows.

The expected JSON structure is defined in :doc:`workflow_schema.json` and is
compatible with the objects emitted by the ReactFlow editor.
"""

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

NodeType = Literal["agent", "tool"]


@dataclass
class NodeDefinition:
    """Represents an agent or tool node in the graph."""

    id: str
    type: NodeType
    label: str
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EdgeDefinition:
    """Connection between two nodes in the workflow graph."""

    source: str
    target: str
    label: Optional[str] = None
    id: Optional[str] = None


@dataclass
class GraphWorkflowDefinition:
    """Complete workflow graph consisting of nodes and edges."""

    name: str
    nodes: List[NodeDefinition]
    edges: List[EdgeDefinition]

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serialisable representation."""

        return {
            "name": self.name,
            "nodes": [asdict(n) for n in self.nodes],
            "edges": [asdict(e) for e in self.edges],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GraphWorkflowDefinition":
        """Create an instance from ``data`` after validation."""

        if not isinstance(data.get("name"), str):
            raise ValueError("workflow 'name' must be a string")
        if not isinstance(data.get("nodes"), list):
            raise ValueError("workflow 'nodes' must be a list")
        if not isinstance(data.get("edges"), list):
            raise ValueError("workflow 'edges' must be a list")

        nodes = []
        for node in data["nodes"]:
            if not isinstance(node, dict):
                raise ValueError("node must be an object")
            if node.get("type") not in {"agent", "tool"}:
                raise ValueError("node type must be 'agent' or 'tool'")
            nodes.append(NodeDefinition(**node))

        edges = []
        for edge in data["edges"]:
            if not isinstance(edge, dict):
                raise ValueError("edge must be an object")
            if not edge.get("source") or not edge.get("target"):
                raise ValueError("edge must contain source and target")
            edges.append(EdgeDefinition(**edge))

        return cls(name=data["name"], nodes=nodes, edges=edges)

    @classmethod
    def from_file(cls, path: str | Path) -> "GraphWorkflowDefinition":
        """Load a workflow from ``path``."""

        data = json.loads(Path(path).read_text())
        return cls.from_dict(data)

    def save(self, path: str | Path) -> None:
        """Persist the workflow to ``path`` as JSON."""

        Path(path).write_text(json.dumps(self.to_dict(), indent=2))
