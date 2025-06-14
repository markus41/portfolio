# Tools/notification_tools/pushover_notifier.py

import requests
from ...constants import PUSHOVER_USER_KEY, PUSHOVER_API_TOKEN
from ...utils.logger import get_logger

logger = get_logger(__name__)

class PushoverNotifier:
    """
    Send push notifications via Pushover.
    """

    API_URL = "https://api.pushover.net/1/messages.json"

    def send(self, message: str, title: str = None, priority: int = 0) -> bool:
        data = {
            "token": PUSHOVER_API_TOKEN,
            "user": PUSHOVER_USER_KEY,
            "message": message,
            "priority": priority
        }
        if title: data["title"] = title
        logger.info("Sending Pushover notification")
        resp = requests.post(self.API_URL, data=data)
        resp.raise_for_status()
        return resp.json().get("status") == 1
