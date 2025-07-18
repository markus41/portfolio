"""Shared notification helper for escalating events to human operators.

This module exposes :func:`notify_human` which sends a message through
Slack, Microsoft Teams and email. It relies on existing notifier classes
and the SendGrid API key configured in :mod:`src.config`.
"""

from __future__ import annotations

import logging
from typing import Dict

from ...config import settings
from .slack_notifier import SlackNotifier
from .teams_notifier import TeamsNotifier
from ..email_tool import EmailTool

logger = logging.getLogger(__name__)

_slack = SlackNotifier()
_teams = TeamsNotifier()
_email = EmailTool()


def notify_human(severity: str, message: str) -> Dict[str, str]:
    """Send ``message`` with ``severity`` to all configured channels."""

    subject = f"{severity.title()} alert"
    body = f"[{severity.upper()}] {message}"

    success = False

    try:
        if settings.SLACK_WEBHOOK_URL:
            _slack.send(channel="#general", text=body)
            success = True
    except Exception as exc:  # pragma: no cover - network issues
        logger.error("Slack notification failed: %s", exc)

    try:
        if settings.TEAMS_WEBHOOK_URL:
            _teams.send(title=subject, text=body)
            success = True
    except Exception as exc:  # pragma: no cover - network issues
        logger.error("Teams notification failed: %s", exc)

    try:
        if settings.SENDGRID_API_KEY:
            _email.send_email(
                to_email=settings.DEFAULT_FROM_EMAIL,
                subject=subject,
                html_content=f"<p>{body}</p>",
            )
            success = True
    except Exception as exc:  # pragma: no cover - network issues
        logger.error("Email notification failed: %s", exc)

    return {"status": "sent" if success else "failed", "severity": severity}
