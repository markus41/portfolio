# Tools/notification_tools/discord_notifier.py

import requests
from ...config import settings
import logging

logger = logging.getLogger(__name__)


class DiscordNotifier:
    """
    Post messages to a Discord channel via webhook.
    """

    def __init__(self):
        self.webhook = settings.DISCORD_WEBHOOK_URL

    def send(self, content: str, username: str = None) -> bool:
        payload = {"content": content}
        if username:
            payload["username"] = username
        logger.info("Posting to Discord via webhook")
        resp = requests.post(self.webhook, json=payload)
        resp.raise_for_status()
        return resp.ok
