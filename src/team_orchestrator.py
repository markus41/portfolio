"""Lightweight orchestrator for a single agent team."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from agentic_core import EventBus, AsyncEventBus

from .base_orchestrator import BaseOrchestrator
from .utils.plugin_loader import load_agent


class TeamOrchestrator(BaseOrchestrator):
    """Load a team config and delegate events to its agents."""

    def __init__(self, config_path: str, bus: EventBus | AsyncEventBus | None = None) -> None:
        """Initialise the orchestrator from a team JSON file.

        Parameters
        ----------
        config_path:
            Path to the JSON configuration describing the team. The file must
            include a ``config.participants`` array. Each participant item is
            expected to define ``config.name`` pointing to an agent module under
            :mod:`src.agents`.

        Notes
        -----
        At construction time every participant listed in the JSON is resolved
        using :func:`~src.utils.plugin_loader.load_agent`. This function looks
        for classes registered via the ``brookside.agents`` entry point group
        before falling back to modules under :mod:`src.agents`. The orchestrator
        then instantiates the resulting agent classes and registers them on an
        internal event bus (:class:`EventBus` or :class:`AsyncEventBus`) for
        message routing.
        """
        self.config_path = Path(config_path)
        with self.config_path.open() as fh:
            data = json.load(fh)
        participants = data.get("config", {}).get("participants", [])

        bus = bus or AsyncEventBus()
        super().__init__(bus=bus)

        for part in participants:
            name = part.get("config", {}).get("name")
            if not name:
                continue
            agent_cls = load_agent(name)
            self.agents[name] = agent_cls()

