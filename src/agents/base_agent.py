"""Common abstract base class for all agents used in the examples."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseAgent(ABC):
    """Define the minimal interface required by the orchestrator."""

    #: Optional list of capabilities advertised by the agent.  Orchestrators may
    #: use these to dynamically select an agent for a given task.
    skills: List[str] = []

    #: Optional token budget available to the agent. When set, orchestrators
    #: track the estimated token usage of each call to :meth:`run` and may
    #: terminate execution once the budget is exhausted.
    token_budget: int | None = None

    #: Optional loop budget limiting how many times the agent may be invoked
    #: for a single task. Orchestrators increment a loop counter for every
    #: :meth:`run` call and stop once this limit is reached.
    loop_budget: int | None = None

    @abstractmethod
    def run(self, payload: Dict[str, Any]) -> Any:
        """Process the input ``payload`` and return a result."""

        # subclasses implement their specific logic here
        pass
