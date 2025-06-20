from __future__ import annotations

from dataclasses import dataclass
from typing import List

try:  # pragma: no cover - optional dependency
    import requests
except Exception:  # pragma: no cover - optional dependency
    requests = None

from .config import settings
from .utils.logger import get_logger
from .user_context import get_current

logger = get_logger(__name__)


@dataclass
class Deal:
    """Minimal CRM deal representation used by RevOpsAgent."""

    id: str
    amount: float
    stage: str
    days_in_stage: int
    last_touch: str
    probability: float


def fetch_deals(tenant_id: str) -> List[Deal]:
    """Return deals for ``tenant_id`` from the configured CRM system.

    The function calls ``settings.CRM_API_URL`` using ``settings.CRM_API_KEY``
    for authentication and expects the API to return JSON containing either a
    list of deal dictionaries or an object with a ``"results"`` key holding that
    list.  Each dictionary is mapped to a :class:`Deal` instance.  Example
    response shape::

        {
            "results": [
                {
                    "id": "d1",
                    "amount": 1000,
                    "stage": "Proposal",
                    "days_in_stage": 5,
                    "last_touch": "2025-06-01",
                    "probability": 0.6
                }
            ]
        }

    Raises ``RuntimeError`` if the optional ``requests`` dependency is missing.
    """

    if not getattr(requests, "get", None):  # pragma: no cover - optional dep
        logger.warning(
            "requests package is not installed or lacks 'get'; returning empty list"
        )
        return []

    current = get_current()
    url = f"{(current.crm_api_url if current and current.crm_api_url else settings.CRM_API_URL)}/deals"
    key = current.crm_api_key if current else settings.CRM_API_KEY
    headers = {"Authorization": f"Bearer {key}"}
    params = {"tenant_id": tenant_id}

    logger.info(f"Fetching deals for tenant {tenant_id}")
    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    payload = resp.json()

    raw_deals = payload.get("results", payload)
    deals: List[Deal] = []
    for item in raw_deals:
        try:
            deals.append(
                Deal(
                    id=str(item["id"]),
                    amount=float(item.get("amount", 0.0)),
                    stage=item.get("stage", ""),
                    days_in_stage=int(item.get("days_in_stage", 0)),
                    last_touch=item.get("last_touch", ""),
                    probability=float(item.get("probability", 0.0)),
                )
            )
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning(f"Skipping invalid deal entry: {exc}")

    return deals
