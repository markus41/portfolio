"""Standalone HTTP server exposing the ``FileMemoryService`` API via FastAPI."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from ..memory_service.file import FileMemoryService

app = FastAPI(title="Memory Service")

# Initialise backend storage using a path supplied via environment variable.
# Defaults to ``memory.jsonl`` inside the working directory so the container can
# mount a persistent volume.
mem_path = Path(os.getenv("MEMORY_FILE_PATH", "memory.jsonl"))
svc = FileMemoryService(mem_path)


class StorePayload(BaseModel):
    """Payload accepted by the ``/store`` endpoint."""

    key: str
    data: Dict[str, Any]


@app.post("/store")
def store(payload: StorePayload) -> Dict[str, str]:
    """Persist ``payload`` in the ``FileMemoryService``."""
    if not svc.store(payload.key, payload.data):  # pragma: no cover - always true
        raise HTTPException(status_code=500, detail="failed to store record")
    return {"status": "ok"}


@app.get("/fetch")
def fetch(key: str = Query(...), top_k: int = Query(5)) -> List[Dict[str, Any]]:
    """Return previously stored payloads for ``key``."""
    return svc.fetch(key, top_k)


if __name__ == "__main__":  # pragma: no cover - manual execution
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
