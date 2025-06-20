import json
import subprocess
import sys


def test_cli_list_plugins():
    cmd = [sys.executable, "-m", "src.cli", "list-plugins"]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
    assert res.returncode == 0
    data = json.loads(res.stdout.strip())
    assert "email_plugin" in data["plugins"]


def test_cli_show_plugin():
    cmd = [sys.executable, "-m", "src.cli", "show-plugin", "email_plugin"]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
    assert res.returncode == 0
    data = json.loads(res.stdout.strip())
    assert data["class"].endswith("EmailPlugin")
