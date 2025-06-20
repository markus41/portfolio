# Tools/notification_tools/slack_notifier.py

from __future__ import annotations

import logging
from typing import Any

import requests  # type: ignore[import-untyped]
from ...config import settings

logger = logging.getLogger(__name__)


class SlackNotifier:
    def __init__(self) -> None:
        self.webhook = settings.SLACK_WEBHOOK_URL

    def send(self, channel: str, text: str) -> bool:
        """Post ``text`` to ``channel`` via the configured webhook."""
        payload = {"channel": channel, "text": text}
        logger.info("Posting to Slack channel %s", channel)
        resp = requests.post(self.webhook, json=payload)
        resp.raise_for_status()
        return resp.ok
