"""Generic e-commerce platform client used for order operations."""

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None

from ..constants import ECOMMERCE_API_URL, ECOMMERCE_API_KEY
from ..utils.logger import get_logger

logger = get_logger(__name__)

class EcommerceTool:
    def create_order(self, order: dict) -> dict:
        logger.info("Creating ecommerce order")
        if not requests:
            raise RuntimeError("requests package is not installed")
        resp = requests.post(
            f"{ECOMMERCE_API_URL}/orders",
            json=order,
            headers={"Authorization": f"Bearer {ECOMMERCE_API_KEY}"},
        )
        resp.raise_for_status()
        return resp.json()

    def get_order(self, order_id: str) -> dict:
        logger.info(f"Fetching order {order_id}")
        if not requests:
            raise RuntimeError("requests package is not installed")
        resp = requests.get(
            f"{ECOMMERCE_API_URL}/orders/{order_id}",
            headers={"Authorization": f"Bearer {ECOMMERCE_API_KEY}"},
        )
        resp.raise_for_status()
        return resp.json()
