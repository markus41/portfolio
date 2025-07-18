from typing import Any, Dict
from .base_plugin import BaseToolPlugin


class OnboardingAgentPlugin(BaseToolPlugin):
    """Kick off onboarding steps for a client."""

    name = "onboarding_agent"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        client_id = payload.get("client_id")
        print(f"Onboarding client {client_id}")
        return {"status": "onboarding_started", "client_id": client_id}
