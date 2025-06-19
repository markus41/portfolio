"""Simplified CRM API client used across agents."""

try:
    import requests
except ImportError:  # pragma: no cover - optional dependency
    requests = None
from ...config import settings
from ...utils.logger import get_logger

logger = get_logger(__name__)


class CRMTool:
    headers = {
        "Authorization": f"Bearer {settings.CRM_API_KEY}",
        "Content-Type": "application/json",
    }

    @staticmethod
    def create_contact(data: dict) -> dict:
        logger.info("Creating CRM contact")
        if not requests:
            raise RuntimeError("requests package is not installed")
        resp = requests.post(
            f"{settings.CRM_API_URL}/contacts", json=data, headers=CRMTool.headers
        )
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def find_duplicate(email: str) -> bool:
        logger.info(f"Checking duplicates for {email}")
        if not requests:
            raise RuntimeError("requests package is not installed")
        resp = requests.get(
            f"{settings.CRM_API_URL}/contacts",
            params={"email": email},
            headers=CRMTool.headers,
        )
        resp.raise_for_status()
        return bool(resp.json().get("results"))

    # src/tools/crm_tool.py

    @staticmethod
    def get_deal(deal_id: str) -> dict:
        logger.info(f"Fetching deal {deal_id}")
        if not requests:
            raise RuntimeError("requests package is not installed")
        resp = requests.get(
            f"{settings.CRM_API_URL}/deals/{deal_id}", headers=CRMTool.headers
        )
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def update_deal(deal_id: str, data: dict) -> dict:
        logger.info(f"Updating deal {deal_id}")
        if not requests:
            raise RuntimeError("requests package is not installed")
        resp = requests.put(
            f"{settings.CRM_API_URL}/deals/{deal_id}",
            json=data,
            headers=CRMTool.headers,
        )
        resp.raise_for_status()
        return resp.json()
