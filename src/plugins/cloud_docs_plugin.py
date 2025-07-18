"""Cloud document management plugin backed by a REST API.

The plugin communicates with a cloud document service specified by
``CLOUD_DOCS_API_URL`` and authenticated via ``CLOUD_DOCS_API_KEY``.  The
``payload`` may contain an ``action`` path and a ``data`` dictionary.  The
JSON response from the service is returned.  When ``requests`` is missing
an empty result is produced so the rest of the application can still run
in limited environments.
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


class CloudDocsPlugin(BaseToolPlugin):
    """Store or fetch documents from a cloud provider."""

    name = "cloud_docs"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Perform an action against the cloud document service."""

        if not getattr(requests, "post", None):  # pragma: no cover - optional dep
            logger.warning("requests package unavailable; returning empty result")
            return {}

        action = payload.get("action", "upload")
        data = payload.get("data")

        url = f"{settings.CLOUD_DOCS_API_URL}/{action}"
        headers = {"Authorization": f"Bearer {settings.CLOUD_DOCS_API_KEY}"}

        logger.info("CloudDocsPlugin calling %s", url)
        resp = requests.post(url, json=data, headers=headers, timeout=5)
        resp.raise_for_status()
        return resp.json()
