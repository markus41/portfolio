import json
import os
import socket
import subprocess
import sys
import threading
import time
import types
from pathlib import Path
from urllib import request as urllib_request

import pytest

from src.solution_orchestrator import SolutionOrchestrator
from src import api
from src.agents.base_agent import BaseAgent


class EchoAgent(BaseAgent):
    def run(self, payload):
        return {"echo": payload}


def _write_team(tmp_path: Path, name: str = "team", agent: str = "echo_agent") -> Path:
    cfg = {
        "responsibilities": [agent],
        "config": {"participants": [{"config": {"name": agent}}]},
    }
    path = tmp_path / f"{name}.json"
    path.write_text(json.dumps(cfg))
    return path


def _register_agent():
    mod = types.ModuleType("src.agents.echo_agent")
    mod.EchoAgent = EchoAgent
    sys.modules["src.agents.echo_agent"] = mod


def _http_post(url: str, data: dict, headers: dict[str, str]) -> tuple[int, str]:
    payload = json.dumps(data).encode()
    req = urllib_request.Request(url, data=payload, headers=headers, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib_request.urlopen(req) as resp:
            return resp.getcode(), resp.read().decode()
    except urllib_request.HTTPError as err:  # type: ignore[attr-defined]
        return err.code, err.read().decode()


def _http_delete(url: str, headers: dict[str, str]) -> tuple[int, str]:
    req = urllib_request.Request(url, headers=headers, method="DELETE")
    try:
        with urllib_request.urlopen(req) as resp:
            return resp.getcode(), resp.read().decode()
    except urllib_request.HTTPError as err:  # type: ignore[attr-defined]
        return err.code, err.read().decode()


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
            urllib_request.urlopen(f"http://127.0.0.1:{port}/docs")
            return server, thread
        except Exception:
            time.sleep(0.1)
    server.should_exit = True
    thread.join(timeout=5)
    raise RuntimeError("server failed to start")


def test_dynamic_team_api(tmp_path):
    _register_agent()
    team_cfg = _write_team(tmp_path)
    port = _get_free_port()
    orch = SolutionOrchestrator({})
    api.settings.API_AUTH_KEY = "secret"
    app = api.create_app(orch)
    server, thread = _start_server(app, port)

    try:
        code, body = _http_post(
            f"http://127.0.0.1:{port}/teams",
            {"name": "demo", "path": str(team_cfg)},
            {"X-API-Key": "secret"},
        )
        assert code == 201

        code, body = _http_post(
            f"http://127.0.0.1:{port}/teams/demo/event",
            {"type": "echo_agent", "payload": {"foo": 1}},
            {"X-API-Key": "secret"},
        )
        assert code == 200
        assert json.loads(body)["result"]["echo"]["foo"] == 1

        code, _ = _http_post(
            f"http://127.0.0.1:{port}/teams/demo/reload",
            {},
            {"X-API-Key": "secret"},
        )
        assert code == 200

        code, _ = _http_delete(
            f"http://127.0.0.1:{port}/teams/demo",
            {"X-API-Key": "secret"},
        )
        assert code == 200

        code, _ = _http_post(
            f"http://127.0.0.1:{port}/teams/demo/event",
            {"type": "echo_agent"},
            {"X-API-Key": "secret"},
        )
        assert code == 404
    finally:
        server.should_exit = True
        thread.join(timeout=5)


def _start_cli_server(team_cfg: Path, port: int) -> tuple[subprocess.Popen, int]:
    env = dict(os.environ)
    root = os.getcwd()
    env["PYTHONPATH"] = f"{root}:{env.get('PYTHONPATH', '')}"
    cmd = [
        sys.executable,
        "-m",
        "src.cli",
        "start",
        f"base={team_cfg}",
        "--port",
        str(port),
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
    line = proc.stderr.readline().strip()
    assert line.startswith("Listening on")
    _, _, addr = line.partition("on ")
    host, p = addr.split(":")
    return proc, int(p)


def test_dynamic_team_cli(tmp_path):
    base_team = _write_team(tmp_path, "base", "operations.dummy_cli_agent")
    extra_team = _write_team(tmp_path, "extra", "operations.dummy_cli_agent")

    server, port = _start_cli_server(base_team, 0)

    try:
        add_cmd = [
            sys.executable,
            "-m",
            "src.cli",
            "add-team",
            f"demo={extra_team}",
            "--port",
            str(port),
        ]
        res = subprocess.run(add_cmd, capture_output=True, text=True, timeout=5)
        assert json.loads(res.stdout)["status"] == "added"

        event = json.dumps({"type": "operations.dummy_cli_agent", "payload": {"x": 1}})
        send_cmd = [
            sys.executable,
            "-m",
            "src.cli",
            "send",
            "--team",
            "demo",
            "--event",
            event,
            "--port",
            str(port),
        ]
        res_send = subprocess.run(send_cmd, capture_output=True, text=True, timeout=5)
        assert json.loads(res_send.stdout)["status"] == "done"

        reload_cmd = [sys.executable, "-m", "src.cli", "reload-team", "demo", "--port", str(port)]
        res_reload = subprocess.run(reload_cmd, capture_output=True, text=True, timeout=5)
        assert json.loads(res_reload.stdout)["status"] == "reloaded"

        remove_cmd = [sys.executable, "-m", "src.cli", "remove-team", "demo", "--port", str(port)]
        res_remove = subprocess.run(remove_cmd, capture_output=True, text=True, timeout=5)
        assert json.loads(res_remove.stdout)["status"] == "removed"

        res_again = subprocess.run(send_cmd, capture_output=True, text=True, timeout=5)
        assert json.loads(res_again.stdout)["status"] == "unknown_team"
    finally:
        server.terminate()
        server.wait(timeout=5)
