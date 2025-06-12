from src.agents.real_estate_lead_agent import RealEstateLeadAgent
from src.agents.mls_agent import MLSAgent
from src.agents.listing_agent import ListingAgent
from src.agents.listing_poster_agent import ListingPosterAgent


def test_real_estate_lead_agent(monkeypatch):
    monkeypatch.setattr(
        "src.tools.real_estate_tools.lead_finder.LeadFinder.search_leads",
        lambda self, city: [{"email": "a@b.com"}],
    )
    agent = RealEstateLeadAgent()
    out = agent.run({"city": "Austin"})
    assert out["leads"][0]["email"] == "a@b.com"


def test_mls_agent(monkeypatch):
    monkeypatch.setattr(
        "src.tools.real_estate_tools.mls_client.MLSClient.pull_listing",
        lambda self, mls_id: {"id": mls_id, "price": 100},
    )
    agent = MLSAgent()
    out = agent.run({"mls_id": "123"})
    assert out["listing"]["id"] == "123"


def test_listing_agent():
    agent = ListingAgent()
    listing = {"address": "123 Main", "price": 500000, "details": "nice"}
    out = agent.run(listing)
    assert out["listing"]["price"] == 500000


def test_listing_poster_agent(monkeypatch):
    monkeypatch.setattr(
        "src.tools.real_estate_tools.listing_poster.ListingPoster.post",
        lambda self, listing: {"status": "ok"},
    )
    agent = ListingPosterAgent()
    out = agent.run({"listing": {"id": "1"}})
    assert out["result"]["status"] == "ok"
