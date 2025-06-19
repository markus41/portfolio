"""Transportation management system API client."""

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None

from ...config import settings
from ...utils.logger import get_logger

logger = get_logger(__name__)

class TMSTool:
    def create_shipment(self, data: dict) -> dict:
        logger.info("Creating shipment in TMS")
        if not requests:
            raise RuntimeError("requests package is not installed")
        resp = requests.post(
            f"{settings.TMS_API_URL}/shipments",
            json=data,
            headers={"Authorization": f"Bearer {settings.TMS_API_KEY}"},
        )
        resp.raise_for_status()
        return resp.json()

    def update_status(self, shipment_id: str, status: str) -> dict:
        logger.info(f"Updating shipment {shipment_id} status to {status}")
        if not requests:
            raise RuntimeError("requests package is not installed")
        resp = requests.put(
            f"{settings.TMS_API_URL}/shipments/{shipment_id}",
            json={"status": status},
            headers={"Authorization": f"Bearer {settings.TMS_API_KEY}"},
        )
        resp.raise_for_status()
        return resp.json()
