"""Base interface for custom tool plugins."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseToolPlugin(ABC):
    """Define the minimal interface for pluggable tools."""

    name: str = ""

    @abstractmethod
    def execute(self, payload: Dict[str, Any]) -> Any:
        """Run the plugin using ``payload`` and return a result."""
        raise NotImplementedError
