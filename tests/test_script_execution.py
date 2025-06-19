import json
import subprocess
import sys


def test_cli_assistant_direct_execution():
    cmd = [sys.executable, "src/cli_assistant.py", "Budget $50 targeting parents"]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
    assert res.returncode == 0
    data = json.loads(res.stdout.strip())
    assert data["budget"] == 50


def test_cli_direct_execution():
    cmd = [sys.executable, "src/cli.py", "assist", "handle new inventory"]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
    assert res.returncode == 0
    data = json.loads(res.stdout.strip())
    assert data["template"].endswith("inventory_management_team.json")
