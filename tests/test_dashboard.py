from __future__ import annotations

import json
import socket
import threading
import time
import types
import sys
from pathlib import Path
from urllib import request as urllib_request

from src import api
from src.solution_orchestrator import SolutionOrchestrator
from src.agents.base_agent import BaseAgent


class EchoAgent(BaseAgent):
    """Simple agent used for testing."""

    def run(self, payload: dict) -> dict:
        return {"echo": payload}


def _register_agent() -> None:
    mod = types.ModuleType("src.agents.echo_agent")
    mod.EchoAgent = EchoAgent
    sys.modules["src.agents.echo_agent"] = mod


def _write_team(tmp_path: Path) -> Path:
    cfg = {
        "provider": "autogen.agentchat.teams.RoundRobinGroupChat",
        "responsibilities": ["echo_agent"],
        "config": {"participants": [{"config": {"name": "echo_agent"}}]},
    }
    path = tmp_path / "team.json"
    path.write_text(json.dumps(cfg))
    return path


def _get_free_port() -> int:
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def _http_post(url: str, data: dict, headers: dict[str, str]) -> tuple[int, str]:
    payload = json.dumps(data).encode()
    req = urllib_request.Request(url, data=payload, headers=headers, method="POST")
    req.add_header("Content-Type", "application/json")
    with urllib_request.urlopen(req) as resp:  # noqa: S310 -- tests
        return resp.getcode(), resp.read().decode()


def _start_server(app, port: int):
    import uvicorn

    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="error")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    for _ in range(100):
        try:
            urllib_request.urlopen(f"http://127.0.0.1:{port}/docs")
            return server, thread
        except Exception:
            time.sleep(0.1)
    server.should_exit = True
    thread.join(timeout=5)
    raise RuntimeError("server failed to start")


def test_dashboard_event_submission(tmp_path: Path) -> None:
    """Submitting an event should return the agent's result."""

    _register_agent()
    team_cfg = _write_team(tmp_path)
    port = _get_free_port()
    orch = SolutionOrchestrator({"demo": str(team_cfg)})
    api.settings.API_AUTH_KEY = "secret"
    app = api.create_app(orch)
    server, thread = _start_server(app, port)

    try:
        code, body = _http_post(
            f"http://127.0.0.1:{port}/teams/demo/event",
            {"type": "echo_agent", "payload": {"foo": 1}},
            headers={"X-API-Key": "secret"},
        )
        assert code == 200
        result = json.loads(body)
        assert result["status"] == "done"
        assert result["result"]["echo"]["foo"] == 1
    finally:
        server.should_exit = True
        thread.join(timeout=5)


def test_stream_endpoint(tmp_path: Path) -> None:
    """The /stream endpoint should emit activity and status events."""

    _register_agent()
    team_cfg = _write_team(tmp_path)
    port = _get_free_port()
    orch = SolutionOrchestrator({"demo": str(team_cfg)})
    api.settings.API_AUTH_KEY = "secret"
    app = api.create_app(orch)
    server, thread = _start_server(app, port)

    stream_url = f"http://127.0.0.1:{port}/teams/demo/stream?api_key=secret"
    req = urllib_request.Request(stream_url)
    try:
        resp = urllib_request.urlopen(req, timeout=5)
        events: list[dict] = []

        def reader() -> None:
            while len(events) < 2:
                line = resp.readline().decode().strip()
                if line.startswith("data:"):
                    payload = json.loads(line.split("data: ", 1)[1])
                    events.append(payload)

        t = threading.Thread(target=reader)
        t.start()
        time.sleep(0.2)

        _http_post(
            f"http://127.0.0.1:{port}/teams/demo/event",
            {"type": "echo_agent", "payload": {"foo": 2}},
            headers={"X-API-Key": "secret"},
        )
        t.join(timeout=5)

        types = {e.get("type") for e in events}
        assert "activity" in types
        assert any(e.get("status") == "handled" for e in events)
    finally:
        server.should_exit = True
        thread.join(timeout=5)
