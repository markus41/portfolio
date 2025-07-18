"""Simple web scraping plugin using ``requests``.

The plugin fetches HTML from the ``url`` in ``payload`` with a configurable
``User-Agent`` header (``SCRAPER_USER_AGENT`` in :mod:`src.config`).  If the
``requests`` package is unavailable it logs a warning and returns an empty
string so unit tests can run without the dependency.
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


class ScrapingPlugin(BaseToolPlugin):
    """Fetch HTML content for a URL."""

    name = "scraping"

    def execute(self, payload: Dict[str, Any]) -> str:
        """Return the raw HTML for the requested URL."""

        if not getattr(requests, "get", None):  # pragma: no cover - optional dep
            logger.warning("requests package not available; returning empty page")
            return ""

        url = payload.get("url", "")
        headers = {"User-Agent": settings.SCRAPER_USER_AGENT}

        logger.info("ScrapingPlugin fetching %s", url)
        resp = requests.get(url, headers=headers, timeout=5)
        resp.raise_for_status()
        return resp.text
