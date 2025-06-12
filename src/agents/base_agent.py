# src/agents/base_agent.py

from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    @abstractmethod
    def run(self, payload: Dict[str, Any]) -> Any:
        """Process input payload and return result."""
        pass
