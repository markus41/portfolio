# src/agents/csat_scheduler_agent.py

from ..base_agent import BaseAgent
from ...tools.scheduler_tool import SchedulerTool
from ...utils.logger import get_logger

logger = get_logger(__name__)


class CSATSchedulerAgent(BaseAgent):
    def __init__(self):
        self.scheduler = SchedulerTool()

    def run(self, payload):
        """
        payload: {
          "client_id": str,
          "milestone": int,             # e.g. 25, 50, 100
          "calendar_id": str,
          "survey_link": str,
          "due": {"dateTime": "YYYY-MM-DDTHH:MM:SS", "timeZone": "America/Los_Angeles"}
        }
        """
        summary = f"CSAT {payload['milestone']}% Survey for {payload['client_id']}"
        event = {
            "summary": summary,
            "start": payload["due"],
            "end": payload["due"],
            "attendees": [{"email": payload.get("client_email", "")}],
        }
        ev = self.scheduler.create_event(payload["calendar_id"], event)
        logger.info(
            f"CSATSchedulerAgent → scheduled {ev['id']} for milestone {payload['milestone']}"
        )
        return {"event_id": ev["id"], "status": "scheduled"}
