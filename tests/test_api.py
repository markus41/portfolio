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


def _http_post(
    url: str, data: dict, headers: dict[str, str] | None = None
) -> tuple[int, str]:
    payload = json.dumps(data).encode()
    req = urllib_request.Request(
        url, data=payload, headers=headers or {}, method="POST"
    )
    req.add_header("Content-Type", "application/json")
    try:
        with urllib_request.urlopen(req) as resp:  # noqa: S310 -- in tests
            return resp.getcode(), resp.read().decode()
    except urllib_request.HTTPError as err:  # type: ignore[attr-defined]
        return err.code, err.read().decode()


def _http_options(
    url: str, headers: dict[str, str] | None = None
) -> tuple[int, str, str]:
    base_headers = {"Access-Control-Request-Method": "POST"}
    if headers:
        base_headers.update(headers)
    req = urllib_request.Request(url, headers=base_headers, method="OPTIONS")
    try:
        with urllib_request.urlopen(req) as resp:
            return (
                resp.getcode(),
                resp.read().decode(),
                resp.headers.get("Access-Control-Allow-Origin", ""),
            )
    except urllib_request.HTTPError as err:  # type: ignore[attr-defined]
        return (
            err.code,
            err.read().decode(),
            err.headers.get("Access-Control-Allow-Origin", ""),
        )


from src.agents.base_agent import BaseAgent


class EchoAgent(BaseAgent):
    def run(self, payload):
        return {"echo": payload}


def _write_team(tmp_path: Path) -> Path:
    cfg = {
        "provider": "autogen.agentchat.teams.RoundRobinGroupChat",
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


def test_activity_endpoint(tmp_path):
    _register_agent()
    team_cfg = _write_team(tmp_path)
    port = _get_free_port()
    log_path = tmp_path / "act.jsonl"
    orch = SolutionOrchestrator({"demo": str(team_cfg)}, log_path=str(log_path))
    api.settings.API_AUTH_KEY = "secret"
    app = api.create_app(orch)
    server, thread = _start_server(app, port)

    try:
        _http_post(
            f"http://127.0.0.1:{port}/teams/demo/event",
            {"type": "echo_agent", "payload": {"foo": 1}},
            headers={"X-API-Key": "secret"},
        )

        code, body = _http_get(
            f"http://127.0.0.1:{port}/activity?limit=1",
            headers={"X-API-Key": "secret"},
        )
        assert code == 200
        data = json.loads(body)
        assert data["activity"][0]["agent_id"] == "echo_agent"
    finally:
        server.should_exit = True
        thread.join(timeout=5)


def test_workflow_endpoints(tmp_path):
    port = _get_free_port()
    api.settings.API_AUTH_KEY = "secret"
    app = api.create_app()
    server, thread = _start_server(app, port)

    try:
        payload = {
            "name": "demo",
            "nodes": [
                {"id": "a", "type": "agent", "label": "A"},
                {"id": "b", "type": "tool", "label": "B"},
            ],
            "edges": [{"source": "a", "target": "b"}],
        }
        code, _ = _http_post(
            f"http://127.0.0.1:{port}/workflows",
            payload,
            headers={"X-API-Key": "secret"},
        )
        assert code == 201

        code, body = _http_get(
            f"http://127.0.0.1:{port}/workflows/demo",
            headers={"X-API-Key": "secret"},
        )
        assert code == 200
        data = json.loads(body)
        assert data["name"] == "demo"
        assert len(data["nodes"]) == 2
    finally:
        server.should_exit = True
        thread.join(timeout=5)


def test_history_and_cors(tmp_path):
    _register_agent()
    team_cfg = _write_team(tmp_path)
    port = _get_free_port()
    api.settings.API_AUTH_KEY = "secret"
    api.settings.DB_CONNECTION_STRING = f"sqlite:///{tmp_path}/test.db"
    app = api.create_app(SolutionOrchestrator({"demo": str(team_cfg)}))
    server, thread = _start_server(app, port)

    try:
        _http_post(
            f"http://127.0.0.1:{port}/teams/demo/event",
            {"type": "echo_agent", "payload": {"x": 1}},
            headers={"X-API-Key": "secret"},
        )

        code, body = _http_get(
            f"http://127.0.0.1:{port}/history?limit=1",
            headers={"X-API-Key": "secret"},
        )
        assert code == 200
        data = json.loads(body)
        assert data["history"][0]["team"] == "demo"

        code, _, allow_origin = _http_options(
            f"http://127.0.0.1:{port}/teams/demo/event",
            headers={"Origin": "http://example.com"},
        )
        assert code == 200
        assert allow_origin == "*"
    finally:
        server.should_exit = True
        thread.join(timeout=5)
