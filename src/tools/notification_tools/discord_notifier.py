# Tools/notification_tools/discord_notifier.py

import requests
from ...constants import DISCORD_WEBHOOK_URL
from ...utils.logger import get_logger

logger = get_logger(__name__)

class DiscordNotifier:
    """
    Post messages to a Discord channel via webhook.
    """

    def __init__(self):
        self.webhook = DISCORD_WEBHOOK_URL

    def send(self, content: str, username: str = None) -> bool:
        payload = {"content": content}
        if username: payload["username"] = username
        logger.info("Posting to Discord via webhook")
        resp = requests.post(self.webhook, json=payload)
        resp.raise_for_status()
        return resp.ok
