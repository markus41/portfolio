"""Autonomous Customer Support agent."""

from __future__ import annotations

import re
from typing import Any, Dict

from agentic_core import (
    AbstractAgent,
    EventBus,
    MemoryService,
    run_maybe_async,
    run_sync,
)
from ...utils.logger import get_logger

logger = get_logger(__name__)


class SupportAgent(AbstractAgent):
    """Handle incoming customer messages for a tenant."""

    # Prompt shown to the GPT engine for intent detection / replies
    SUPPORT_PROMPT = """
You are SupportBot for tenant {{tenant_id}}.
Use the available tools to lookup orders and issue refunds.
If user asks "where is my order {{order_id}}" respond with its status.
For late deliveries over 3 days, refund up to 15%.
Unknown or complex requests should be escalated via a ticket.
Reply in JSON like {"text": "..."}.
Example:
User: my package {{order_id}} is late
Assistant: {"text": "Apologies, issuing 10% refund."}
User: where is order {{order_id}}?
Assistant: {"text": "Order is in transit"}
Keep answers short and helpful.
""".strip()

    def __init__(
        self, tenant_id: str, memory: MemoryService, bus: EventBus, toolbox: Any
    ) -> None:
        super().__init__("support")
        self.tenant_id = tenant_id
        self.memory = memory
        self.bus = bus
        self.tools = toolbox
        self.bus.subscribe("Customer.Message", self.run)

    def _extract_order_id(self, text: str) -> str | None:
        match = re.search(r"(\d{3,})", text)
        return match.group(1) if match else None

    async def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        text = payload.get("text", "")
        customer_id = payload.get("customer_id")
        lowered = text.lower()
        order_id = self._extract_order_id(text)
        reply_text = ""
        escalate = False

        if any(k in lowered for k in ["status", "where", "track"]):
            if order_id:
                info = self.tools.lookup_order(order_id)
                reply_text = f"Order {order_id} status: {info.get('status', 'unknown')}"
            else:
                reply_text = "Please provide an order id so I can check the status."
        elif any(k in lowered for k in ["late", "delay"]):
            if order_id:
                info = self.tools.lookup_order(order_id)
                days = int(info.get("days_delayed", 0))
                pct = min(15, max(0, days * 5))
                receipt = self.tools.issue_refund(order_id, pct)
                reply_text = f"Sorry for the delay. A {pct}% refund was issued. Receipt {receipt}."
            else:
                reply_text = "I'm sorry about the delay. Please share your order id."
        else:
            ticket = self.tools.create_ticket(text, customer_id)
            reply_text = f"I've escalated your request. Ticket {ticket}."
            escalate = True

        await run_maybe_async(
            self.bus.publish,
            "Support.Reply",
            {"customer_id": customer_id, "text": reply_text},
        )
        self.memory.store(f"faq:{self.tenant_id}", [f"Q:{text}", f"A:{reply_text}"])
        logger.info(f"Responded to customer {customer_id}")
        return {"text": reply_text, "escalate": escalate}

    def run_sync(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Compatibility wrapper running :meth:`run` synchronously."""
        return run_sync(self.run(payload))


def main() -> None:
    """Run a simple demo when executed as a script."""

    bus = EventBus()
    memory = MemoryService()

    class Toolbox:
        def lookup_order(self, order_id: str) -> dict:
            return {"status": "shipped", "days_delayed": 4}

        def issue_refund(self, order_id: str, pct: int) -> str:
            return "r123"

        def create_ticket(self, summary: str, customer_id: str) -> str:
            return "t789"

    agent = SupportAgent("demo", memory, bus, Toolbox())

    bus.publish("Customer.Message", {"customer_id": "c1", "text": "Where is order 42?"})
    bus.publish(
        "Customer.Message", {"customer_id": "c2", "text": "My order 99 is late"}
    )


if __name__ == "__main__":  # pragma: no cover - manual demo
    main()
