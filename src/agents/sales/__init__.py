"""Sales and marketing agent package.

Agents in this package focus on lead generation, deal management and
customer engagement. Importing a class lazily loads the underlying
module the first time it is accessed.

Example
-------
>>> from src.agents.sales import LeadCaptureAgent
>>> agent = LeadCaptureAgent()
"""

import importlib
from types import ModuleType
from typing import Dict

__all__ = [
    "AnalyticsAgent",
    "ChatbotAgent",
    "ContractAgent",
    "ContractSignMonitorAgent",
    "CRMEntryAgent",
    "CRMPipelineAgent",
    "EmailReplyMonitorAgent",
    "HumanApprovalAgent",
    "LeadCaptureAgent",
    "LeadEnrichmentAgent",
    "LeadScoringAgent",
    "NegotiationAgent",
    "OnboardingAgent",
    "OutreachAgent",
    "ProposalGeneratorAgent",
    "ReferralAgent",
    "RevOpsAgent",
    "SchedulingAgent",
    "SegmentationAdTargetingAgent",
    "UpsellAgent",
    "VisitorTrackingAgent",
]

_module_map: Dict[str, str] = {
    "AnalyticsAgent": "analytics_agent",
    "ChatbotAgent": "chatbot_agent",
    "ContractAgent": "contract_agent",
    "ContractSignMonitorAgent": "contract_sign_monitor_agent",
    "CRMEntryAgent": "crm_entry_agent",
    "CRMPipelineAgent": "crm_pipeline_agent",
    "EmailReplyMonitorAgent": "email_reply_monitor_agent",
    "HumanApprovalAgent": "human_approval_agent",
    "LeadCaptureAgent": "lead_capture_agent",
    "LeadEnrichmentAgent": "lead_enrichment_agent",
    "LeadScoringAgent": "lead_scoring_agent",
    "NegotiationAgent": "negotiation_agent",
    "OnboardingAgent": "onboarding_agent",
    "OutreachAgent": "outreach_agent",
    "ProposalGeneratorAgent": "proposal_generator_agent",
    "ReferralAgent": "referral_agent",
    "RevOpsAgent": "revops_agent",
    "SchedulingAgent": "scheduling_agent",
    "SegmentationAdTargetingAgent": "segmentation_ad_targeting_agent",
    "UpsellAgent": "upsell_agent",
    "VisitorTrackingAgent": "visitor_tracking_agent",
}


def __getattr__(name: str):
    if name in _module_map:
        module: ModuleType = importlib.import_module(f".{_module_map[name]}", __name__)
        attr = getattr(module, name)
        globals()[name] = attr
        return attr
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
