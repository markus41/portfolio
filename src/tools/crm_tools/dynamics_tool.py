# Tools/crm_tools/dynamics_tool.py

import requests
from msal import ConfidentialClientApplication
from ...config import settings
from ...utils.logger import get_logger

logger = get_logger(__name__)


class DynamicsTool:
    def __init__(self):
        authority = f"https://login.microsoftonline.com/{settings.DYNAMICS_TENANT_ID}"
        scope = [f"{settings.DYNAMICS_API_URL}/.default"]
        self.app = ConfidentialClientApplication(
            client_id=settings.DYNAMICS_CLIENT_ID,
            authority=authority,
            client_credential=settings.DYNAMICS_CLIENT_SECRET,
        )
        self.base_url = settings.DYNAMICS_API_URL

    def _get_token(self) -> str:
        result = self.app.acquire_token_for_client(scopes=[f"{self.base_url}/.default"])
        token = result.get("access_token")
        if not token:
            raise RuntimeError("Failed to acquire Dynamics access token")
        return token

    def create_contact(self, data: dict) -> dict:
        token = self._get_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        resp = requests.post(f"{self.base_url}/contacts", json=data, headers=headers)
        resp.raise_for_status()
        return resp.json()

    def get_contact(self, contact_id: str) -> dict:
        token = self._get_token()
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(f"{self.base_url}/contacts({contact_id})", headers=headers)
        resp.raise_for_status()
        return resp.json()

    def update_contact(self, contact_id: str, data: dict) -> bool:
        token = self._get_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        resp = requests.patch(
            f"{self.base_url}/contacts({contact_id})", json=data, headers=headers
        )
        resp.raise_for_status()
        return resp.status_code == 204
