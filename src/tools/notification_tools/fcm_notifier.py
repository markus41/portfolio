# Tools/notification_tools/fcm_notifier.py

import requests
from ...config import settings
import logging

logger = logging.getLogger(__name__)


class FCMNotifier:
    """
    Send mobile push via Firebase Cloud Messaging.
    """

    FCM_URL = "https://fcm.googleapis.com/fcm/send"

    def __init__(self):
        self.server_key = settings.FCM_SERVER_KEY

    def send(self, token: str, title: str, body: str, data: dict = None) -> bool:
        headers = {
            "Authorization": f"key={self.server_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "to": token,
            "notification": {"title": title, "body": body},
            "data": data or {},
        }
        logger.info(f"Sending FCM notification to {token}")
        resp = requests.post(self.FCM_URL, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json().get("success", 0) == 1
