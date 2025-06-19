"""Common abstract base class for all agents used in the examples."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseAgent(ABC):
    """Define the minimal interface required by the orchestrator."""

    #: Optional list of capabilities advertised by the agent.  Orchestrators may
    #: use these to dynamically select an agent for a given task.
    skills: List[str] = []

    @abstractmethod
    def run(self, payload: Dict[str, Any]) -> Any:
        """Process the input ``payload`` and return a result."""

        # subclasses implement their specific logic here
        pass
