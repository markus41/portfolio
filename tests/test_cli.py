import json
import os
import sys
import types
import time
from pathlib import Path
import subprocess

import pytest



def _write_team(tmp_path: Path) -> Path:
    cfg = {
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
