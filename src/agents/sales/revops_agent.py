from __future__ import annotations

"""Revenue operations agent producing pipeline forecasts."""

import json
from dataclasses import dataclass
from typing import List

from agentic_core import (
    AbstractAgent,
    EventBus,
    AsyncEventBus,
    run_maybe_async,
    run_sync,
)

from ...crm_connector import Deal, fetch_deals
from ...utils.logger import get_logger
from ...config import settings
from ...user_context import get_current

try:  # pragma: no cover - optional dependency
    import openai
except Exception:  # pragma: no cover - optional dependency
    openai = None

logger = get_logger(__name__)

STALE_DAYS = 30


@dataclass
class KPI:
    total_pipeline: float
    avg_cycle_time: float
    stalled_count: int


class RevOpsAgent(AbstractAgent):
    """Respond to ``RevOps.Analyze`` events with deal forecasts."""

    def __init__(self, bus: EventBus | AsyncEventBus) -> None:
        super().__init__("revops")
        self.bus = bus
        if openai:
            openai.api_key = settings.OPENAI_API_KEY
        self.bus.subscribe("RevOps.Analyze", self.run)

    def _summarize_kpis(self, deals: List[Deal]) -> KPI:
        if not deals:
            return KPI(0.0, 0.0, 0)
        total = sum(d.amount for d in deals)
        avg_cycle = sum(d.days_in_stage for d in deals) / len(deals)
        stalled = sum(1 for d in deals if d.days_in_stage > STALE_DAYS)
        return KPI(total, avg_cycle, stalled)

    def _ask_gpt(self, prompt: str) -> dict:
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

    async def run(self, payload: dict) -> dict:
        tenant = payload.get("tenant_id")
        deals = fetch_deals(tenant)
        kpi = self._summarize_kpis(deals)
        prompt = (
            f"Total pipeline ${kpi.total_pipeline:.2f}, avg cycle {kpi.avg_cycle_time:.1f} days, "
            f"stalled {kpi.stalled_count}. Forecast Q(close -> revenue) and top 3 risks "
            f"& recommended next actions (JSON)."
        )
        try:
            analysis = self._ask_gpt(prompt)
        except Exception as exc:  # pragma: no cover - network failures
            logger.warning(f"GPT analysis failed: {exc}")
            analysis = {"forecast": "unknown", "risks": [], "actions": []}

        report = {
            "tenant": tenant,
            "forecast": analysis.get("forecast"),
            "risks": analysis.get("risks", []),
            "actions": analysis.get("actions", []),
        }
        await run_maybe_async(self.bus.publish, "RevOps.Report", report)
        return report

    def run_sync(self, payload: dict) -> dict:
        """Compatibility wrapper running :meth:`run` synchronously."""
        return run_sync(self.run(payload))
