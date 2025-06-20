"""Example cloud document tool plugin."""

from typing import Any, Dict

from .base_plugin import BaseToolPlugin
import logging

logger = logging.getLogger(__name__)


class CloudDocsPlugin(BaseToolPlugin):
    """Store or fetch documents from a cloud provider."""

    name = "cloud_docs"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, str]:
        logger.info("Stub cloud docs action: %s", payload)
        return {"doc_id": "example"}
