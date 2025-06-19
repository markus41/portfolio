from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from ..config import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class EmailTool:
    """Simple wrapper around SendGrid for sending HTML emails."""

    def __init__(self):
        self.client = SendGridAPIClient(settings.SENDGRID_API_KEY)

    def send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        logger.info(f"Sending email to {to_email}")
        message = Mail(
            from_email="sales@yourcompany.com",
            to_emails=to_email,
            subject=subject,
            html_content=html_content,
        )
        try:
            response = self.client.send(message)
            return 200 <= response.status_code < 300
        except Exception as exc:  # pragma: no cover - network call
            logger.error(f"Email send failed: {exc}")
            return False
