# src/tools/scheduler_tool.py

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
except ImportError:  # pragma: no cover - optional dependency
    service_account = None
    build = None
from ..utils.logger import get_logger

logger = get_logger(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'credentials.json'

class SchedulerTool:
    def __init__(self):
        if service_account is None or build is None:
            raise RuntimeError("google-api-python-client is required for SchedulerTool")
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        self.service = build('calendar', 'v3', credentials=creds)

    def create_event(self, calendar_id: str, event: dict) -> dict:
        if self.service is None:
            raise RuntimeError("google-api-python-client is required for SchedulerTool")
        logger.info("Creating calendar event")
        return (
            self.service.events()
            .insert(calendarId=calendar_id, body=event)
            .execute()
        )
