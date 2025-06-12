# src/tests/test_lead_capture.py

from src.agents.lead_capture_agent import LeadCaptureAgent

def test_lead_capture_normalization():
    agent = LeadCaptureAgent()
    payload = {"form_data":{"Email":"Test@Ex.com","Name":" Foo ","Phone":"(123) 456-7890"},"source":"web"}
    out = agent.run(payload)
    assert out["lead"]["email"] == "test@ex.com"
    assert out["lead"]["name"] == "Foo"
    assert out["lead"]["phone"] == "1234567890"
    assert out["status"] == "captured"
