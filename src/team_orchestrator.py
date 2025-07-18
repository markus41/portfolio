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
tests remain lightweight even when the AutoGen package is unavailable. Team
definitions may be written in JSON or YAML; the loader automatically detects
``.yaml``/``.yml`` extensions and parses them with :func:`yaml.safe_load` when
PyYAML is installed.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict
import types

try:  # pragma: no cover - optional dependency
    import jsonschema
except Exception:  # pragma: no cover - optional dependency
    from .jsonschema_stub import validate as _validate, ValidationError as _VE

    jsonschema = types.SimpleNamespace(validate=_validate, ValidationError=_VE)

from agentic_core import EventBus, AsyncEventBus

try:  # pragma: no cover - PyYAML is optional
    import yaml  # type: ignore
except Exception:  # pragma: no cover - not required unless YAML files are used
    yaml = None

try:  # pragma: no cover - optional AutoGen dependency
    import autogen
except Exception:  # pragma: no cover - tests still run without it
    autogen = None

from .base_orchestrator import BaseOrchestrator
from .utils.plugin_loader import load_agent
from .config import settings


_SCHEMA_PATH = Path(__file__).resolve().parent.parent / "docs" / "team_schema.json"
try:
    _TEAM_SCHEMA = json.loads(_SCHEMA_PATH.read_text())
except FileNotFoundError:  # pragma: no cover - schema missing in some envs
    _TEAM_SCHEMA = {}


def validate_team_config(data: Dict[str, Any]) -> None:
    """Validate ``data`` against :mod:`docs/team_schema.json`."""

    if _TEAM_SCHEMA and jsonschema is not None:
        jsonschema.validate(data, _TEAM_SCHEMA)


class TeamOrchestrator(BaseOrchestrator):
    """Load a team config and delegate events to its agents."""

    def __init__(
        self, config_path: str, bus: EventBus | AsyncEventBus | None = None
    ) -> None:
        """Initialise the orchestrator from a team configuration file.

        Parameters
        ----------
        config_path:
            Path to the JSON or YAML configuration describing the team. The file must
            include a ``config.participants`` array. Each participant item is
            expected to define ``config.name`` pointing to an agent module under
            :mod:`src.agents`.

        The configuration may also provide a ``responsibilities`` array listing
        the agent names allowed to run within this team. Any participant not
        present in this list will cause a :class:`ValueError` during
        initialisation.


        Notes
        -----
        At construction time every participant listed in the configuration file is resolved
        using :func:`~src.utils.plugin_loader.load_agent`. This function looks
        for classes registered via the ``brookside.agents`` entry point group
        before falling back to modules under :mod:`src.agents`. The orchestrator
        then instantiates the resulting agent classes and registers them on an
        internal event bus (:class:`EventBus` or :class:`AsyncEventBus`) for
        message routing.
        """
        self.config_path = Path(config_path)
        text = self.config_path.read_text()
        if self.config_path.suffix in {".yaml", ".yml"}:
            if yaml is None:
                raise ModuleNotFoundError(
                    "PyYAML is required to load YAML team definitions"
                )
            data = yaml.safe_load(text)
        else:
            data = json.loads(text)
        try:
            validate_team_config(data)
        except jsonschema.ValidationError as exc:
            raise ValueError(f"Invalid team configuration: {exc.message}") from exc
        # Keep the raw specification for downstream AutoGen integration
        # without forcing the dependency at test time.
        self.team_config: Dict[str, Any] = data

        self.responsibilities: list[str] = data.get("responsibilities", [])
        participants = data.get("config", {}).get("participants", [])

        # ------------------------------------------------------------------
        # Resolve prompt files for any participants specifying ``prompt_path``.
        # ``<lang>`` within the path is replaced with ``settings.LANG`` to
        # enable localisation.  The resulting file contents are stored under
        # ``system_message`` for use by AutoGen at runtime.
        # ------------------------------------------------------------------
        lang = getattr(settings, "LANG", "en")
        for part in participants:
            cfg = part.get("config", {})
            prompt_path = cfg.get("prompt_path")
            if not prompt_path:
                continue
            path = Path(str(prompt_path).replace("<lang>", lang))
            if not path.is_absolute():
                path = self.config_path.parent / path
            try:
                cfg["system_message"] = path.read_text()
            except OSError:
                cfg["system_message"] = ""

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
