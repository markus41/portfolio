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
