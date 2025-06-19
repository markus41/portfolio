"""Example cloud document tool plugin."""

from typing import Any, Dict

from .base_plugin import BaseToolPlugin
from ..utils.logger import get_logger

logger = get_logger(__name__)


class CloudDocsPlugin(BaseToolPlugin):
    """Store or fetch documents from a cloud provider."""

    name = "cloud_docs"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, str]:
        logger.info("Stub cloud docs action: %s", payload)
        return {"doc_id": "example"}
