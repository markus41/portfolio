"""Wrapper around the OpenAI Chat API used by :class:`ChatbotAgent`."""

try:
    import openai
except ImportError:  # pragma: no cover - optional dependency
    openai = None

from ..config import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)
if openai:
    openai.api_key = settings.OPENAI_API_KEY


class ChatTool:
    """Minimal helper for calling ``openai.ChatCompletion``."""

    def chat(self, messages: list, model: str = "gpt-4") -> str:
        """Return the assistant reply for ``messages`` using ``model``."""
        logger.info("Invoking OpenAI ChatCompletion")
        if not openai:
            raise RuntimeError("openai package is not installed")
        resp = openai.ChatCompletion.create(model=model, messages=messages)
        return resp.choices[0].message.content
