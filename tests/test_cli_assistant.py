import json
import subprocess
import sys


def test_cli_assistant_parsing():
    text = "Budget $300 targeting students on 01/02/2025"
    cmd = [sys.executable, "-m", "src.cli_assistant", text]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
    assert res.returncode == 0
    data = json.loads(res.stdout.strip())
    assert data["budget"] == 300
    assert "2025-01-02" in data["dates"]
    assert data["target_audience"] == "students"
