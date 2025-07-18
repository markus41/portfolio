from typing import Any, Dict
from .base_plugin import BaseToolPlugin


class InvokeAgentPlugin(BaseToolPlugin):
    """Simulate calling another agent and returning its status."""

    name = "invoke_agent"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        agent_id = payload.get("agent_id")
        inp = payload.get("input")
        print(f"Invoking {agent_id} with input: {inp}")
        return {"status": "done", "agent": agent_id}
