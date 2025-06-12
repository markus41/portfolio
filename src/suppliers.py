from __future__ import annotations

"""Supplier adapter interfaces for :class:`ProcurementAgent`."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
import random


@dataclass
class Quote:
    """Represent a supplier quote."""

    supplier_id: str
    price: Decimal
    delivery_days: int


class BaseSupplierAdapter(ABC):
    """Abstract supplier interface used by :class:`ProcurementAgent`."""

    supplier_id: str

    @abstractmethod
    def get_quote(self, item: str, qty: int) -> Quote:
        """Return a :class:`Quote` for ``item`` and ``qty``."""


class AcmeCement(BaseSupplierAdapter):
    """Dummy supplier returning random prices for cement."""

    supplier_id = "acme_cement"

    def get_quote(self, item: str, qty: int) -> Quote:
        price = Decimal(random.randint(95, 105)) * qty
        days = random.randint(3, 7)
        return Quote(self.supplier_id, price, days)


class SteelCorp(BaseSupplierAdapter):
    """Dummy supplier returning random prices for steel."""

    supplier_id = "steel_corp"

    def get_quote(self, item: str, qty: int) -> Quote:
        price = Decimal(random.randint(80, 110)) * qty
        days = random.randint(5, 10)
        return Quote(self.supplier_id, price, days)
