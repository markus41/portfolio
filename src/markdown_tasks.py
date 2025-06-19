"""Utilities for loading goal-based task plans from Markdown files."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List

from .utils.logger import get_logger


logger = get_logger(__name__)


GOAL_RE = re.compile(r"^##\s*Goal:\s*(.+)")
TASK_RE = re.compile(r"^[-*]\s+(\{.*\})$")


def load_goals_from_markdown(path: str | Path) -> Dict[str, List[Dict[str, Any]]]:
    """Parse ``path`` and return a mapping of goals to task sequences.

    The parser looks for ``## Goal:`` headers followed by JSON bullet items. Any
    text within fenced code blocks is ignored so that examples or documentation
    inside the Markdown do not interfere with parsing. Invalid JSON task lines
    are skipped with a warning.
    """

    p = Path(path)
    inside_fence = False
    current_goal: str | None = None
    tasks: List[Dict[str, Any]] = []
    plans: Dict[str, List[Dict[str, Any]]] = {}

    for raw_line in p.read_text().splitlines():
        line = raw_line.strip()

        if line.startswith("```"):
            inside_fence = not inside_fence
            continue
        if inside_fence or not line:
            continue

        m_goal = GOAL_RE.match(line)
        if m_goal:
            if current_goal is not None:
                plans[current_goal] = tasks
            current_goal = m_goal.group(1).strip()
            tasks = []
            continue

        m_task = TASK_RE.match(line)
        if m_task and current_goal:
            try:
                task = json.loads(m_task.group(1))
            except json.JSONDecodeError:  # pragma: no cover - user error
                logger.warning("Skipping invalid JSON task: %s", raw_line)
                continue
            if isinstance(task, dict):
                tasks.append(task)
            else:  # pragma: no cover - user error
                logger.warning("Skipping task that is not a JSON object: %s", raw_line)

    if current_goal is not None:
        plans[current_goal] = tasks

    return plans
