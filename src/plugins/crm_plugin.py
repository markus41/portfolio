"""CRM tool plugin providing a minimal REST integration.

``CRMPlugin`` posts payload data to the configured CRM API using the
``requests`` library.  It expects ``settings.CRM_API_URL`` and
``settings.CRM_API_KEY`` to be defined.  The payload may specify an
``action`` (path appended to the base URL) and a ``data`` dictionary that
is sent as JSON.  The method returns the decoded JSON response from the
service.  When the optional ``requests`` dependency is missing a warning is
logged and an empty dictionary is returned so tests can run without
network access.
"""

from typing import Any, Dict

try:  # pragma: no cover - optional dependency
    import requests
except Exception:  # pragma: no cover - optional dependency
    requests = None

from ..config import settings

from .base_plugin import BaseToolPlugin
import logging

logger = logging.getLogger(__name__)


class CRMPlugin(BaseToolPlugin):
    """Perform basic CRM operations."""

    name = "crm"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send ``payload`` to the CRM API and return the JSON response."""

        if not getattr(requests, "post", None):  # pragma: no cover - optional dep
            logger.warning("requests package is unavailable; returning empty response")
            return {}

        action = payload.get("action", "record")
        data = payload.get("data", {})

        url = f"{settings.CRM_API_URL}/{action}"
        headers = {"Authorization": f"Bearer {settings.CRM_API_KEY}"}

        logger.info("CRMPlugin posting to %s", url)
        resp = requests.post(url, json=data, headers=headers, timeout=5)
        resp.raise_for_status()
        return resp.json()
