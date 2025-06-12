# Tools/notification_tools/teams_notifier.py

import requests
from ...utils.logger import get_logger
from ...constants import TEAMS_WEBHOOK_URL

logger = get_logger(__name__)

class TeamsNotifier:
    def __init__(self):
        self.webhook = TEAMS_WEBHOOK_URL

    def send(self, title: str, text: str):
        card = {
            "@type": "MessageCard",
            "summary": title,
            "sections": [{"activityTitle": title, "text": text}]
        }
        logger.info(f"Posting to Microsoft Teams: {title}")
        resp = requests.post(self.webhook, json=card)
        resp.raise_for_status()
        return resp.ok
