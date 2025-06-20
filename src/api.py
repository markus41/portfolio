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

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from .user_settings import (
    UserSettingsData,
    init_db,
    get_settings,
    upsert_settings,
)
from .user_context import use_settings


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


class SettingsModel(BaseModel):
    """Incoming user configuration payload."""

    organization: str | None = None
    openai_api_key: str | None = None
    crm_api_url: str | None = None
    crm_api_key: str | None = None
    email_service_api_key: str | None = None
    disabled_teams: List[str] | None = None


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

    app = FastAPI(
        title="Brookside API", description="SolutionOrchestrator HTTP interface"
    )
    orch = orchestrator or SolutionOrchestrator({})
    db_url = settings.DB_CONNECTION_STRING or "sqlite:///user_settings.db"
    init_db(db_url)
    workflow_dir = Path(__file__).resolve().parent / "workflows" / "saved"

    async def _auth(request: Request, x_api_key: str | None = Header(None)) -> None:
        """Validate API key from header or ``api_key`` query parameter."""

        required = settings.API_AUTH_KEY
        supplied = x_api_key or request.query_params.get("api_key")
        if required and supplied != required:
            raise HTTPException(status_code=401, detail="invalid api key")

    @app.post("/teams/{name}/event")
    async def handle_event(
        name: str, event: Event, x_api_key: str | None = Header(None), _=Depends(_auth)
    ) -> Dict[str, Any]:
        """Dispatch ``event`` to ``name`` via the orchestrator."""

        user_cfg = get_settings(x_api_key or "")
        if user_cfg and user_cfg.disabled_teams and name in user_cfg.disabled_teams:
            raise HTTPException(status_code=404, detail="team disabled")

        with use_settings(user_cfg):
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

    @app.post("/settings", status_code=200)
    def save_settings(
        payload: SettingsModel, x_api_key: str | None = Header(None), _=Depends(_auth)
    ) -> None:
        """Persist configuration for the requesting user."""

        data = UserSettingsData(api_key=x_api_key or "", **payload.dict())
        upsert_settings(x_api_key or "", data)

    @app.get("/settings")
    def load_settings(x_api_key: str | None = Header(None), _=Depends(_auth)) -> Dict[str, Any]:
        """Return stored configuration for the requesting user."""

        cfg = get_settings(x_api_key or "")
        return cfg.dict() if cfg else {}

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
