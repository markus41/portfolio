# Tools/notification_tools/ses_notifier.py

import boto3
from botocore.exceptions import ClientError
from ...config import settings
import logging

logger = logging.getLogger(__name__)


class SESNotifier:
    """
    Send emails via AWS SES.
    """

    def __init__(self):
        self.client = boto3.client("ses", region_name=settings.AWS_SES_REGION)

    def send_email(
        self,
        from_addr: str,
        to_addrs: list,
        subject: str,
        html_body: str,
        text_body: str = None,
    ) -> dict:
        logger.info(f"Sending SES email to {to_addrs}")
        try:
            resp = self.client.send_email(
                Source=from_addr,
                Destination={"ToAddresses": to_addrs},
                Message={
                    "Subject": {"Data": subject},
                    "Body": {
                        "Html": {"Data": html_body},
                        **({"Text": {"Data": text_body}} if text_body else {}),
                    },
                },
            )
            return {"MessageId": resp.get("MessageId")}
        except ClientError as e:
            logger.error(f"AWS SES error: {e}")
            raise
