# Tools/notification_tools/twilio_notifier.py

from twilio.rest import Client
from ...constants import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_PHONE
from ...utils.logger import get_logger

logger = get_logger(__name__)

class TwilioNotifier:
    """
    Send SMS messages via Twilio.
    """

    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        self.from_phone = TWILIO_FROM_PHONE

    def send_sms(self, to: str, body: str) -> dict:
        logger.info(f"Sending SMS to {to}")
        msg = self.client.messages.create(
            body=body,
            from_=self.from_phone,
            to=to
        )
        return {"sid": msg.sid, "status": msg.status}
