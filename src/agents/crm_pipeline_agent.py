"""Advance deals through a CRM pipeline and schedule follow-ups."""

from .base_agent import BaseAgent
import importlib
from ..utils.logger import get_logger

logger = get_logger(__name__)

class CRMPipelineAgent(BaseAgent):
    def __init__(self):
        CRMTool = importlib.import_module("src.tools.crm_tools.crm_tool").CRMTool
        SchedulerTool = importlib.import_module("src.tools.scheduler_tool").SchedulerTool
        self.crm = CRMTool()
        self.scheduler = SchedulerTool()

    def run(self, payload: dict) -> dict:
        """
        payload: {
          "deal_id": str,
          "calendar_id": str,
          "followup_template": {
            "summary": str,
            "attendees": [ {"email": str} ]
          }
        }
        """
        # pull deal details from the CRM
        deal = self.crm.get_deal(payload["deal_id"])
        stage = deal.get("stage")
        action = "none"
        event_id = None

        if stage == "Proposal Sent":
            ev = {
                "summary": payload["followup_template"]["summary"],
                "start": deal["next_action_date"],      # assume ISO datetime
                "end":   deal["next_action_date"],
                "attendees": payload["followup_template"].get("attendees", [])
            }
            # schedule a follow-up meeting in the prospect's calendar
            res = self.scheduler.create_event(payload["calendar_id"], ev)
            event_id = res["id"]
            action = "followup_scheduled"
            logger.info(f"Scheduled follow-up for deal {payload['deal_id']} as event {event_id}")

        return {"deal_id": payload["deal_id"], "action": action, "event_id": event_id}
