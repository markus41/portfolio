from src.agents.roles import AssistantAgent, WriterAgent, AnalystAgent


def test_assistant_permissions():
    agent = AssistantAgent()
    assert agent.can_use("chat_tool")
    assert agent.run({"tool": "chat_tool"}) == {"status": "ok"}
    denied = agent.run({"tool": "unknown_tool"})
    assert denied["error"] == "permission_denied"


def test_writer_permissions():
    agent = WriterAgent()
    assert agent.can_use("docgen_tool")
    assert not agent.can_use("crm_tool")


def test_analyst_permissions():
    agent = AnalystAgent()
    assert agent.can_use("metrics_tools")
    assert agent.run({"tool": "metrics_tools"}) == {"status": "ok"}

