import requests
from ..constants import (
    DOCUSIGN_ACCOUNT_ID,
    DOCUSIGN_BASE_URL,
)
from ..utils.logger import get_logger

logger = get_logger(__name__)

class DocuSignTool:
    """Minimal DocuSign API wrapper."""

    def __init__(self, token: str):
        self.token = token
        self.base_url = DOCUSIGN_BASE_URL

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def send_envelope(self, envelope_definition: dict) -> dict:
        url = f"{self.base_url}/v2.1/accounts/{DOCUSIGN_ACCOUNT_ID}/envelopes"
        logger.info("Creating DocuSign envelope")
        resp = requests.post(url, json=envelope_definition, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def get_envelope_status(self, envelope_id: str) -> dict:
        url = f"{self.base_url}/v2.1/accounts/{DOCUSIGN_ACCOUNT_ID}/envelopes/{envelope_id}"
        logger.info(f"Fetching DocuSign envelope status for {envelope_id}")
        resp = requests.get(url, headers=self._headers())
        resp.raise_for_status()
        return resp.json()
