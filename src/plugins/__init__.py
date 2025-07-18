"""Plugin stubs providing tool integrations."""

from .base_plugin import BaseToolPlugin
from .email_plugin import EmailPlugin
from .crm_plugin import CRMPlugin
from .scraping_plugin import ScrapingPlugin
from .cloud_docs_plugin import CloudDocsPlugin

# auto-generated simple business logic plugins used by the sales team
from .log_event_plugin import LogEventPlugin
from .invoke_agent_plugin import InvokeAgentPlugin
from .notify_human_plugin import NotifyHumanPlugin
from .lead_capture_plugin import LeadCapturePlugin
from .lead_enrichment_plugin import LeadEnrichmentPlugin
from .lead_scoring_plugin import LeadScoringPlugin
from .email_outreach_plugin import EmailOutreachPlugin
from .generate_proposal_plugin import GenerateProposalPlugin
from .negotiation_agent_plugin import NegotiationAgentPlugin
from .contract_agent_plugin import ContractAgentPlugin
from .onboarding_agent_plugin import OnboardingAgentPlugin
from .csat_checker_agent_plugin import CsatCheckerAgentPlugin
from .upsell_agent_plugin import UpsellAgentPlugin
from .referral_agent_plugin import ReferralAgentPlugin
from .chatbot_agent_plugin import ChatbotAgentPlugin
from .visitor_tracking_plugin import VisitorTrackingPlugin
from .segmentation_and_targeting_plugin import SegmentationAndTargetingPlugin
from .crm_entry_dedup_plugin import CrmEntryDedupPlugin
from .crm_pipeline_agent_plugin import CrmPipelineAgentPlugin
from .push_metric_plugin import PushMetricPlugin

__all__ = [
    "BaseToolPlugin",
    "EmailPlugin",
    "CRMPlugin",
    "ScrapingPlugin",
    "CloudDocsPlugin",
    "LogEventPlugin",
    "InvokeAgentPlugin",
    "NotifyHumanPlugin",
    "LeadCapturePlugin",
    "LeadEnrichmentPlugin",
    "LeadScoringPlugin",
    "EmailOutreachPlugin",
    "GenerateProposalPlugin",
    "NegotiationAgentPlugin",
    "ContractAgentPlugin",
    "OnboardingAgentPlugin",
    "CsatCheckerAgentPlugin",
    "UpsellAgentPlugin",
    "ReferralAgentPlugin",
    "ChatbotAgentPlugin",
    "VisitorTrackingPlugin",
    "SegmentationAndTargetingPlugin",
    "CrmEntryDedupPlugin",
    "CrmPipelineAgentPlugin",
    "PushMetricPlugin",
]
