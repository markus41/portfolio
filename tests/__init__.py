"""Test package setup hooking the local HTTPX stub."""

import sys
from . import httpx_stub as httpx

sys.modules.setdefault("httpx", httpx)
