# Tools/notification_tools/pushover_notifier.py

import requests
from ...config import settings
import logging

logger = logging.getLogger(__name__)


class PushoverNotifier:
    """
    Send push notifications via Pushover.
    """

    API_URL = "https://api.pushover.net/1/messages.json"

    def send(self, message: str, title: str = None, priority: int = 0) -> bool:
        data = {
            "token": settings.PUSHOVER_API_TOKEN,
            "user": settings.PUSHOVER_USER_KEY,
            "message": message,
            "priority": priority,
        }
        if title:
            data["title"] = title
        logger.info("Sending Pushover notification")
        resp = requests.post(self.API_URL, data=data)
        resp.raise_for_status()
        return resp.json().get("status") == 1
