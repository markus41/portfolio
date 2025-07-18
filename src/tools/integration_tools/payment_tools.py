from __future__ import annotations
import logging

try:
    import requests
except Exception:  # pragma: no cover - optional dependency
    requests = None

logger = logging.getLogger(__name__)


class PaymentConnector:
    """Payment processor connector."""

    def __init__(self, subtype: str, creds: dict) -> None:
        self.subtype = subtype
        self.base_url = creds.get("url", "").rstrip("/")
        self.headers = creds.get("headers", {})

    def _request(self, method: str, path: str, **kwargs):
        if not requests:
            raise RuntimeError("requests package is not installed")
        url = f"{self.base_url}/{path.lstrip('/')}"
        resp = requests.request(method, url, headers=self.headers, **kwargs)
        resp.raise_for_status()
        try:
            return resp.json()
        except Exception:  # pragma: no cover
            return {}

    def fetch_data(self, obj: str):
        logger.info(f"Payment({self.subtype}) fetching {obj}")
        return self._request("GET", obj)

    def send_data(self, obj: str, data):
        logger.info(f"Payment({self.subtype}) sending {obj}")
        return self._request("POST", obj, json=data)

    def count_data(self, obj: str) -> int:
        logger.info(f"Payment({self.subtype}) counting {obj}")
        data = self._request("GET", f"{obj}/count")
        if isinstance(data, dict):
            return int(data.get("count", 0))
        return 0
