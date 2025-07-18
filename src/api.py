from __future__ import annotations

"""HTTP interface exposing :class:`SolutionOrchestrator` via FastAPI.

This module supports being executed directly as ``python src/api.py`` or via
``python -m src.api``. When run as a script the ``src`` package may not be on
``sys.path`` which breaks the relative imports below. The bootstrap logic adds
the project root to ``sys.path`` so the package layout remains valid in both
scenarios. This mirrors the behaviour of ``python -m`` but allows direct script
execution as well.
"""

from pathlib import Path
import os
import sys

if __package__ in {None, ""}:  # pragma: no cover - safe for direct execution
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    __package__ = "src"

from typing import Any, Dict, List, Literal
import json
import asyncio
import types

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .utils.logging_config import setup_logging
from .utils.team_mapping import parse_team_mapping

try:  # pragma: no cover - optional dependency
    import jsonschema
except Exception:  # pragma: no cover - optional dependency
    from .jsonschema_stub import validate as _validate, ValidationError as _VE

    jsonschema = types.SimpleNamespace(validate=_validate, ValidationError=_VE)


_WF_SCHEMA_PATH = Path(__file__).resolve().parent.parent / "docs" / "workflow_schema.json"
try:  # pragma: no cover - schema may be missing
    _WORKFLOW_SCHEMA = json.loads(_WF_SCHEMA_PATH.read_text())
except FileNotFoundError:  # pragma: no cover - schema missing
    _WORKFLOW_SCHEMA = {}


def validate_workflow(data: Dict[str, Any]) -> None:
    """Validate ``data`` against :mod:`docs/workflow_schema.json`."""

    if _WORKFLOW_SCHEMA and jsonschema is not None:
        jsonschema.validate(data, _WORKFLOW_SCHEMA)


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
from . import db


def create_app(orchestrator: SolutionOrchestrator | None = None) -> FastAPI:
    """Return a configured :class:`FastAPI` app bound to ``orchestrator``.

    Parameters
    ----------
    orchestrator:
        Instance of :class:`SolutionOrchestrator` to dispatch requests to. If
        omitted an orchestrator with no teams is created.
    """

    app = FastAPI(
        title="Brookside API", description="SolutionOrchestrator HTTP interface"
    )

    db.init_db()
    orch = orchestrator or SolutionOrchestrator({})

    @app.on_event("startup")
    async def _startup() -> None:
        await orch.__aenter__()

    @app.on_event("shutdown")
    async def _shutdown() -> None:
        await orch.__aexit__(None, None, None)

    origins = (
        [o.strip() for o in settings.ALLOWED_ORIGINS.split(",")]
        if settings.ALLOWED_ORIGINS and settings.ALLOWED_ORIGINS != "*"
        else ["*"]
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    workflow_dir = Path(__file__).resolve().parent / "workflows" / "saved"

    async def _auth(request: Request, x_api_key: str | None = Header(None)) -> None:
        """Validate API key from header or ``api_key`` query parameter."""

        required = settings.API_AUTH_KEY
        supplied = x_api_key or request.query_params.get("api_key")
        if required and supplied != required:
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

    @app.get("/teams/{name}/stream")
    async def stream(name: str, request: Request, _=Depends(_auth)):
        """Server-Sent Events stream of status and activity messages."""

        queue = orch.subscribe(name)

        async def event_generator():
            try:
                current = orch.get_status(name)
                if current is not None:
                    payload = json.dumps({"status": current})
                    yield f"event: status\ndata: {payload}\n\n"
                while True:
                    if await request.is_disconnected():
                        break
                    try:
                        msg = await asyncio.wait_for(queue.get(), 1.0)
                    except asyncio.TimeoutError:
                        continue
                    yield f"event: {msg['type']}\ndata: {json.dumps(msg)}\n\n"
            finally:
                orch.unsubscribe(name, queue)

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    @app.get("/activity")
    def get_activity(limit: int = 10, _=Depends(_auth)) -> Dict[str, Any]:
        """Return recent orchestrator activity."""
        return {"activity": orch.get_recent_activity(limit)}

    @app.get("/history")
    def get_history(
        limit: int = 10, offset: int = 0, _=Depends(_auth)
    ) -> Dict[str, Any]:
        """Return persisted event history from the database."""
        items = db.fetch_history(limit=limit, offset=offset)
        return {"history": items}

    @app.post("/workflows", status_code=201)
    def save_workflow(workflow: Dict[str, Any], _=Depends(_auth)) -> Dict[str, Any]:
        """Persist ``workflow`` to disk for later execution.

        The payload is validated against :mod:`docs/workflow_schema.json`.
        """

        data = workflow
        try:
            validate_workflow(data)
        except jsonschema.ValidationError as exc:
            raise HTTPException(
                status_code=400, detail=f"invalid workflow: {exc.message}"
            ) from exc

        workflow_dir.mkdir(parents=True, exist_ok=True)
        name = data.get("name", "")
        path = workflow_dir / f"{name}.json"
        path.write_text(json.dumps(data, indent=2))
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

    try:
        teams = parse_team_mapping(sys.argv[1:])
    except ValueError as exc:
        raise SystemExit(str(exc))
    orch = SolutionOrchestrator(teams)
    app = create_app(orch)
    setup_logging()

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
