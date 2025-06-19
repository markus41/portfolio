# src/tests/test_lead_capture.py

from src.agents.sales.lead_capture_agent import LeadCaptureAgent
from src.events import LeadCaptureEvent


def test_lead_capture_normalization():
    agent = LeadCaptureAgent()
    payload = LeadCaptureEvent(
        form_data={"Email": "Test@Ex.com", "Name": " Foo ", "Phone": "(123) 456-7890"},
        source="web",
    )
    out = agent.run(payload)
    assert out["lead"]["email"] == "test@ex.com"
    assert out["lead"]["name"] == "Foo"
    assert out["lead"]["phone"] == "1234567890"
    assert out["status"] == "captured"
