# src/tools/chat_tool.py

try:
    import openai
except ImportError:  # pragma: no cover - optional dependency
    openai = None

from ..constants import OPENAI_API_KEY
from ..utils.logger import get_logger

logger = get_logger(__name__)
if openai:
    openai.api_key = OPENAI_API_KEY

class ChatTool:
    def chat(self, messages: list, model: str = "gpt-4") -> str:
        logger.info("Invoking OpenAI ChatCompletion")
        if not openai:
            raise RuntimeError("openai package is not installed")
        resp = openai.ChatCompletion.create(model=model, messages=messages)
        return resp.choices[0].message.content
