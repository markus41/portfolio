# Tools/notification_tools/sns_notifier.py

import boto3
from botocore.exceptions import ClientError
from ...config import settings
from ...utils.logger import get_logger

logger = get_logger(__name__)

class SNSNotifier:
    """
    Publish notifications to AWS SNS topic.
    """

    def __init__(self):
        self.client = boto3.client('sns', region_name=settings.AWS_REGION)
        self.topic_arn = settings.AWS_SNS_TOPIC_ARN

    def publish(self, subject: str, message: str) -> dict:
        logger.info(f"Publishing to SNS topic {self.topic_arn}")
        try:
            resp = self.client.publish(
                TopicArn=self.topic_arn,
                Subject=subject,
                Message=message
            )
            return {"MessageId": resp.get("MessageId")}
        except ClientError as e:
            logger.error(f"SNS publish error: {e}")
            raise
