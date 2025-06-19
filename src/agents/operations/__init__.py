"""Operations agent package.

This subpackage bundles agents dealing with logistics, procurement,
notifications and other back office tasks. Each class can be imported
directly from :mod:`src.agents.operations`. Modules are loaded lazily on
first attribute access to keep import overhead low.

Example
-------
>>> from src.agents.operations import InboundAgent
>>> agent = InboundAgent()
"""

import importlib
from types import ModuleType
from typing import Dict

__all__ = [
    "CSATCheckerAgent",
    "CSATSchedulerAgent",
    "DummyCliAgent",
    "NotificationAgent",
    "InboundAgent",
    "OutboundAgent",
    "InventoryManagementAgent",
    "TMSAgent",
    "FulfillmentAgent",
    "OnRoadAgent",
    "EcommerceAgent",
    "ProcurementAgent",
    "SupportAgent",
]

_module_map: Dict[str, str] = {
    "CSATCheckerAgent": "csat_checker_agent",
    "CSATSchedulerAgent": "csat_scheduler_agent",
    "DummyCliAgent": "dummy_cli_agent",
    "NotificationAgent": "notification_agent",
    "InboundAgent": "inbound_agent",
    "OutboundAgent": "outbound_agent",
    "InventoryManagementAgent": "inventory_management_agent",
    "TMSAgent": "tms_agent",
    "FulfillmentAgent": "fulfillment_agent",
    "OnRoadAgent": "on_road_agent",
    "EcommerceAgent": "ecommerce_agent",
    "ProcurementAgent": "procurement_agent",
    "SupportAgent": "support_agent",
}

def __getattr__(name: str):
    if name in _module_map:
        module: ModuleType = importlib.import_module(f'.{_module_map[name]}', __name__)
        attr = getattr(module, name)
        globals()[name] = attr
        return attr
    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')
