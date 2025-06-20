"""Role-based base agents with tool permission sets."""

from __future__ import annotations

from typing import Iterable, List

from ..base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)


class RoleAgent(BaseAgent):
    """Base class enforcing allowed tool permissions."""

    #: Unique role identifier used for logging
    role_name: str = "role"
    #: List of tool names permitted for this role
    allowed_tools: List[str] = []

    def __init__(self, allowed_tools: Iterable[str] | None = None) -> None:
        if allowed_tools is not None:
            self.allowed_tools = list(allowed_tools)

    def can_use(self, tool_name: str) -> bool:
        """Return ``True`` if ``tool_name`` is permitted."""
        return tool_name in self.allowed_tools

    def run(self, payload: dict) -> dict:
        """Validate tool usage in ``payload`` and echo status."""
        tool = payload.get("tool")
        if tool and not self.can_use(tool):
            logger.warning("%s attempted disallowed tool %s", self.role_name, tool)
            return {"error": "permission_denied", "tool": tool}
        logger.info("%s processed payload", self.role_name)
        return {"status": "ok"}


class AssistantAgent(RoleAgent):
    """General assistant role with broad permissions."""

    role_name = "assistant"
    allowed_tools = [
        "chat_tool",
        "email_tool",
        "memory_tools",
        "notification_tools",
    ]


class WriterAgent(RoleAgent):
    """Content writer role with document-focused tools."""

    role_name = "writer"
    allowed_tools = [
        "docgen_tool",
        "email_tool",
    ]


class AnalystAgent(RoleAgent):
    """Data analyst role permitted analytical utilities."""

    role_name = "analyst"
    allowed_tools = [
        "metrics_tools",
        "crm_tools",
        "segmentation_tools",
    ]
