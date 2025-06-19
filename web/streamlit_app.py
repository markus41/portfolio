"""Simple Streamlit UI for launching Brookside workflows.

The module exposes helper functions for interacting with the HTTP API and a
``main`` function which renders the interface.  The UI reads configuration from
environment variables so it can easily be pointed at different API instances.

Environment variables
---------------------
``BACKEND_URL``: Base URL for the FastAPI backend (default
``http://localhost:8000``).

``API_KEY``: Optional authentication key sent in the ``X-API-Key`` header.

``TEAM_DIR``: Directory containing team JSON files.  Defaults to
``src/teams`` relative to the repository root.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import requests
import streamlit as st


@dataclass
class Settings:
    """Configuration derived from environment variables."""

    api_url: str
    api_key: str
    team_dir: Path

    def __init__(self) -> None:  # noqa: D401 - simple initializer
        """Load values from ``os.environ``."""
        self.api_url = os.environ.get("BACKEND_URL", "http://localhost:8000")
        self.api_key = os.environ.get("API_KEY", "")
        self.team_dir = Path(
            os.environ.get(
                "TEAM_DIR",
                (Path(__file__).resolve().parent.parent / "src" / "teams"),
            )
        )


settings = Settings()


def load_team_configs(directory: Path = settings.team_dir) -> Dict[str, List[str]]:
    """Return mapping of team names to available event types.

    Parameters
    ----------
    directory:
        Folder containing team JSON files.
    """
    teams: Dict[str, List[str]] = {}
    for file in directory.glob("*.json"):
        try:
            data = json.loads(file.read_text())
        except json.JSONDecodeError:
            continue
        responsibilities = data.get("responsibilities", [])
        teams[file.stem] = responsibilities
    return teams


def send_event(team: str, event_type: str, payload: Dict) -> requests.Response:
    """POST ``payload`` to the backend for ``team`` using ``event_type``."""
    url = f"{settings.api_url}/teams/{team}/event"
    headers = {"X-API-Key": settings.api_key} if settings.api_key else {}
    try:
        return requests.post(
            url, json={"type": event_type, "payload": payload}, headers=headers
        )
    except requests.RequestException as exc:  # pragma: no cover - network errors
        raise RuntimeError(f"Request failed: {exc}") from exc


def get_status(team: str) -> requests.Response:
    """Fetch status for ``team`` from the backend."""
    url = f"{settings.api_url}/teams/{team}/status"
    headers = {"X-API-Key": settings.api_key} if settings.api_key else {}
    try:
        return requests.get(url, headers=headers)
    except requests.RequestException as exc:  # pragma: no cover - network errors
        raise RuntimeError(f"Request failed: {exc}") from exc


# ---------------------------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------------------------


def main() -> None:
    """Launch the interactive Streamlit UI.

    The user is prompted to choose a workflow and event type.  The JSON payload
    is sent to the backend specified by :class:`Settings`.  Results and the
    latest status are displayed inline.
    """
    st.title("Brookside Workflow Launcher")

    teams = load_team_configs()
    if not teams:
        st.error("No teams found in src/teams")
        return

    team = st.selectbox("Select workflow", sorted(teams.keys()))
    events = teams.get(team, [])

    if events:
        event_type = st.selectbox("Event type", events)
    else:
        event_type = st.text_input("Event type")

    payload_text = st.text_area("Payload (JSON)", "{}")

    if st.button("Launch"):
        try:
            payload = json.loads(payload_text) if payload_text.strip() else {}
        except json.JSONDecodeError as exc:
            st.error(f"Invalid JSON payload: {exc}")
        else:
            resp = send_event(team, event_type, payload)
            if resp.ok:
                st.success(resp.json())
                status_resp = get_status(team)
                if status_resp.ok:
                    st.info(f"Status: {status_resp.json().get('status')}")
                else:
                    st.warning(f"Failed to fetch status: {status_resp.text}")
            else:
                st.error(f"Error {resp.status_code}: {resp.text}")


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
