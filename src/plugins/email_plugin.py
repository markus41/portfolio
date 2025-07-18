"""Email plugin using SendGrid for delivery.

The plugin expects ``SENDGRID_API_KEY`` and ``DEFAULT_FROM_EMAIL`` in
``Settings``.  The payload should contain ``to``, ``subject`` and ``html``
keys.  ``execute`` returns ``True`` if the API call succeeds (2xx status
code) otherwise ``False``.  Any exception raised by the SendGrid client is
caught and logged so the orchestrator can continue running.
"""

from typing import Any, Dict

import types
import sys

try:  # pragma: no cover - optional dependency
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
except Exception:  # pragma: no cover - optional dependency
    SendGridAPIClient = None
    Mail = None

from ..config import settings

from .base_plugin import BaseToolPlugin
import logging

logger = logging.getLogger(__name__)


class EmailPlugin(BaseToolPlugin):
    """Send an email using the provided payload."""

    name = "email"

    def execute(self, payload: Dict[str, Any]) -> bool:
        """Send an HTML email using SendGrid."""

        if not (SendGridAPIClient and Mail):  # pragma: no cover - optional dep
            logger.warning("sendgrid package not available; email not sent")
            return False

        to_email = payload.get("to")
        subject = payload.get("subject", "")
        html = payload.get("html", "")
        from_email = payload.get("from_email", settings.DEFAULT_FROM_EMAIL)

        client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            html_content=html,
        )

        logger.info("EmailPlugin sending to %s", to_email)
        try:
            resp = client.send(message)
            return 200 <= resp.status_code < 300
        except Exception as exc:  # pragma: no cover - network call
            logger.error("Email send failed: %s", exc)
            return False
