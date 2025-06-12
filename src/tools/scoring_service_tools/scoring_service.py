from __future__ import annotations
from math import exp


def score_lead(features: dict) -> dict:
    """Naive logistic scoring for a lead."""
    # Example weights
    weight = {
        "company_size": 0.02,
        "annual_revenue": 0.000001,
        "engagement": 0.05,
    }
    z = (
        features.get("company_size", 0) * weight["company_size"]
        + features.get("annual_revenue", 0) * weight["annual_revenue"]
        + features.get("engagement", 0) * weight["engagement"]
    )
    prob = 1 / (1 + exp(-z))
    tier = "hot" if prob >= 0.75 else "warm" if prob >= 0.45 else "cold"
    return {"score": prob * 100, "tier": tier}
