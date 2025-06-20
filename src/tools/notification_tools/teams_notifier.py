# Tools/notification_tools/teams_notifier.py

from __future__ import annotations

import logging
from typing import Any

import requests  # type: ignore[import-untyped]
from ...config import settings

logger = logging.getLogger(__name__)


class TeamsNotifier:
    def __init__(self) -> None:
        self.webhook = settings.TEAMS_WEBHOOK_URL

    def send(self, title: str, text: str) -> bool:
        """Send a Teams card with ``title`` and ``text``."""
        card = {
            "@type": "MessageCard",
            "summary": title,
            "sections": [{"activityTitle": title, "text": text}],
        }
        logger.info("Posting to Microsoft Teams: %s", title)
        resp = requests.post(self.webhook, json=card)
        resp.raise_for_status()
        return resp.ok
