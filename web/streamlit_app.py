import json
import os
from pathlib import Path
from typing import Dict, List

import requests
import streamlit as st


API_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
API_KEY = os.environ.get("API_KEY", "")
TEAM_DIR = Path(__file__).resolve().parent.parent / "src" / "teams"


def load_team_configs(directory: Path = TEAM_DIR) -> Dict[str, List[str]]:
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
    url = f"{API_URL}/teams/{team}/event"
    headers = {"X-API-Key": API_KEY} if API_KEY else {}
    return requests.post(
        url, json={"type": event_type, "payload": payload}, headers=headers
    )


def get_status(team: str) -> requests.Response:
    """Fetch status for ``team`` from the backend."""
    url = f"{API_URL}/teams/{team}/status"
    headers = {"X-API-Key": API_KEY} if API_KEY else {}
    return requests.get(url, headers=headers)


# ---------------------------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------------------------


def main() -> None:
    """Launch the interactive Streamlit UI."""
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
