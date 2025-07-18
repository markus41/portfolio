from __future__ import annotations

"""Utilities for handling team configuration mappings."""

from typing import Iterable, Dict


def parse_team_mapping(pairs: Iterable[str]) -> Dict[str, str]:
    """Return mapping of team names to config paths.

    Parameters
    ----------
    pairs:
        Iterable of strings in the format ``NAME=PATH``. ``NAME`` is the
        identifier for the team and ``PATH`` points to its JSON configuration
        file.

    Returns
    -------
    dict[str, str]
        Mapping of team names to configuration file paths.

    Raises
    ------
    ValueError
        If any element of ``pairs`` does not contain an ``=`` separator.

    Examples
    --------
    >>> parse_team_mapping(["sales=src/teams/sales_team.json"])
    {'sales': 'src/teams/sales_team.json'}
    """

    mapping: Dict[str, str] = {}
    for pair in pairs:
        if "=" not in pair:
            raise ValueError(f"Invalid team spec '{pair}'. Use NAME=PATH")
        name, path = pair.split("=", 1)
        mapping[name] = path
    return mapping
