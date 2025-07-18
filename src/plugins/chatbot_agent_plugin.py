from typing import Any, Dict
from .base_plugin import BaseToolPlugin


class ChatbotAgentPlugin(BaseToolPlugin):
    """Answer visitor questions with canned responses."""

    name = "chatbot_agent"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        visitor_id = payload.get("visitor_id")
        question = payload.get("question")
        print(f"Chatbot handling question for visitor {visitor_id}: {question}")
        return {"status": "answered", "visitor_id": visitor_id}
