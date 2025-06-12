# src/agents/human_approval_agent.py

from .base_agent import BaseAgent
from ..tools.notification_tools.teams_notifier import TeamsNotifier
from ..utils.logger import get_logger
import time

logger = get_logger(__name__)

class HumanApprovalAgent(BaseAgent):
    def __init__(self):
        self.teams = TeamsNotifier()

    def run(self, payload):
        """
        payload: {
          "approval_request": str,
          "approvers": [str],    # channels or user IDs
          "timeout": int         # seconds to wait
        }
        """
        msg = payload["approval_request"]
        for approver in payload.get("approvers", []):
            self.teams.send(title="⚠️ Approval Needed", text=msg)
        logger.info("HumanApprovalAgent → waiting for manual approval (stub)")
        time.sleep(1)  # simulate wait; replace with real callback/polling
        return {"status": "approved", "approved_by": payload.get("approvers", [None])[0]}
