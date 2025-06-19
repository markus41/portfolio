from __future__ import annotations

import json
import os
import socket
import threading
from pathlib import Path
from types import ModuleType

import pytest

import src.api as api
from src.solution_orchestrator import SolutionOrchestrator
from src.agents.base_agent import BaseAgent

# Provide minimal stubs for optional dependencies so the module can be imported
import types
import sys

sys.modules.setdefault(
    "streamlit",
    types.SimpleNamespace(
        title=lambda *a, **k: None,
        selectbox=lambda *a, **k: None,
        text_input=lambda *a, **k: None,
        text_area=lambda *a, **k: None,
        button=lambda *a, **k: False,
        success=lambda *a, **k: None,
        error=lambda *a, **k: None,
        info=lambda *a, **k: None,
        warning=lambda *a, **k: None,
    ),
)

import json as _json
from urllib import request as _urllib_request


class _Resp:
    def __init__(self, status_code: int, text: str) -> None:
        self.status_code = status_code
        self.text = text
        self.ok = 200 <= status_code < 300

    def json(self):
        return _json.loads(self.text)


def _post(url: str, json=None, headers=None):
    data = _json.dumps(json or {}).encode()
    req = _urllib_request.Request(url, data=data, method="POST", headers=headers or {})
    req.add_header("Content-Type", "application/json")
    try:
        with _urllib_request.urlopen(req) as resp:
            body = resp.read().decode()
            return _Resp(resp.getcode(), body)
    except _urllib_request.HTTPError as err:
        return _Resp(err.code, err.read().decode())


def _get(url: str, headers=None):
    req = _urllib_request.Request(url, headers=headers or {})
    try:
        with _urllib_request.urlopen(req) as resp:
            body = resp.read().decode()
            return _Resp(resp.getcode(), body)
    except _urllib_request.HTTPError as err:
        return _Resp(err.code, err.read().decode())


sys.modules["requests"] = types.SimpleNamespace(Response=_Resp, post=_post, get=_get)

from web import streamlit_app


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


def _register_agent() -> None:
    mod = ModuleType("src.agents.echo_agent")
    mod.EchoAgent = EchoAgent
    import sys

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
            streamlit_app.requests.get(f"http://127.0.0.1:{port}/docs")
            return server, thread
        except Exception:
            import time

            time.sleep(0.1)
    server.should_exit = True
    thread.join(timeout=5)
    raise RuntimeError("server failed to start")


def test_load_team_configs(tmp_path: Path):
    team_dir = tmp_path / "teams"
    team_dir.mkdir()
    cfg = {"responsibilities": ["a", "b"]}
    (team_dir / "demo.json").write_text(json.dumps(cfg))

    teams = streamlit_app.load_team_configs(team_dir)
    assert teams == {"demo": ["a", "b"]}


def test_send_event_and_status(tmp_path: Path, monkeypatch):
    _register_agent()
    team_cfg = _write_team(tmp_path)
    port = _get_free_port()
    orch = SolutionOrchestrator({"demo": str(team_cfg)})
    api.settings.API_AUTH_KEY = "secret"
    app = api.create_app(orch)
    server, thread = _start_server(app, port)

    try:
        monkeypatch.setitem(
            streamlit_app.os.environ, "BACKEND_URL", f"http://127.0.0.1:{port}"
        )
        monkeypatch.setitem(streamlit_app.os.environ, "API_KEY", "secret")
        streamlit_app.API_URL = os.environ["BACKEND_URL"]
        streamlit_app.API_KEY = os.environ["API_KEY"]

        resp = streamlit_app.send_event("demo", "echo_agent", {"foo": 1})
        assert resp.status_code == 200
        assert resp.json()["result"]["echo"]["foo"] == 1

        status_resp = streamlit_app.get_status("demo")
        assert status_resp.status_code == 200
        assert status_resp.json()["status"] == "handled"
    finally:
        server.should_exit = True
        thread.join(timeout=5)
