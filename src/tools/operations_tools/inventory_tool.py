"""Simple inventory management API client."""

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None

from ...constants import INVENTORY_API_URL, INVENTORY_API_KEY
from ...utils.logger import get_logger

logger = get_logger(__name__)

class InventoryTool:
    def update_inventory(self, item_id: str, quantity: int) -> dict:
        logger.info(f"Updating inventory {item_id} by {quantity}")
        if not requests:
            raise RuntimeError("requests package is not installed")
        resp = requests.post(
            f"{INVENTORY_API_URL}/items/{item_id}",
            json={"quantity": quantity},
            headers={"Authorization": f"Bearer {INVENTORY_API_KEY}"},
        )
        resp.raise_for_status()
        return resp.json()

    def get_item(self, item_id: str) -> dict:
        logger.info(f"Fetching inventory item {item_id}")
        if not requests:
            raise RuntimeError("requests package is not installed")
        resp = requests.get(
            f"{INVENTORY_API_URL}/items/{item_id}",
            headers={"Authorization": f"Bearer {INVENTORY_API_KEY}"},
        )
        resp.raise_for_status()
        return resp.json()
