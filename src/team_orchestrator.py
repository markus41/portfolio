"""Lightweight orchestrator for a single agent team.

This class understands the AutoGen team specification format.  Team
configuration files now use the ``autogen`` namespace instead of the old
``autogen_core``/``autogen_agentchat`` packages.  A minimal example::

    {
        "provider": "autogen.agentchat.teams.RoundRobinGroupChat",
        "config": {
            "participants": [
                {"provider": "src.agents.roles.AssistantAgent",
                 "config": {"name": "sales_agent"}}
            ]
        }
    }

``TeamOrchestrator`` only resolves the participants into local agent classes so
tests remain lightweight even when the AutoGen package is unavailable.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from agentic_core import EventBus, AsyncEventBus

try:  # pragma: no cover - optional AutoGen dependency
    import autogen
except Exception:  # pragma: no cover - tests still run without it
    autogen = None

from .base_orchestrator import BaseOrchestrator
from .utils.plugin_loader import load_agent


class TeamOrchestrator(BaseOrchestrator):
    """Load a team config and delegate events to its agents."""

    def __init__(
        self, config_path: str, bus: EventBus | AsyncEventBus | None = None
    ) -> None:
        """Initialise the orchestrator from a team JSON file.

        Parameters
        ----------
        config_path:
            Path to the JSON configuration describing the team. The file must
            include a ``config.participants`` array. Each participant item is
            expected to define ``config.name`` pointing to an agent module under
            :mod:`src.agents`.

        The configuration may also provide a ``responsibilities`` array listing
        the agent names allowed to run within this team. Any participant not
        present in this list will cause a :class:`ValueError` during
        initialisation.


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
        # Keep the raw specification for downstream AutoGen integration
        # without forcing the dependency at test time.
        self.team_config: Dict[str, Any] = data

        self.responsibilities: list[str] = data.get("responsibilities", [])
        participants = data.get("config", {}).get("participants", [])

        if self.responsibilities:
            for part in participants:
                name = part.get("config", {}).get("name")
                if name and name not in self.responsibilities:
                    raise ValueError(
                        f"Agent '{name}' not permitted by responsibilities"
                    )

        bus = bus or AsyncEventBus()
        super().__init__(bus=bus)

        for part in participants:
            name = part.get("config", {}).get("name")
            if not name:
                continue
            agent_cls = load_agent(name)
            self.agents[name] = agent_cls()

        # Optionally construct the AutoGen chat team when the dependency is
        # installed.  The exact API differs across AutoGen versions so we guard
        # the call in a try/except block and fall back to ``None`` if anything
        # goes wrong.  Tests do not require the external package to be present.
        self.autogen_team = None
        if autogen is not None:
            try:  # pragma: no cover - external dependency
                self.autogen_team = autogen.from_dict(data)
            except Exception:  # pragma: no cover - ignore API mismatches
                self.autogen_team = None
