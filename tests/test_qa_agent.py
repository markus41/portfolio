import types
import sys

from agentic_core import EventBus


class DummySupportAgent:
    """Minimal SupportAgent replacement used for QA tests."""

    def __init__(self, replies):
        self.replies = list(replies)
        self.index = 0

    def run(self, payload):
        reply = self.replies[self.index]
        self.index += 1
        return reply


# Provide a stub SupportAgent module so src.qa_agent imports cleanly
stub_module = types.ModuleType("src.agents.support_agent")
stub_module.SupportAgent = DummySupportAgent
sys.modules.setdefault("src.agents.support_agent", stub_module)

from src.qa_agent import QAAgent


def test_qa_agent_reports_passed():
    bus = EventBus()
    reports = []
    bus.subscribe("QA.Report", reports.append)

    support = DummySupportAgent([{"text": "ok"}, {"text": "sure"}])
    agent = QAAgent(bus, support)

    result = agent.run_sync({"scripts": [{"text": "A"}, {"text": "B"}]})

    assert result == {"passed": True}
    assert reports == [{"passed": True}]


def test_qa_agent_reports_failed_for_unserializable():
    bus = EventBus()
    reports = []
    bus.subscribe("QA.Report", reports.append)

    # A reply containing a set is not JSON serializable
    support = DummySupportAgent([{"text": set()}])
    agent = QAAgent(bus, support)

    result = agent.run_sync({"scripts": [{"text": "fail"}]})

    assert result == {"passed": False}
    assert reports == [{"passed": False}]
