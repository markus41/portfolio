# src/agents/onboarding_agent.py

from .base_agent import BaseAgent
from ..tools.email_tool import EmailTool
from ..utils.logger import get_logger

logger = get_logger(__name__)

class OnboardingAgent(BaseAgent):
    def __init__(self):
        self.email = EmailTool()

    def run(self, payload):
        """
        payload: {
          "to": str,
          "welcome_message": str,
          "tasks": [ {"title": str, "due": "YYYY-MM-DD"} ]
        }
        """
        self.email.send_email(
            to_email=payload["to"],
            subject="Welcome aboard!",
            html_content=payload["welcome_message"]
        )
        # could integrate PlannerTool here to create tasks...
        logger.info(f"Sent welcome to {payload['to']}")
        return {"status": "onboarded"}
