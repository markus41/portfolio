"""Lightweight NLP parameter extraction utilities."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Dict, List, Optional


_MONTHS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}


def _parse_budget(text: str) -> Optional[int]:
    """Return an integer budget if found in ``text``."""

    match = re.search(
        r"(?:budget\s*(?:is|of)?\s*\$?(\d+[\d,]*))(?:\s*dollars|\b)",
        text,
        re.IGNORECASE,
    )
    if match:
        value = match.group(1).replace(",", "")
        try:
            return int(value)
        except ValueError:
            pass
    return None


def _standardize_date(date_str: str) -> str:
    """Convert ``date_str`` to ``YYYY-MM-DD`` if possible."""

    formats = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%m/%d/%y",
        "%d/%m/%Y",
        "%d/%m/%y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue

    m = re.match(
        r"(?P<mon>\w+)\s+(?P<day>\d{1,2})(?:st|nd|rd|th)?(?:,?\s*(?P<year>\d{4}))?",
        date_str,
        re.IGNORECASE,
    )
    if m:
        mon = _MONTHS.get(m.group("mon")[:3].lower())
        if mon:
            year = int(m.group("year")) if m.group("year") else datetime.utcnow().year
            day = int(m.group("day"))
            try:
                return datetime(year, mon, day).strftime("%Y-%m-%d")
            except ValueError:
                pass

    return date_str.strip()


def _parse_dates(text: str) -> List[str]:
    """Return a list of dates detected in ``text``.

    Dates are returned in ISO ``YYYY-MM-DD`` format when possible."""

    patterns = [
        r"\b\d{4}-\d{2}-\d{2}\b",
        r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
        r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+\d{1,2}(?:st|nd|rd|th)?(?:,?\s*\d{4})?\b",
    ]
    matches: List[str] = []
    for pat in patterns:
        matches.extend(re.findall(pat, text, re.IGNORECASE))

    return [_standardize_date(m) for m in matches]


def _parse_target_audience(text: str) -> Optional[str]:
    """Return a target audience phrase if found."""

    patterns = [
        r"target audience is ([^.,;]+?)\b",
        r"targeting ([^.,;]+?)(?=\s+(?:on|with|for|$))",
        r"for ([^.,;]+?) audience",
        r"for ([^.,;]+?)(?=\s+(?:on|with|$))",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return None


def parse_parameters(text: str) -> Dict[str, object]:
    """Extract common campaign parameters from ``text``."""

    return {
        "budget": _parse_budget(text),
        "dates": _parse_dates(text),
        "target_audience": _parse_target_audience(text),
    }


__all__ = ["parse_parameters"]
