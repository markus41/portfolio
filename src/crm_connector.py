from __future__ import annotations

from dataclasses import dataclass
from typing import List


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
    """Return deals for ``tenant_id``.

    This stub simply returns an empty list and should be replaced by a real CRM
    connector in production.
    """
    return []
