# src/tools/crm_tool.py

try:
    import requests
except ImportError:  # pragma: no cover - optional dependency
    requests = None
from src.constants import CRM_API_URL, CRM_API_KEY
from src.utils.logger import get_logger

logger = get_logger(__name__)

class CRMTool:
    headers = {"Authorization": f"Bearer {CRM_API_KEY}", "Content-Type": "application/json"}

    @staticmethod
    def create_contact(data: dict) -> dict:
        if requests is None:
            raise RuntimeError("requests package is required for CRMTool")
        logger.info("Creating CRM contact")
        resp = requests.post(f"{CRM_API_URL}/contacts", json=data, headers=CRMTool.headers)
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def find_duplicate(email: str) -> bool:
        if requests is None:
            raise RuntimeError("requests package is required for CRMTool")
        logger.info(f"Checking duplicates for {email}")
        resp = requests.get(f"{CRM_API_URL}/contacts", params={"email": email}, headers=CRMTool.headers)
        resp.raise_for_status()
        return bool(resp.json().get("results"))

    @staticmethod
    def get_deal(deal_id: str) -> dict:
        if requests is None:
            raise RuntimeError("requests package is required for CRMTool")
        logger.info(f"Fetching deal {deal_id}")
        resp = requests.get(f"{CRM_API_URL}/deals/{deal_id}", headers=CRMTool.headers)
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def update_deal(deal_id: str, data: dict) -> dict:
        if requests is None:
            raise RuntimeError("requests package is required for CRMTool")
        logger.info(f"Updating deal {deal_id}")
        resp = requests.put(f"{CRM_API_URL}/deals/{deal_id}", json=data, headers=CRMTool.headers)
        resp.raise_for_status()
        return resp.json()
