"""Common abstract base class for all agents used in the examples."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgent(ABC):
    """Define the minimal interface required by the orchestrator."""

    @abstractmethod
    def run(self, payload: Dict[str, Any]) -> Any:
        """Process the input ``payload`` and return a result."""

        # subclasses implement their specific logic here
        pass
