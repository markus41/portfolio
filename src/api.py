from __future__ import annotations

"""HTTP interface exposing :class:`SolutionOrchestrator` via FastAPI."""

from typing import Any, Dict
import os

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel


class Event(BaseModel):
    """Schema for incoming events."""

    type: str
    payload: Dict[str, Any] = {}

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
