import importlib

import pytest
from pydantic import ValidationError

import src.config as config


def _reload_settings(monkeypatch, **env):
    """Reload ``src.config`` with provided environment variables."""
    for key, value in env.items():
        if value is None:
            monkeypatch.delenv(key, raising=False)
        else:
            monkeypatch.setenv(key, value)
    return importlib.reload(config)


def test_invalid_aws_region(monkeypatch):
    with pytest.raises(ValidationError):
        _reload_settings(monkeypatch, AWS_REGION="mars-east-1")
    # restore
    _reload_settings(monkeypatch, AWS_REGION=None)


def test_invalid_adyen_environment(monkeypatch):
    with pytest.raises(ValidationError):
        _reload_settings(monkeypatch, ADYEN_ENVIRONMENT="LOCAL")
    _reload_settings(monkeypatch, ADYEN_ENVIRONMENT=None)


def test_env_file_selection(monkeypatch, tmp_path):
    """Settings should load variables from the file chosen via ENV."""
    from pathlib import Path

    cwd = Path.cwd()
    try:
        # create environment-specific file
        env_file = tmp_path / ".env.dev"
        env_file.write_text("OPENAI_API_KEY=from_dev_file\n")
        monkeypatch.chdir(tmp_path)
        mod = _reload_settings(monkeypatch, ENV="dev", ENV_FILE=None)
        assert mod.settings.OPENAI_API_KEY == "from_dev_file"
    finally:
        monkeypatch.chdir(cwd)


def test_env_file_override(monkeypatch, tmp_path):
    """ENV_FILE should override default selection logic."""
    env_file = tmp_path / "custom.env"
    env_file.write_text("OPENAI_API_KEY=from_override\n")
    mod = _reload_settings(monkeypatch, ENV_FILE=str(env_file))
    assert mod.settings.OPENAI_API_KEY == "from_override"
    _reload_settings(monkeypatch, ENV_FILE=None, OPENAI_API_KEY=None)
