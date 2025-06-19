import json
import socket
import threading
import time
import types
import sys
from pathlib import Path
from urllib import request as urllib_request

from src.solution_orchestrator import SolutionOrchestrator
from src import api
from src.agents.base_agent import BaseAgent


def _http_request(
    url: str, data: dict | None, method: str, headers: dict[str, str] | None = None
) -> tuple[int, str]:
    payload = None if data is None else json.dumps(data).encode()
    req = urllib_request.Request(
        url, data=payload, headers=headers or {}, method=method
    )
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib_request.urlopen(req) as resp:  # noqa: S310 -- in tests
            return resp.getcode(), resp.read().decode()
    except urllib_request.HTTPError as err:  # type: ignore[attr-defined]
        return err.code, err.read().decode()


def _http_get(url: str, headers: dict[str, str] | None = None) -> tuple[int, str]:
    return _http_request(url, None, "GET", headers)


def _http_put(
    url: str, data: dict, headers: dict[str, str] | None = None
) -> tuple[int, str]:
    return _http_request(url, data, "PUT", headers)


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


class EchoAgent(BaseAgent):
    def run(self, payload):
        return payload


def test_config_endpoints(tmp_path):
    teams_dir = tmp_path / "teams"
    teams_dir.mkdir()
    cfg = {
        "responsibilities": ["echo_agent"],
        "config": {"participants": [{"config": {"name": "echo_agent"}}]},
    }
    team_file = teams_dir / "demo.json"
    team_file.write_text(json.dumps(cfg))
    env_file = tmp_path / ".env"
    env_file.write_text("MONDAY_API_URL=https://old\nOTHER=1\n")

    mod = types.ModuleType("src.agents.echo_agent")
    mod.EchoAgent = EchoAgent
    sys.modules["src.agents.echo_agent"] = mod

    port = _get_free_port()
    orch = SolutionOrchestrator({"demo": str(team_file)})
    api.settings.API_AUTH_KEY = "secret"
    app = api.create_app(orch, teams_dir=teams_dir, env_file=env_file)
    server, thread = _start_server(app, port)

    try:
        # CORS headers should allow requests from any origin
        code, _ = _http_request(
            f"http://127.0.0.1:{port}/config/teams",
            None,
            "OPTIONS",
            {"Origin": "http://example.com", "Access-Control-Request-Method": "GET"},
        )
        assert code == 200

        code, body = _http_get(
            f"http://127.0.0.1:{port}/config/teams",
            headers={"X-API-Key": "secret"},
        )
        assert code == 200
        assert json.loads(body) == ["demo"]

        code, body = _http_get(
            f"http://127.0.0.1:{port}/config/teams/demo",
            headers={"X-API-Key": "secret"},
        )
        assert code == 200
        assert json.loads(body)["responsibilities"] == ["echo_agent"]

        cfg["config"]["tools"] = []
        code, _ = _http_put(
            f"http://127.0.0.1:{port}/config/teams/demo",
            cfg,
            headers={"X-API-Key": "secret"},
        )
        assert code == 200
        saved = json.loads(team_file.read_text())
        assert saved["config"]["tools"] == []

        code, _ = _http_put(
            f"http://127.0.0.1:{port}/config/settings",
            {"MONDAY_API_URL": "https://new"},
            headers={"X-API-Key": "secret"},
        )
        assert code == 200
        content = env_file.read_text().strip().splitlines()
        assert "MONDAY_API_URL=https://new" in content
        assert "OTHER=1" in content
    finally:
        server.should_exit = True
        thread.join(timeout=5)
