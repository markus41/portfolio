# Tools/notification_tools/teams_notifier.py

import requests
import logging
from ...config import settings

logger = logging.getLogger(__name__)


class TeamsNotifier:
    def __init__(self):
        self.webhook = settings.TEAMS_WEBHOOK_URL

    def send(self, title: str, text: str):
        card = {
            "@type": "MessageCard",
            "summary": title,
            "sections": [{"activityTitle": title, "text": text}],
        }
        logger.info(f"Posting to Microsoft Teams: {title}")
        resp = requests.post(self.webhook, json=card)
        resp.raise_for_status()
        return resp.ok
