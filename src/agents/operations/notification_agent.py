# src/agents/notification_agent.py

from __future__ import annotations

from typing import Dict, Any

from ..base_agent import BaseAgent
from ...tools.notification_tools.slack_notifier import SlackNotifier
from ...tools.notification_tools.teams_notifier import TeamsNotifier
from ...events import NotificationPayload
import logging

logger = logging.getLogger(__name__)


class NotificationAgent(BaseAgent):
    """Send notifications to Slack or Teams."""

    def __init__(self) -> None:
        self.slack = SlackNotifier()
        self.teams = TeamsNotifier()

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send ``payload.message`` to the configured channel."""

        data = NotificationPayload(**payload)
        platform = data.platform
        if platform == "slack":
            ok = self.slack.send(channel=data.channel, text=data.message)
        else:
            ok = self.teams.send(title="Notification", text=data.message)

        status = "notified" if ok else "failed"
        logger.info("NotificationAgent → %s", status)
        return {"status": status}
