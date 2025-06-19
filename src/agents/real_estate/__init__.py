"""Real estate agent package.

Agents focused on property listings and lead generation for real estate
workflows. Modules are imported lazily the first time a class is
accessed.

Example
-------
>>> from src.agents.real_estate import MLSAgent
>>> agent = MLSAgent()
"""

import importlib
from types import ModuleType
from typing import Dict

__all__ = [
    "RealEstateLeadAgent",
    "MLSAgent",
    "ListingAgent",
    "ListingPosterAgent",
]

_module_map: Dict[str, str] = {
    "RealEstateLeadAgent": "real_estate_lead_agent",
    "MLSAgent": "mls_agent",
    "ListingAgent": "listing_agent",
    "ListingPosterAgent": "listing_poster_agent",
}


def __getattr__(name: str):
    if name in _module_map:
        module: ModuleType = importlib.import_module(f'.{_module_map[name]}', __name__)
        attr = getattr(module, name)
        globals()[name] = attr
        return attr
    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')
