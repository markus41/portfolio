from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml
except Exception:  # pragma: no cover - optional dependency
    yaml = None

from .base_agent import BaseAgent
from ..tools.integration_tools.crm_tools import CRMConnector
from ..tools.integration_tools.erp_tools import ERPConnector
from ..tools.integration_tools.payment_tools import PaymentConnector
from ..tools.integration_tools.office_tools import OfficeConnector

logger = logging.getLogger(__name__)


class IntegrationAgent(BaseAgent):
    """Execute config-driven data integrations between external systems."""

    skills = ["integration"]

    def __init__(self, config_path: str) -> None:
        self.systems: Dict[str, Any] = {}
        self.integrations: List[Dict[str, Any]] = []
        self.load_config(config_path)

    def load_config(self, path: str) -> None:
        """Load YAML configuration and initialise connectors."""
        logger.info(f"Loading integration config from {path}")
        try:
            text = Path(path).read_text()
        except FileNotFoundError:
            logger.warning(f"Integration config not found: {path}")
            return
        if yaml:
            cfg = yaml.safe_load(text) or {}
        else:
            try:
                cfg = json.loads(text)
            except Exception:
                logger.error("Unable to parse integration config without PyYAML")
                return
        self.integrations = cfg.get("integrations", [])
        self.systems = {}
        for name, spec in cfg.get("systems", {}).items():
            typ = spec.get("type")
            subtype = spec.get("subtype", "")
            creds = spec.get("credentials", {})
            if typ == "crm":
                self.systems[name] = CRMConnector(subtype, creds)
            elif typ == "erp":
                self.systems[name] = ERPConnector(subtype, creds)
            elif typ == "payment":
                self.systems[name] = PaymentConnector(subtype, creds)
            elif typ == "office":
                self.systems[name] = OfficeConnector(subtype, creds)
            else:
                logger.warning(f"Unknown system type {typ} for {name}")
        logger.info(
            "Loaded %d integrations across %d systems",
            len(self.integrations),
            len(self.systems),
        )

    # ------------------------------------------------------------------
    def _retry(self, fn, *args, **kwargs):
        delay = 1.0
        for attempt in range(1, 4):
            try:
                return fn(*args, **kwargs)
            except Exception as exc:  # pragma: no cover - defensive
                logger.error(f"Attempt {attempt} failed: {exc}")
                if attempt == 3:
                    raise
                time.sleep(delay)
                delay *= 2

    # ------------------------------------------------------------------
    def plan_integrations(self) -> List[Dict[str, Any]]:
        """Return a list of pipeline execution plans."""
        plans: List[Dict[str, Any]] = []
        for item in self.integrations:
            steps = [
                {"source": item["source"], "target": item["target"], "object": obj}
                for obj in item.get("objects", [])
            ]
            plans.append({"name": item["name"], "steps": steps})
        logger.info("Planned %d integration pipelines", len(plans))
        return plans

    def execute_integration(self, plan: Dict[str, Any]) -> None:
        """Execute the given integration ``plan``."""
        name = plan.get("name")
        logger.info(f"Executing integration {name}")
        for step in plan.get("steps", []):
            src = self.systems[step["source"]]
            tgt = self.systems[step["target"]]
            obj = step["object"]
            records = self._retry(src.fetch_data, obj) or []
            for rec in records:
                self._retry(tgt.send_data, obj, rec)
            src_count = self._retry(src.count_data, obj)
            tgt_count = self._retry(tgt.count_data, obj)
            if tgt_count >= src_count:
                logger.info(f"{name}:{obj} Verification passed")
            else:
                logger.error(
                    f"{name}:{obj} Verification failed {tgt_count}/{src_count}"
                )

    # ------------------------------------------------------------------
    def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle an ``integration_request`` task."""
        if task.get("type") != "integration_request":
            logger.warning("Ignoring unknown task type %s", task.get("type"))
            return {"status": "ignored"}
        target = task.get("payload", {}).get("name")
        plan = next((p for p in self.plan_integrations() if p["name"] == target), None)
        if not plan:
            logger.error(f"No integration named {target}")
            return {"status": "not_found"}
        self.execute_integration(plan)
        return {"status": "done", "name": target}

    def run(self, payload: Dict[str, Any]) -> Any:
        """Compatibility wrapper for :class:`BaseOrchestrator`."""
        return self.handle_task({"type": "integration_request", "payload": payload})
