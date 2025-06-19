# src/agents/scheduling_agent.py

from ..base_agent import BaseAgent
from ...tools.scheduler_tool import SchedulerTool
from ...utils.logger import get_logger

logger = get_logger(__name__)

class SchedulingAgent(BaseAgent):
    def __init__(self):
        self.scheduler = SchedulerTool()

    def run(self, payload):
        """
        payload: {
          "calendar_id": str,
          "summary": str,
          "start": {"dateTime": "2025-07-01T10:00:00", "timeZone": "America/Los_Angeles"},
          "end":   {"dateTime": "2025-07-01T10:30:00", "timeZone": "America/Los_Angeles"},
          "attendees": [{"email": "foo@bar.com"}]
        }
        """
        event = {
            "summary": payload["summary"],
            "start": payload["start"],
            "end": payload["end"],
            "attendees": payload.get("attendees", []),
        }
        ev = self.scheduler.create_event(payload["calendar_id"], event)
        logger.info(f"Created event {ev['id']}")
        return {"event_id": ev["id"], "status": "scheduled"}
