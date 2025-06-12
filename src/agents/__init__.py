"""Convenience imports for agent classes."""

import importlib
from types import ModuleType
from typing import Dict

__all__ = [
    'AnalyticsAgent',
    'BaseAgent',
    'ChatbotAgent',
    'ContractAgent',
    'ContractSignMonitorAgent',
    'CRMEntryAgent',
    'CRMPipelineAgent',
    'CSATCheckerAgent',
    'CSATSchedulerAgent',
    'EmailReplyMonitorAgent',
    'HumanApprovalAgent',
    'LeadCaptureAgent',
    'LeadEnrichmentAgent',
    'LeadScoringAgent',
    'NegotiationAgent',
    'NotificationAgent',
    'OnboardingAgent',
    'OutreachAgent',
    'ProposalGeneratorAgent',
    'ReferralAgent',
    'SchedulingAgent',
    'SegmentationAdTargetingAgent',
    'UpsellAgent',
    'VisitorTrackingAgent',
    'RealEstateLeadAgent',
    'MLSAgent',
    'ListingAgent',
    'ListingPosterAgent',
]

_module_map: Dict[str, str] = {
    'AnalyticsAgent': 'analytics_agent',
    'BaseAgent': 'base_agent',
    'ChatbotAgent': 'chatbot_agent',
    'ContractAgent': 'contract_agent',
    'ContractSignMonitorAgent': 'contract_sign_monitor_agent',
    'CRMEntryAgent': 'crm_entry_agent',
    'CRMPipelineAgent': 'crm_pipeline_agent',
    'CSATCheckerAgent': 'csat_checker_agent',
    'CSATSchedulerAgent': 'csat_scheduler_agent',
    'EmailReplyMonitorAgent': 'email_reply_monitor_agent',
    'HumanApprovalAgent': 'human_approval_agent',
    'LeadCaptureAgent': 'lead_capture_agent',
    'LeadEnrichmentAgent': 'lead_enrichment_agent',
    'LeadScoringAgent': 'lead_scoring_agent',
    'NegotiationAgent': 'negotiation_agent',
    'NotificationAgent': 'notification_agent',
    'OnboardingAgent': 'onboarding_agent',
    'OutreachAgent': 'outreach_agent',
    'ProposalGeneratorAgent': 'proposal_generator_agent',
    'ReferralAgent': 'referral_agent',
    'SchedulingAgent': 'scheduling_agent',
    'SegmentationAdTargetingAgent': 'segmentation_ad_targeting_agent',
    'UpsellAgent': 'upsell_agent',
    'VisitorTrackingAgent': 'visitor_tracking_agent',
    'RealEstateLeadAgent': 'real_estate_lead_agent',
    'MLSAgent': 'mls_agent',
    'ListingAgent': 'listing_agent',
    'ListingPosterAgent': 'listing_poster_agent',
}


def __getattr__(name: str):
    if name in _module_map:
        module: ModuleType = importlib.import_module(f'.{_module_map[name]}', __name__)
        attr = getattr(module, name)
        globals()[name] = attr
        return attr
    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')
