# Agent & Tool Catalog

This page lists all of the built-in agents available in the Brookside BI framework along with the most commonly used utility modules.

## Agents

* **AnalyticsAgent** (`src/agents/sales/analytics_agent.py`) – Push a metric to Prometheus via the PrometheusPusher tool.
* **BaseAgent** (`src/agents/base_agent.py`) – Common abstract base class for all agents used in the examples.
* **ChatbotAgent** (`src/agents/sales/chatbot_agent.py`) – Agent wrapping a very small OpenAI `ChatCompletion` invocation.
* **ContractAgent** (`src/agents/sales/contract_agent.py`) – Handles contract operations.
* **ContractSignMonitorAgent** (`src/agents/sales/contract_sign_monitor_agent.py`) – Handles contract sign monitor operations.
* **CRMEntryAgent** (`src/agents/sales/crm_entry_agent.py`) – Handles crmentry operations.
* **CRMPipelineAgent** (`src/agents/sales/crm_pipeline_agent.py`) – Advance deals through a CRM pipeline and schedule follow-ups.
* **CSATCheckerAgent** (`src/agents/operations/csat_checker_agent.py`) – Handles csatchecker operations.
* **CSATSchedulerAgent** (`src/agents/operations/csat_scheduler_agent.py`) – Handles csatscheduler operations.
* **EmailReplyMonitorAgent** (`src/agents/sales/email_reply_monitor_agent.py`) – Handles email reply monitor operations.
* **HumanApprovalAgent** (`src/agents/sales/human_approval_agent.py`) – Handles human approval operations.
* **LeadCaptureAgent** (`src/agents/sales/lead_capture_agent.py`) – Extract and normalise lead form submissions.
* **LeadEnrichmentAgent** (`src/agents/sales/lead_enrichment_agent.py`) – Handles lead enrichment operations.
* **LeadScoringAgent** (`src/agents/sales/lead_scoring_agent.py`) – Handles lead scoring operations.
* **NegotiationAgent** (`src/agents/sales/negotiation_agent.py`) – Handles negotiation operations.
* **NotificationAgent** (`src/agents/operations/notification_agent.py`) – Handles notification operations.
* **OnboardingAgent** (`src/agents/sales/onboarding_agent.py`) – Handles onboarding operations.
* **OutreachAgent** (`src/agents/sales/outreach_agent.py`) – Handles outreach operations.
* **ProposalGeneratorAgent** (`src/agents/sales/proposal_generator_agent.py`) – Handles proposal generator operations.
* **ReferralAgent** (`src/agents/sales/referral_agent.py`) – Handles referral operations.
* **SchedulingAgent** (`src/agents/sales/scheduling_agent.py`) – Handles scheduling operations.
* **SegmentationAdTargetingAgent** (`src/agents/sales/segmentation_ad_targeting_agent.py`) – Create ad campaigns for multiple audience segments.
* **UpsellAgent** (`src/agents/sales/upsell_agent.py`) – Handles upsell operations.
* **VisitorTrackingAgent** (`src/agents/sales/visitor_tracking_agent.py`) – Logs visitor activity and forwards events to your analytics service.
* **RealEstateLeadAgent** (`src/agents/real_estate/real_estate_lead_agent.py`) – Locate potential real-estate buyers or sellers.
* **MLSAgent** (`src/agents/real_estate/mls_agent.py`) – Agent that pulls listing data from the MLS.
* **ListingAgent** (`src/agents/real_estate/listing_agent.py`) – Construct simple listing dictionaries for property data.
* **ListingPosterAgent** (`src/agents/real_estate/listing_poster_agent.py`) – Agent that posts real estate listings to external portals.
* **InboundAgent** (`src/agents/operations/inbound_agent.py`) – Process an inbound trailer and update inventory.
* **OutboundAgent** (`src/agents/operations/outbound_agent.py`) – Process an outbound trailer and decrement inventory.
* **InventoryManagementAgent** (`src/agents/operations/inventory_management_agent.py`) – Update inventory counts.
* **TMSAgent** (`src/agents/operations/tms_agent.py`) – Update shipment status in the TMS.
* **FulfillmentAgent** (`src/agents/operations/fulfillment_agent.py`) – Fulfill an e-commerce order.
* **OnRoadAgent** (`src/agents/operations/on_road_agent.py`) – Update live location for a shipment.
* **EcommerceAgent** (`src/agents/operations/ecommerce_agent.py`) – Create a new ecommerce order.
* **ProcurementAgent** (`src/agents/operations/procurement_agent.py`) – Agent for automating material purchasing decisions.
* **SupportAgent** (`src/agents/operations/support_agent.py`) – Autonomous Customer Support agent.
* **RevOpsAgent** (`src/agents/sales/revops_agent.py`) – Revenue operations agent producing pipeline forecasts.
* **ReviewAgent** (`src/agents/review_agent.py`) – Validates drafts and publishes approval results.
* **PlannerAgent** (`src/agents/planner_agent.py`) – Executes goal-based plans by sequencing events across teams.

## Key Utilities

Brookside BI's utilities live under `src/tools/` and provide integrations that agents can call directly.

- **CRM tools** (`crm_tools/`) – connectors for Salesforce, HubSpot, Monday and other CRMs.
- **Notification tools** (`notification_tools/`) – helpers for Slack, Teams, SMS and more.
- **Real estate tools** (`real_estate_tools/`) – fetch MLS data and post property listings.
- **Operations tools** (`operations_tools/`) – inventory management and transportation APIs.
- **Segmentation tools** (`segmentation_tools/`) – create ad audiences from customer data.
- **Metrics utilities** (`metrics_tools/`) – push custom gauges to Prometheus.
- Other modules support document generation, scheduling, e-commerce and memory services.
