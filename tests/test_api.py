from __future__ import annotations

import json
import os
import socket
import threading
import sys
import time
import types
from pathlib import Path

from urllib import request as urllib_request

from src.solution_orchestrator import SolutionOrchestrator
from src import api

def _http_get(url: str, headers: dict[str, str] | None = None) -> tuple[int, str]:
    req = urllib_request.Request(url, headers=headers or {})
    try:
        with urllib_request.urlopen(req) as resp:  # noqa: S310 -- in tests
            return resp.getcode(), resp.read().decode()
    except urllib_request.HTTPError as err:  # type: ignore[attr-defined]
        return err.code, err.read().decode()


def _http_post(url: str, data: dict, headers: dict[str, str] | None = None) -> tuple[int, str]:
    payload = json.dumps(data).encode()
    req = urllib_request.Request(url, data=payload, headers=headers or {}, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib_request.urlopen(req) as resp:  # noqa: S310 -- in tests
            return resp.getcode(), resp.read().decode()
    except urllib_request.HTTPError as err:  # type: ignore[attr-defined]
        return err.code, err.read().decode()

from src.agents.base_agent import BaseAgent


class EchoAgent(BaseAgent):
    def run(self, payload):
        return {"echo": payload}


def _write_team(tmp_path: Path) -> Path:
    cfg = {
        "responsibilities": ["echo_agent"],
        "config": {"participants": [{"config": {"name": "echo_agent"}}]},
    }
    path = tmp_path / "team.json"
    path.write_text(json.dumps(cfg))
    return path


def _register_agent():
    mod = types.ModuleType("src.agents.echo_agent")
    mod.EchoAgent = EchoAgent
    sys.modules["src.agents.echo_agent"] = mod


def _get_free_port() -> int:
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def _start_server(app, port: int):
    import uvicorn

    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="error")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    for _ in range(100):
        try:
            _http_get(f"http://127.0.0.1:{port}/docs")
            return server, thread
        except Exception:
            time.sleep(0.1)
    server.should_exit = True
    thread.join(timeout=5)
    raise RuntimeError("server failed to start")


def test_event_and_status(tmp_path):
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
        assert json.loads(body)["result"]["echo"]["foo"] == 1

        code, body = _http_get(
            f"http://127.0.0.1:{port}/teams/demo/status",
            headers={"X-API-Key": "secret"},
        )
        assert code == 200
        assert json.loads(body)["status"] == "handled"
    finally:
        server.should_exit = True
        thread.join(timeout=5)


def test_auth_failure(tmp_path):
    _register_agent()
    team_cfg = _write_team(tmp_path)
    port = _get_free_port()
    orch = SolutionOrchestrator({"demo": str(team_cfg)})
    api.settings.API_AUTH_KEY = "secret"
    app = api.create_app(orch)
    server, thread = _start_server(app, port)

    try:
        code, _ = _http_post(
            f"http://127.0.0.1:{port}/teams/demo/event",
            {},
            headers={"X-API-Key": "bad"},
        )
        assert code == 401
    finally:
        server.should_exit = True
        thread.join(timeout=5)


def test_unknown_team(tmp_path):
    port = _get_free_port()
    app = api.create_app(SolutionOrchestrator({}))
    api.settings.API_AUTH_KEY = "secret"
    server, thread = _start_server(app, port)

    try:
        code, _ = _http_post(
            f"http://127.0.0.1:{port}/teams/missing/event",
            {"type": "x"},
            headers={"X-API-Key": "secret"},
        )
        assert code == 404
    finally:
        server.should_exit = True
        thread.join(timeout=5)


def test_goal_dry_run(tmp_path):
    _register_agent()
    team_cfg = _write_team(tmp_path)
    port = _get_free_port()
    plans = {"demo": [{"team": "demo", "event": {"type": "echo_agent"}}]}
    orch = SolutionOrchestrator({"demo": str(team_cfg)}, planner_plans=plans)
    api.settings.API_AUTH_KEY = "secret"
    app = api.create_app(orch)
    server, thread = _start_server(app, port)

    try:
        code, body = _http_post(
            f"http://127.0.0.1:{port}/goals/demo?dry_run=true",
            {},
            headers={"X-API-Key": "secret"},
        )
        assert code == 200
        data = json.loads(body)
        assert data["status"] == "planned"
        assert data["sequence"] == [{"team": "demo", "event": "echo_agent"}]
    finally:
        server.should_exit = True
        thread.join(timeout=5)
