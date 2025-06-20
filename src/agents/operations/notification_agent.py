# src/agents/notification_agent.py

from ..base_agent import BaseAgent
from ...tools.notification_tools.slack_notifier import SlackNotifier
from ...tools.notification_tools.teams_notifier import TeamsNotifier
import logging

logger = logging.getLogger(__name__)


class NotificationAgent(BaseAgent):
    def __init__(self):
        self.slack = SlackNotifier()
        self.teams = TeamsNotifier()

    def run(self, payload):
        """
        payload: {
          "channel": str,
          "message": str,
          "platform": "slack" or "teams"
        }
        """
        platform = payload.get("platform", "slack")
        if platform == "slack":
            ok = self.slack.send(channel=payload["channel"], text=payload["message"])
        else:
            ok = self.teams.send(title="Notification", text=payload["message"])
        status = "notified" if ok else "failed"
        logger.info(f"NotificationAgent → {status}")
        return {"status": status}
