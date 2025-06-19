# Tools/notification_tools/slack_notifier.py

import requests
from ...utils.logger import get_logger
from ...config import settings

logger = get_logger(__name__)

class SlackNotifier:
    def __init__(self):
        self.webhook = settings.SLACK_WEBHOOK_URL

    def send(self, channel: str, text: str):
        payload = {"channel": channel, "text": text}
        logger.info(f"Posting to Slack channel {channel}")
        resp = requests.post(self.webhook, json=payload)
        resp.raise_for_status()
        return resp.ok
