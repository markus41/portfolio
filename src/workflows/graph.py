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


class GraphWorkflowEngine:
    """Execute :class:`GraphWorkflowDefinition` nodes in topological order.

    Each node ``config`` dictionary may specify a ``team`` and ``event`` entry.
    During synchronous execution these are passed to
    :meth:`~src.solution_orchestrator.SolutionOrchestrator.handle_event_sync`.
    Asynchronous flows use :meth:`~src.solution_orchestrator.SolutionOrchestrator.handle_event`.
    Nodes without either field are treated as no-ops.
    """

    def __init__(self, definition: GraphWorkflowDefinition) -> None:
        if not definition.nodes:
            raise ValueError("workflow must contain at least one node")
        self.definition = definition
        self._node_map = {n.id: n for n in definition.nodes}

        # Track incoming edge counts for topological ordering
        self._incoming: dict[str, int] = {n.id: 0 for n in definition.nodes}
        for edge in definition.edges:
            if edge.source not in self._node_map or edge.target not in self._node_map:
                raise ValueError("edge references unknown node")
            self._incoming[edge.target] += 1

        self._queue: list[str] = [n for n, deg in self._incoming.items() if deg == 0]
        if not self._queue:
            raise ValueError("workflow has no starting node or contains a cycle")

    def step(self, orchestrator: "SolutionOrchestrator") -> dict:
        """Execute the next queued node and return the result."""

        if not self._queue:
            raise StopIteration("workflow complete")

        node_id = self._queue.pop(0)
        node = self._node_map[node_id]
        team = node.config.get("team")
        event = node.config.get("event")

        if team and event:
            result = orchestrator.handle_event_sync(team, event)
        else:  # pragma: no cover - simple branch
            result = {"status": "noop"}

        for edge in self.definition.edges:
            if edge.source == node_id:
                tgt = edge.target
                self._incoming[tgt] -= 1
                if self._incoming[tgt] == 0:
                    self._queue.append(tgt)

        return {"node": node_id, "team": team, "result": result}

    async def async_step(self, orchestrator: "SolutionOrchestrator") -> dict:
        """Asynchronously execute the next queued node."""

        if not self._queue:
            raise StopAsyncIteration("workflow complete")

        node_id = self._queue.pop(0)
        node = self._node_map[node_id]
        team = node.config.get("team")
        event = node.config.get("event")

        if team and event:
            result = await orchestrator.handle_event(team, event)
        else:  # pragma: no cover - simple branch
            result = {"status": "noop"}

        for edge in self.definition.edges:
            if edge.source == node_id:
                tgt = edge.target
                self._incoming[tgt] -= 1
                if self._incoming[tgt] == 0:
                    self._queue.append(tgt)

        return {"node": node_id, "team": team, "result": result}

    def run(self, orchestrator: "SolutionOrchestrator") -> dict:
        """Execute all nodes sequentially until finished."""

        results = []
        while True:
            try:
                results.append(self.step(orchestrator))
            except (StopIteration, StopAsyncIteration):
                break
        return {"status": "complete", "results": results}

    async def async_run(self, orchestrator: "SolutionOrchestrator") -> dict:
        """Asynchronously execute all nodes sequentially."""

        results = []
        while True:
            try:
                results.append(await self.async_step(orchestrator))
            except (StopIteration, StopAsyncIteration):
                break
        return {"status": "complete", "results": results}
