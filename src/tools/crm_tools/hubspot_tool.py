# Tools/crm_tools/hubspot_tool.py

import requests
from ...config import settings
import logging

logger = logging.getLogger(__name__)


class HubSpotTool:
    def __init__(self):
        self.base_url = "https://api.hubapi.com"
        self.params = {"hapikey": settings.HUBSPOT_API_KEY}

    def create_contact(self, email: str, properties: dict) -> dict:
        url = f"{self.base_url}/crm/v3/objects/contacts"
        data = {"properties": {"email": email, **properties}}
        resp = requests.post(url, params=self.params, json=data)
        resp.raise_for_status()
        return resp.json()

    def get_contact_by_email(self, email: str) -> dict | None:
        url = f"{self.base_url}/crm/v3/objects/contacts/search"
        payload = {
            "filterGroups": [
                {
                    "filters": [
                        {"propertyName": "email", "operator": "EQ", "value": email}
                    ]
                }
            ],
            "limit": 1,
        }
        resp = requests.post(url, params=self.params, json=payload)
        resp.raise_for_status()
        results = resp.json().get("results", [])
        return results[0] if results else None

    def update_contact(self, contact_id: str, properties: dict) -> dict:
        url = f"{self.base_url}/crm/v3/objects/contacts/{contact_id}"
        data = {"properties": properties}
        resp = requests.patch(url, params=self.params, json=data)
        resp.raise_for_status()
        return resp.json()
