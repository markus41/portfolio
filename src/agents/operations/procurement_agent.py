from __future__ import annotations

"""Agent for automating material purchasing decisions."""

import json
from decimal import Decimal
from typing import Iterable, List

from agentic_core import (
    AbstractAgent,
    EventBus,
    AsyncEventBus,
    run_maybe_async,
    run_sync,
)
from ...suppliers import BaseSupplierAdapter, Quote
from ...utils.logger import get_logger
from ...config import settings
from ...user_context import get_current

try:
    import openai
except ImportError:  # pragma: no cover - optional dependency
    openai = None

logger = get_logger(__name__)

MAX_AUTO_APPROVAL = Decimal("50000")

EVALUATE_PROMPT = (
    "Given the following supplier quotes for {qty} x {item}:\n"
    "{quotes}\n"
    "Select the best supplier that meets the target of {target_days} days. "
    'Respond in JSON as {{"supplier_id": "...", "reason": "...", '
    '"requires_approval": false}}.'
)


class ProcurementAgent(AbstractAgent):
    """Subscribe to material requests and automate purchasing."""

    def __init__(
        self,
        bus: EventBus | AsyncEventBus,
        suppliers: Iterable[BaseSupplierAdapter],
    ) -> None:
        super().__init__("Procurement")
        self.bus = bus
        self.suppliers: List[BaseSupplierAdapter] = list(suppliers)
        if openai:
            openai.api_key = settings.OPENAI_API_KEY
        self.bus.subscribe("Project.MaterialsNeeded", self.run)

    def _format_prompt(
        self, item: str, qty: int, target_days: int, quotes: List[Quote]
    ) -> str:
        lines = [
            f"- {q.supplier_id}: ${q.price} in {q.delivery_days} days" for q in quotes
        ]
        return EVALUATE_PROMPT.format(
            item=item,
            qty=qty,
            target_days=target_days,
            quotes="\n".join(lines),
        )

    def _gpt_decide(self, prompt: str) -> dict:
        if not openai:
            raise RuntimeError("openai package is not installed")
        current = get_current()
        if current and current.openai_api_key:
            openai.api_key = current.openai_api_key
        resp = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            timeout=10,
        )
        return json.loads(resp.choices[0].message.content)

    def place_order(self, quote: Quote, item: str, qty: int) -> str:
        logger.info(
            f"Placing order with {quote.supplier_id} for {qty} {item} at ${quote.price}"
        )
        return "PO-0001"

    async def run(self, payload: dict) -> dict:
        item = payload.get("item")
        qty = int(payload.get("qty", 0))
        target_days = int(payload.get("target_days", 0))

        quotes = [s.get_quote(item, qty) for s in self.suppliers]
        valid = [q for q in quotes if q.delivery_days <= target_days]
        cheapest = min(valid or quotes, key=lambda q: q.price)

        try:
            decision = self._gpt_decide(
                self._format_prompt(item, qty, target_days, quotes)
            )
            supplier_id = decision.get("supplier_id", cheapest.supplier_id)
            reason = decision.get("reason", "")
            requires_approval = bool(decision.get("requires_approval", False))
            chosen = next((q for q in quotes if q.supplier_id == supplier_id), cheapest)
        except Exception as exc:  # pragma: no cover - network failures
            logger.warning(f"GPT evaluation failed: {exc}")
            chosen = cheapest
            reason = "Selected cheapest available supplier."
            requires_approval = False

        if chosen.price > MAX_AUTO_APPROVAL:
            requires_approval = True

        event = {
            "supplier_id": chosen.supplier_id,
            "item": item,
            "qty": qty,
            "price": str(chosen.price),
            "reason": reason,
        }

        if requires_approval:
            await run_maybe_async(
                self.bus.publish, "Procurement.PendingApproval", event
            )
            return {"status": "pending_approval", **event}

        order_id = self.place_order(chosen, item, qty)
        out_event = {**event, "order_id": order_id}
        await run_maybe_async(self.bus.publish, "Procurement.Ordered", out_event)
        return {"status": "ordered", **out_event}

    def run_sync(self, payload: dict) -> dict:
        """Compatibility wrapper running :meth:`run` synchronously."""
        return run_sync(self.run(payload))
