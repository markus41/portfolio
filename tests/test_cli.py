import json
import os
import sys
import types
import time
from pathlib import Path
import subprocess
import socket

import pytest


def _write_team(tmp_path: Path) -> Path:
    cfg = {
        "provider": "autogen.agentchat.teams.RoundRobinGroupChat",
        "responsibilities": ["operations.dummy_cli_agent"],
        "config": {
            "participants": [{"config": {"name": "operations.dummy_cli_agent"}}]
        },
    }
    path = tmp_path / "team.json"
    path.write_text(json.dumps(cfg))
    return path


def _start_server(team_cfg: Path, port: int) -> tuple[subprocess.Popen, int]:
    env = dict(os.environ)
    root = os.getcwd()
    env["PYTHONPATH"] = f"{root}:{env.get('PYTHONPATH', '')}"
    cmd = [
        sys.executable,
        "-m",
        "src.cli",
        "start",
        f"demo={team_cfg}",
        "--port",
        str(port),
    ]
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env
    )
    line = proc.stderr.readline().strip()
    assert line.startswith("Listening on")
    _, _, addr = line.partition("on ")
    host, p = addr.split(":")
    return proc, int(p)


def test_cli_start_send_status(tmp_path, monkeypatch):
    team_cfg = _write_team(tmp_path)
    sys.modules.setdefault(
        "requests",
        types.SimpleNamespace(
            post=lambda *a, **k: types.SimpleNamespace(ok=True, json=lambda: {}),
            get=lambda *a, **k: types.SimpleNamespace(ok=True, json=lambda: {}),
        ),
    )

    server, port = _start_server(team_cfg, 0)

    event = {"type": "operations.dummy_cli_agent", "payload": {"foo": 1}}
    send_cmd = [
        sys.executable,
        "-m",
        "src.cli",
        "send",
        "--team",
        "demo",
        "--event",
        json.dumps(event),
        "--port",
        str(port),
    ]
    res = subprocess.run(send_cmd, capture_output=True, text=True, timeout=5)
    assert res.returncode == 0
    data = json.loads(res.stdout.strip())
    assert data["status"] == "done"

    status_cmd = [sys.executable, "-m", "src.cli", "status", "--port", str(port)]
    res_status = subprocess.run(status_cmd, capture_output=True, text=True, timeout=5)
    status_data = json.loads(res_status.stdout.strip())
    assert status_data.get("demo") == "handled"

    server.terminate()
    server.wait(timeout=5)


def test_cli_assist(tmp_path):
    """The assist subcommand should map phrases to workflow templates."""

    cmd = [sys.executable, "-m", "src.cli", "assist", "handle new inventory"]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
    assert res.returncode == 0
    data = json.loads(res.stdout.strip())
    assert data["template"].endswith("inventory_management_team.json")

    cmd_unknown = [sys.executable, "-m", "src.cli", "assist", "unknown gibberish"]
    res_unknown = subprocess.run(cmd_unknown, capture_output=True, text=True, timeout=5)
    assert res_unknown.returncode == 0
    data_unknown = json.loads(res_unknown.stdout.strip())
    assert data_unknown["template"] is None


def test_cli_validate_team(tmp_path):
    path = _write_team(tmp_path)

    cmd = [sys.executable, "-m", "src.cli", "validate-team", str(path)]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
    assert res.returncode == 0
    assert json.loads(res.stdout.strip())["valid"] is True

    bad = tmp_path / "bad.json"
    bad.write_text("{}")
    cmd_bad = [sys.executable, "-m", "src.cli", "validate-team", str(bad)]
    res_bad = subprocess.run(cmd_bad, capture_output=True, text=True, timeout=5)
    assert res_bad.returncode == 0
    out = json.loads(res_bad.stdout.strip())
    assert out["valid"] is False
    # the CLI should include a descriptive error message when validation fails
    assert isinstance(out.get("error"), str) and out["error"]


@pytest.mark.parametrize(
    "task,expected",
    [
        ("close more sales leads", "src/teams/sales_team_full.json"),
        ("ship customer order asap", "src/teams/fulfillment_pipeline_team.json"),
        (
            "update INVENTORY counts",  # check case-insensitive matching
            "src/teams/inventory_management_team.json",
        ),
        ("operations planning", "src/teams/operations_team.json"),
        (
            "driver tracking updates",
            "src/teams/on_the_road_team.json",
        ),
        (
            "new real estate listing published",
            "src/teams/real_estate_team.json",
        ),
        (
            "eCommerce shopping cart improvements",
            "src/teams/ecommerce_team.json",
        ),
    ],
)
def test_match_workflow_known(task, expected):
    """Verify that known keywords map to the correct workflow templates."""
    from src import cli

    assert cli._match_workflow(task) == expected


def test_match_workflow_unknown():
    """Tasks without mapped keywords should return ``None``."""
    from src import cli

    assert cli._match_workflow("unrelated gibberish task") is None


class _FakeSock:
    """Simple socket stand-in used for ``_send_payload`` tests."""

    def __init__(self, resp: bytes | Exception):
        self._resp = resp
        self.sent: bytes = b""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def settimeout(self, _timeout: float) -> None:
        pass

    def sendall(self, data: bytes) -> None:
        self.sent += data

    def recv(self, _size: int) -> bytes:
        if isinstance(self._resp, Exception):
            raise self._resp
        if self._resp is None:
            return b""
        data = self._resp
        self._resp = None
        return data


def test_send_payload_success(monkeypatch):
    from src import cli

    def fake_conn(addr, timeout=None):
        return _FakeSock(b'{"ok": true}\n')

    monkeypatch.setattr(cli.socket, "create_connection", fake_conn)
    out = cli._send_payload("h", 1, {"cmd": "x"}, timeout=1)
    assert out == {"ok": True}


def test_send_payload_connection_refused(monkeypatch):
    from src import cli

    def fake_conn(addr, timeout=None):
        raise ConnectionRefusedError

    monkeypatch.setattr(cli.socket, "create_connection", fake_conn)
    with pytest.raises(SystemExit) as exc:
        cli._send_payload("h", 1, {"cmd": "x"})
    assert "Failed to connect" in str(exc.value)


def test_send_payload_timeout(monkeypatch):
    from src import cli

    def fake_conn(addr, timeout=None):
        return _FakeSock(socket.timeout())

    monkeypatch.setattr(cli.socket, "create_connection", fake_conn)
    with pytest.raises(SystemExit) as exc:
        cli._send_payload("h", 1, {"cmd": "x"}, timeout=0.1)
    assert "Timed out" in str(exc.value)


def test_send_payload_bad_json(monkeypatch):
    from src import cli

    def fake_conn(addr, timeout=None):
        return _FakeSock(b"not-json\n")

    monkeypatch.setattr(cli.socket, "create_connection", fake_conn)
    with pytest.raises(SystemExit) as exc:
        cli._send_payload("h", 1, {"cmd": "x"})
    assert "Invalid JSON response" in str(exc.value)
