# Agent & Tool Catalog

This page lists all of the built-in agents available in the Brookside BI framework along with the most commonly used utility modules.

## Agents

* **AnalyticsAgent** (`src/agents/analytics_agent.py`) – Push a metric to Prometheus via the PrometheusPusher tool.
* **BaseAgent** (`src/agents/base_agent.py`) – Common abstract base class for all agents used in the examples.
* **ChatbotAgent** (`src/agents/chatbot_agent.py`) – Agent wrapping a very small OpenAI `ChatCompletion` invocation.
* **ContractAgent** (`src/agents/contract_agent.py`) – Handles contract operations.
* **ContractSignMonitorAgent** (`src/agents/contract_sign_monitor_agent.py`) – Handles contract sign monitor operations.
* **CRMEntryAgent** (`src/agents/crm_entry_agent.py`) – Handles crmentry operations.
* **CRMPipelineAgent** (`src/agents/crm_pipeline_agent.py`) – Advance deals through a CRM pipeline and schedule follow-ups.
* **CSATCheckerAgent** (`src/agents/csat_checker_agent.py`) – Handles csatchecker operations.
* **CSATSchedulerAgent** (`src/agents/csat_scheduler_agent.py`) – Handles csatscheduler operations.
* **EmailReplyMonitorAgent** (`src/agents/email_reply_monitor_agent.py`) – Handles email reply monitor operations.
* **HumanApprovalAgent** (`src/agents/human_approval_agent.py`) – Handles human approval operations.
* **LeadCaptureAgent** (`src/agents/lead_capture_agent.py`) – Extract and normalise lead form submissions.
* **LeadEnrichmentAgent** (`src/agents/lead_enrichment_agent.py`) – Handles lead enrichment operations.
* **LeadScoringAgent** (`src/agents/lead_scoring_agent.py`) – Handles lead scoring operations.
* **NegotiationAgent** (`src/agents/negotiation_agent.py`) – Handles negotiation operations.
* **NotificationAgent** (`src/agents/notification_agent.py`) – Handles notification operations.
* **OnboardingAgent** (`src/agents/onboarding_agent.py`) – Handles onboarding operations.
* **OutreachAgent** (`src/agents/outreach_agent.py`) – Handles outreach operations.
* **ProposalGeneratorAgent** (`src/agents/proposal_generator_agent.py`) – Handles proposal generator operations.
* **ReferralAgent** (`src/agents/referral_agent.py`) – Handles referral operations.
* **SchedulingAgent** (`src/agents/scheduling_agent.py`) – Handles scheduling operations.
* **SegmentationAdTargetingAgent** (`src/agents/segmentation_ad_targeting_agent.py`) – Create ad campaigns for multiple audience segments.
* **UpsellAgent** (`src/agents/upsell_agent.py`) – Handles upsell operations.
* **VisitorTrackingAgent** (`src/agents/visitor_tracking_agent.py`) – Handles visitor tracking operations.
* **RealEstateLeadAgent** (`src/agents/real_estate_lead_agent.py`) – Locate potential real-estate buyers or sellers.
* **MLSAgent** (`src/agents/mls_agent.py`) – Agent that pulls listing data from the MLS.
* **ListingAgent** (`src/agents/listing_agent.py`) – Construct simple listing dictionaries for property data.
* **ListingPosterAgent** (`src/agents/listing_poster_agent.py`) – Agent that posts real estate listings to external portals.
* **InboundAgent** (`src/agents/inbound_agent.py`) – Process an inbound trailer and update inventory.
* **OutboundAgent** (`src/agents/outbound_agent.py`) – Process an outbound trailer and decrement inventory.
* **InventoryManagementAgent** (`src/agents/inventory_management_agent.py`) – Update inventory counts.
* **TMSAgent** (`src/agents/tms_agent.py`) – Update shipment status in the TMS.
* **FulfillmentAgent** (`src/agents/fulfillment_agent.py`) – Fulfill an e-commerce order.
* **OnRoadAgent** (`src/agents/on_road_agent.py`) – Update live location for a shipment.
* **EcommerceAgent** (`src/agents/ecommerce_agent.py`) – Create a new ecommerce order.
* **ProcurementAgent** (`src/agents/procurement_agent.py`) – Agent for automating material purchasing decisions.
* **SupportAgent** (`src/agents/support_agent.py`) – Autonomous Customer Support agent.
* **RevOpsAgent** (`src/agents/revops_agent.py`) – Revenue operations agent producing pipeline forecasts.

## Key Utilities

Brookside BI's utilities live under `src/tools/` and provide integrations that agents can call directly.

- **CRM tools** (`crm_tools/`) – connectors for Salesforce, HubSpot, Monday and other CRMs.
- **Notification tools** (`notification_tools/`) – helpers for Slack, Teams, SMS and more.
- **Real estate tools** (`real_estate_tools/`) – fetch MLS data and post property listings.
- **Operations tools** (`operations_tools/`) – inventory management and transportation APIs.
- **Segmentation tools** (`segmentation_tools/`) – create ad audiences from customer data.
- **Metrics utilities** (`metrics_tools/`) – push custom gauges to Prometheus.
- Other modules support document generation, scheduling, e-commerce and memory services.
