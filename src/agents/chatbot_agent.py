"""Agent wrapping a very small OpenAI `ChatCompletion` invocation."""

from .base_agent import BaseAgent
import importlib
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ChatbotAgent(BaseAgent):
    """Generate chat completions using the :mod:`chat_tool` utility."""

    def __init__(self):
        # Import ChatTool lazily so tests can monkeypatch it easily
        ChatTool = importlib.import_module("src.tools.chat_tool").ChatTool
        self.chat_tool = ChatTool()

    def run(self, payload: dict) -> dict:
        """Return the assistant response for a list of chat messages.

        Parameters
        ----------
        payload:
            Dictionary containing a ``messages`` key compatible with the
            OpenAI Chat API.
        """

        logger.info("Running ChatbotAgent")
        # forward the messages to ChatTool which wraps the OpenAI call
        response = self.chat_tool.chat(payload["messages"])
        return {"response": response}
