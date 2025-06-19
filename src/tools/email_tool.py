from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from ..config import settings
from ..utils.logger import get_logger
from ..utils import retry_tool

logger = get_logger(__name__)

class EmailTool:
    """Simple wrapper around SendGrid for sending HTML emails."""

    def __init__(self):
        self.client = SendGridAPIClient(settings.SENDGRID_API_KEY)

    @retry_tool(fallback=lambda exc, _a, _kw: False)
    def send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        """Send a single HTML email via SendGrid.

        Parameters
        ----------
        to_email:
            Recipient address.
        subject:
            Email subject line.
        html_content:
            Body of the message in HTML format.
        """

        logger.info(f"Sending email to {to_email}")
        message = Mail(
            from_email="sales@yourcompany.com",
            to_emails=to_email,
            subject=subject,
            html_content=html_content,
        )
        response = self.client.send(message)
        return 200 <= response.status_code < 300
