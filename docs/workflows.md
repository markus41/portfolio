# Workflow Engine

The workflow engine provides a tiny state machine for moving through a series of
steps defined in JSON or YAML. Each workflow file contains a list of step names
and an optional `name` field. The `WorkflowEngine` loads this definition and
exposes methods to query the current step, advance to the next one and reset the
flow.

## Definition Format

```json
{
  "name": "content_creation",
  "steps": ["Research", "Draft", "Edit", "Send"]
}
```

Save the file anywhere on disk and load it using
`WorkflowEngine.from_file(path)`.

## Basic Usage

```python
from src.workflows.engine import WorkflowEngine

engine = WorkflowEngine.from_file("path/to/workflow.json")
print(engine.current)  # -> first step
engine.advance()       # move to next
```

`advance()` raises `StopIteration` once the workflow reaches the final step.
Call `reset()` to start over.

## Example

The repository ships with a ready-made workflow at
`src/workflows/examples/content_creation.json`. The unit tests demonstrate how to
walk through the steps using the engine.

## Graph Workflows

For more complex flows you can describe nodes and edges explicitly. The
[`frontend`](../frontend) editor exports a graph conforming to the JSON schema in
[`workflow_schema.json`](workflow_schema.json). Each node represents an `agent`
or `tool` and edges model the execution order. Persist the file via the `/workflows`
endpoint and load it later with `GraphWorkflowDefinition.from_file()`.

### Executing Graph Workflows

`GraphWorkflowEngine` walks the graph in topological order and dispatches each
node through `SolutionOrchestrator`. A node's ``config`` must include a
``team`` name and an ``event`` dictionary which are forwarded to
``SolutionOrchestrator.handle_event_sync``.

```python
from src.solution_orchestrator import SolutionOrchestrator
from src.workflows.graph import GraphWorkflowDefinition

orch = SolutionOrchestrator({"A": "team_a.json"})
wf = GraphWorkflowDefinition.from_file("workflows/my_flow.json")
orch.execute_workflow(wf)
```

``execute_workflow`` returns a dictionary containing the orchestrator results
for every node.
