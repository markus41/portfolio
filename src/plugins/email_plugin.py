"""Example email tool plugin."""

from typing import Any, Dict

from .base_plugin import BaseToolPlugin
import logging

logger = logging.getLogger(__name__)


class EmailPlugin(BaseToolPlugin):
    """Send an email using the provided payload."""

    name = "email"

    def execute(self, payload: Dict[str, Any]) -> bool:
        logger.info("Stub email send: %s", payload)
        return True
