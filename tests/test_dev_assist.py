import os
import sys
import subprocess
from pathlib import Path


def test_dev_assist_creates_files(tmp_path: Path) -> None:
    """`dev_assist` should scaffold module and test placeholders."""
    # Arrange - working directory with src/ and tests/ folders
    (tmp_path / "src").mkdir()
    (tmp_path / "tests").mkdir()

    env = dict(os.environ)
    root = Path(__file__).resolve().parents[1]
    env["PYTHONPATH"] = f"{root}:{env.get('PYTHONPATH', '')}"
    cmd = [sys.executable, "-m", "src.dev_assist", "Demo Module"]

    # Act
    result = subprocess.run(
        cmd, cwd=tmp_path, capture_output=True, text=True, env=env, timeout=5
    )

    # Assert
    assert result.returncode == 0
    code_file = tmp_path / "src" / "demo_module.py"
    test_file = tmp_path / "tests" / "test_demo_module.py"
    assert code_file.exists(), "Expected module file was not created"
    assert test_file.exists(), "Expected test file was not created"

    assert code_file.read_text() == '"""TODO: Demo Module."""\n'
    expected_test = (
        '"""Tests for {name}"""\n\n\n' "def test_placeholder():\n    assert True\n"
    )
    assert test_file.read_text() == expected_test
