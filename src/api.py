from __future__ import annotations

"""HTTP interface exposing :class:`SolutionOrchestrator` via FastAPI."""

from typing import Any, Dict, List, Literal
import os
import json

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel
from pathlib import Path


class Event(BaseModel):
    """Schema for incoming events."""

    type: str
    payload: Dict[str, Any] = {}


class NodeModel(BaseModel):
    """Representation of a workflow node."""

    id: str
    type: Literal["agent", "tool"]
    label: str
    config: Dict[str, Any] = {}


class EdgeModel(BaseModel):
    """Representation of a workflow edge."""

    source: str
    target: str
    label: str | None = None
    id: str | None = None


class WorkflowModel(BaseModel):
    """Schema for graph workflows."""

    name: str
    nodes: List[NodeModel]
    edges: List[EdgeModel]

from .solution_orchestrator import SolutionOrchestrator
from .config import settings


def create_app(orchestrator: SolutionOrchestrator | None = None) -> FastAPI:
    """Return a configured :class:`FastAPI` app bound to ``orchestrator``.

    Parameters
    ----------
    orchestrator:
        Instance of :class:`SolutionOrchestrator` to dispatch requests to. If
        omitted an orchestrator with no teams is created.
    """

    app = FastAPI(title="Brookside API", description="SolutionOrchestrator HTTP interface")
    orch = orchestrator or SolutionOrchestrator({})
    workflow_dir = Path(__file__).resolve().parent / "workflows" / "saved"

    async def _auth(x_api_key: str = Header(...)) -> None:
        required = settings.API_AUTH_KEY
        if required and x_api_key != required:
            raise HTTPException(status_code=401, detail="invalid api key")

    @app.post("/teams/{name}/event")
    async def handle_event(name: str, event: Event, _=Depends(_auth)) -> Dict[str, Any]:
        """Dispatch ``event`` to ``name`` via the orchestrator."""
        result = await orch.handle_event(name, event.dict())
        if result.get("status") == "unknown_team":
            raise HTTPException(status_code=404, detail="unknown team")
        orch.report_status(name, "handled")
        return result

    @app.get("/teams/{name}/status")
    def get_status(name: str, _=Depends(_auth)) -> Dict[str, Any]:
        """Return the last reported status for ``name``."""
        status = orch.get_status(name)
        if status is None:
            raise HTTPException(status_code=404, detail="unknown team")
        return {"team": name, "status": status}

    @app.get("/activity")
    def get_activity(limit: int = 10, _=Depends(_auth)) -> Dict[str, Any]:
        """Return recent orchestrator activity."""
        return {"activity": orch.get_recent_activity(limit)}

    @app.post("/workflows", status_code=201)
    def save_workflow(workflow: WorkflowModel, _=Depends(_auth)) -> Dict[str, Any]:
        """Persist ``workflow`` to disk for later execution."""

        workflow_dir.mkdir(parents=True, exist_ok=True)
        path = workflow_dir / f"{workflow.name}.json"
        path.write_text(workflow.json(indent=2))
        return {"status": "saved", "path": str(path)}

    @app.get("/workflows/{name}")
    def load_workflow(name: str, _=Depends(_auth)) -> Dict[str, Any]:
        """Return a previously saved workflow."""

        path = workflow_dir / f"{name}.json"
        if not path.exists():
            raise HTTPException(status_code=404, detail="unknown workflow")
        return json.loads(path.read_text())

    return app


app = create_app()

if __name__ == "__main__":  # pragma: no cover - manual execution
    import sys
    import uvicorn

    def _parse_team_mapping(pairs: list[str]) -> dict[str, str]:
        mapping: dict[str, str] = {}
        for pair in pairs:
            if "=" not in pair:
                raise SystemExit(f"Invalid team spec '{pair}'. Use NAME=PATH")
            name, path = pair.split("=", 1)
            mapping[name] = path
        return mapping

    teams = _parse_team_mapping(sys.argv[1:])
    orch = SolutionOrchestrator(teams)
    app = create_app(orch)

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
