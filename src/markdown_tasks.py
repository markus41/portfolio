"""Utilities for loading goal-based task plans from Markdown files."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


def load_goals_from_markdown(path: str | Path) -> Dict[str, List[Dict[str, Any]]]:
    """Parse ``path`` and return planner plans.

    The parser looks for lines starting with ``"## Goal:"``. Any bullet line
    following such a header is interpreted as a JSON task specification until
    the next goal header is reached.
    Each bullet must contain a JSON object with ``team`` and ``event`` keys.
    """
    p = Path(path)
    current_goal: str | None = None
    tasks: List[Dict[str, Any]] = []
    plans: Dict[str, List[Dict[str, Any]]] = {}
    for line in p.read_text().splitlines():
        line = line.strip()
        if line.startswith("## Goal:"):
            if current_goal is not None:
                plans[current_goal] = tasks
            current_goal = line.partition("## Goal:")[2].strip()
            tasks = []
        elif line.startswith("-") and current_goal:
            try:
                task = json.loads(line.lstrip("- "))
            except json.JSONDecodeError:
                continue
            if isinstance(task, dict):
                tasks.append(task)
    if current_goal is not None:
        plans[current_goal] = tasks
    return plans
