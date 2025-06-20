"""Example web scraping tool plugin."""

from typing import Any, Dict

from .base_plugin import BaseToolPlugin
import logging

logger = logging.getLogger(__name__)


class ScrapingPlugin(BaseToolPlugin):
    """Return dummy HTML for a URL."""

    name = "scraping"

    def execute(self, payload: Dict[str, Any]) -> str:
        logger.info("Stub scrape: %s", payload)
        return "<html></html>"
