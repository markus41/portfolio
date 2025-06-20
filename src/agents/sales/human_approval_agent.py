# src/agents/human_approval_agent.py

from __future__ import annotations

from typing import Dict, Any

from ..base_agent import BaseAgent
from ...tools.notification_tools.teams_notifier import TeamsNotifier
from ...events import HumanApprovalRequest
import logging
import time

logger = logging.getLogger(__name__)


class HumanApprovalAgent(BaseAgent):
    """Agent that sends approval requests via Teams."""

    def __init__(self) -> None:
        self.teams = TeamsNotifier()

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Request human approval and return the result."""

        req = HumanApprovalRequest(**payload)
        msg = req.approval_request
        for approver in req.approvers:
            self.teams.send(title="⚠️ Approval Needed", text=msg)

        logger.info("HumanApprovalAgent → waiting for manual approval (stub)")
        time.sleep(1)  # simulate wait; replace with real callback/polling
        return {
            "status": "approved",
            "approved_by": req.approvers[0] if req.approvers else None,
        }
