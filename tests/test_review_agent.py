from agentic_core import EventBus
from src.agents.review_agent import ReviewAgent
from src.agents.base_agent import BaseAgent


class DraftAgent(BaseAgent):
    """Minimal author agent used in tests."""

    def __init__(self, bus: EventBus):
        self.bus = bus

    def run(self, payload):
        draft = payload.get("text", "")
        self.bus.publish("draft.created", {"draft": draft})
        return {"status": "submitted", "draft": draft}


def test_review_agent_approves():
    bus = EventBus()
    reviews = []
    bus.subscribe("draft.reviewed", reviews.append)

    review_agent = ReviewAgent(bus)
    author = DraftAgent(bus)

    author.run({"text": "All good here"})
    assert reviews[0]["status"] == "approved"


def test_review_agent_rejects():
    bus = EventBus()
    reviews = []
    bus.subscribe("draft.reviewed", reviews.append)

    review_agent = ReviewAgent(bus, banned_words={"bad"})
    author = DraftAgent(bus)

    author.run({"text": "This is a bad idea"})
    assert reviews[0]["status"] == "rejected"
    assert "bad" in reviews[0]["comments"][0].lower()
