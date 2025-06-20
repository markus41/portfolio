"""Example CRM tool plugin."""

from typing import Any, Dict

from .base_plugin import BaseToolPlugin
import logging

logger = logging.getLogger(__name__)


class CRMPlugin(BaseToolPlugin):
    """Perform basic CRM operations."""

    name = "crm"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Stub CRM action: %s", payload)
        return {"ok": True}
