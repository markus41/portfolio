import json
import os
import sys
from pathlib import Path
import subprocess

from src import db
from src.config import settings


def test_key_admin_create_and_rotate(tmp_path: Path):
    settings.DB_CONNECTION_STRING = f"sqlite:///{tmp_path}/keys.db"
    db.init_db()

    env = dict(os.environ)
    root = Path(__file__).resolve().parents[1]
    env["PYTHONPATH"] = f"{root}:{env.get('PYTHONPATH', '')}"
    env["DB_CONNECTION_STRING"] = f"sqlite:///{tmp_path}/keys.db"

    create_cmd = [sys.executable, "-m", "src.key_admin", "create", "tenant1", "--scopes", "read,write"]
    res = subprocess.run(create_cmd, capture_output=True, text=True, env=env, timeout=5)
    assert res.returncode == 0
    data = json.loads(res.stdout.strip())
    key = data["key"]
    assert db.validate_api_key(key, "read")

    rotate_cmd = [sys.executable, "-m", "src.key_admin", "rotate", key]
    res_rot = subprocess.run(rotate_cmd, capture_output=True, text=True, env=env, timeout=5)
    assert res_rot.returncode == 0
    new_key = json.loads(res_rot.stdout.strip())["key"]
    assert not db.validate_api_key(key, "read")
    assert db.validate_api_key(new_key, "write")
