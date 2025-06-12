# src/tests/test_segmentation.py

import pytest
from src.agents.segmentation_ad_targeting_agent import SegmentationAdTargetingAgent

def test_segmentation_targeting(monkeypatch):
    agent = SegmentationAdTargetingAgent()
    # stub out AdTool methods
    monkeypatch.setattr("src.tools.ad_tool.AdTool.create_facebook_campaign",
                        lambda self,n,a,b: {"campaign_id":"fb1"})
    monkeypatch.setattr("src.tools.ad_tool.AdTool.create_google_campaign",
                        lambda self,n,k,b: {"campaign_id":"ga1"})
    payload = {
        "segments":[{"name":"A","criteria":{"facebook_audiences":[1],"google_keywords":["x"]}}],
        "budget_per_segment":100
    }
    res = agent.run(payload)
    assert res["targeting_results"][0]["facebook"]["campaign_id"] == "fb1"
    assert res["targeting_results"][0]["google"]["campaign_id"]  == "ga1"

