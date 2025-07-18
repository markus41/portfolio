"""Brookside BI core package.

This module exposes the package version for external callers.  The
version is read from ``setup.cfg`` so that both the codebase and the
packaging metadata stay in sync.
"""

from __future__ import annotations

import configparser
from pathlib import Path


def _load_version() -> str:
    """Return the version defined in ``setup.cfg``.

    The configuration file lives one directory above ``src``.  Using a
    lightweight ``configparser`` reader avoids importing
    ``pkg_resources`` or ``importlib.metadata`` at runtime which keeps
    the dependency surface minimal while ensuring the value always
    matches the packaging metadata.
    """

    cfg_path = Path(__file__).resolve().parents[1] / "setup.cfg"
    parser = configparser.ConfigParser()
    parser.read(cfg_path)
    try:
        return parser["metadata"]["version"]
    except KeyError as exc:  # pragma: no cover - defensive programming
        raise RuntimeError("Malformed setup.cfg, missing [metadata] version") from exc


#: Current package version as defined in ``setup.cfg``.
__version__: str = _load_version()


def get_version() -> str:
    """Return the current package version.

    This helper simply exposes :data:`__version__` for callers that want
    a function-based API.  It is primarily useful when mocking during
    tests or when accessed from dynamic import contexts.
    """

    return __version__


__all__ = ["__version__", "get_version"]
