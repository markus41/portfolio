# src/tests/test_chatbot_agent.py

from src.agents.chatbot_agent import ChatbotAgent

class DummyChatTool:
    def chat(self, messages, model="gpt-4"): return "OK"

def test_chatbot(monkeypatch):
    monkeypatch.setattr("src.tools.chat_tool.ChatTool", DummyChatTool)
    agent = ChatbotAgent()
    out = agent.run({"messages":[{"role":"user","content":"Hello"}]})
    assert out["response"] == "OK"
