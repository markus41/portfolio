# src/agents/chatbot_agent.py

from .base_agent import BaseAgent
import importlib
from ..utils.logger import get_logger

logger = get_logger(__name__)

class ChatbotAgent(BaseAgent):
    def __init__(self):
        ChatTool = importlib.import_module("src.tools.chat_tool").ChatTool
        self.chat_tool = ChatTool()

    def run(self, payload: dict) -> dict:
        """
        payload: {
          "messages": [
            {"role": "system", "content": "..."},
            {"role": "user",   "content": "..."}
          ]
        }
        """
        logger.info("Running ChatbotAgent")
        response = self.chat_tool.chat(payload["messages"])
        return {"response": response}
