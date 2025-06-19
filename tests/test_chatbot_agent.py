# src/tests/test_chatbot_agent.py

from src.agents.sales.chatbot_agent import ChatbotAgent
from src.events import ChatbotEvent


class DummyChatTool:
    def chat(self, messages, model="gpt-4"):
        return "OK"


def test_chatbot(monkeypatch):
    monkeypatch.setattr("src.tools.chat_tool.ChatTool", DummyChatTool)
    agent = ChatbotAgent()
    event = ChatbotEvent(messages=[{"role": "user", "content": "Hello"}])
    out = agent.run(event)
    assert out["response"] == "OK"
