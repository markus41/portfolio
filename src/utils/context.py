"""Utilities for managing conversation context.

This module provides helpers to keep chat histories under a
configurable token limit. When the accumulated messages exceed the
threshold they are summarised and trimmed so downstream LLM calls
remain efficient.
"""

from __future__ import annotations

from typing import List, Dict


def _estimate_tokens(text: str) -> int:
    """Return a rough token count for ``text``.

    The implementation uses a simple word split which is good enough
    for trimming purposes without requiring extra dependencies.
    """

    return len(text.split())


def _simple_summary(texts: List[str], max_tokens: int) -> str:
    """Collapse ``texts`` into a short summary not exceeding ``max_tokens``."""

    combined = " ".join(texts)
    words = combined.split()
    if len(words) > max_tokens:
        words = words[:max_tokens]
        return " ".join(words) + " ..."
    return " ".join(words)


def summarise_messages(
    messages: List[Dict[str, str]],
    *,
    max_tokens: int = 2000,
    summary_tokens: int = 200,
) -> List[Dict[str, str]]:
    """Return ``messages`` trimmed with a summary if needed.

    Parameters
    ----------
    messages:
        Chat history as a list of OpenAI ChatCompletion style dicts.
    max_tokens:
        Threshold for the total token count. When exceeded older
        messages are summarised until the remainder plus summary fits
        within this limit.
    summary_tokens:
        Maximum tokens to allocate for the generated summary message.

    Notes
    -----
    The function uses a naive token estimation based on whitespace
    splitting.  This keeps the implementation lightweight while still
    providing sensible context management for unit tests.
    """

    def total_tokens(msgs: List[Dict[str, str]]) -> int:
        return sum(_estimate_tokens(m.get("content", "")) for m in msgs)

    current = list(messages)
    if total_tokens(current) <= max_tokens:
        return current

    removed: List[Dict[str, str]] = []
    # Remove from the start until there is space for the summary
    while current and total_tokens(current) > max_tokens - summary_tokens:
        removed.append(current.pop(0))

    summary_text = _simple_summary([m.get("content", "") for m in removed], summary_tokens)
    summary_msg = {
        "role": "system",
        "content": f"Summary of earlier messages: {summary_text}",
    }
    return [summary_msg] + current
