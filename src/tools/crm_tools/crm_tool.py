"""Simplified CRM API client used across agents."""

try:
    import requests
except ImportError:  # pragma: no cover - optional dependency
    requests = None
from ...config import settings
from ...utils.logger import get_logger
from ...user_context import get_current

logger = get_logger(__name__)


class CRMTool:
    """Simplified CRM API client used across agents.

    The tool reads the CRM credentials from :mod:`src.config` but will override
    them with the values stored in :class:`~src.user_settings.UserSettingsData`
    when the current request provides such configuration.  This allows each user
    to target their own CRM instance without restarting the backend.
    """

    def _headers(self) -> dict:
        current = get_current()
        key = current.crm_api_key if current else settings.CRM_API_KEY
        return {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        }

    def _url(self) -> str:
        current = get_current()
        return current.crm_api_url if current and current.crm_api_url else settings.CRM_API_URL

    def create_contact(self, data: dict) -> dict:
        logger.info("Creating CRM contact")
        if not requests:
            raise RuntimeError("requests package is not installed")
        resp = requests.post(
            f"{self._url()}/contacts", json=data, headers=self._headers()
        )
        resp.raise_for_status()
        return resp.json()

    def find_duplicate(self, email: str) -> bool:
        logger.info(f"Checking duplicates for {email}")
        if not requests:
            raise RuntimeError("requests package is not installed")
        resp = requests.get(
            f"{self._url()}/contacts",
            params={"email": email},
            headers=self._headers(),
        )
        resp.raise_for_status()
        return bool(resp.json().get("results"))

    # src/tools/crm_tool.py

    def get_deal(self, deal_id: str) -> dict:
        logger.info(f"Fetching deal {deal_id}")
        if not requests:
            raise RuntimeError("requests package is not installed")
        resp = requests.get(
            f"{self._url()}/deals/{deal_id}", headers=self._headers()
        )
        resp.raise_for_status()
        return resp.json()

    def update_deal(self, deal_id: str, data: dict) -> dict:
        logger.info(f"Updating deal {deal_id}")
        if not requests:
            raise RuntimeError("requests package is not installed")
        resp = requests.put(
            f"{self._url()}/deals/{deal_id}",
            json=data,
            headers=self._headers(),
        )
        resp.raise_for_status()
        return resp.json()
