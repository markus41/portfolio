"""Lightweight orchestrator for a single agent team."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any, Dict

from agentic_core import EventBus


class TeamOrchestrator:
    """Load a team config and delegate events to its agents."""

    def __init__(self, config_path: str) -> None:
        self.config_path = Path(config_path)
        with self.config_path.open() as fh:
            data = json.load(fh)
        participants = data.get("config", {}).get("participants", [])

        self.bus = EventBus()
        self.agents: Dict[str, Any] = {}

        for part in participants:
            name = part.get("config", {}).get("name")
            if not name:
                continue
            module = importlib.import_module(f"src.agents.{name}")
            class_name = "".join(word.capitalize() for word in name.split("_"))
            agent_cls = getattr(module, class_name)
            self.agents[name] = agent_cls()

    def handle_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatch ``event`` to the appropriate team agent."""
        event_type = event.get("type")
        payload = event.get("payload", {})
        agent = self.agents.get(event_type)
        if not agent:
            return {"status": "ignored"}
        result = agent.run(payload)
        return {"status": "done", "result": result}
