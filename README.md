<!-- README.md -->

# 🚀 Brookside BI – Autonomous Sales & Marketing Agents

Welcome to the Brookside BI Agentic System! This repo contains a modular, turn-based framework of specialized AI “expert” agents that power everything from lead capture to contract delivery, all orchestrated under a central Orchestrator agent. Whether you’re adding a new campaign agent or tweaking your CRM integration, you’ll find a clean separation of concerns that makes extending and testing your workflow a breeze.

---

## 🔍 What’s Inside

├── .coding/
│ └─ Code-style & linting configs
├── Agents/
│ ├─ base_agent.py – Core abstract interface
│ ├─ orchestrator_agent.py – Routes & sequences your workflow
│ ├─ chatbot_agent.py – Live Q&A chatbot
│ ├─ contract_agent.py – E-signature & contract tracking
│ ├─ crm_entry_agent.py – Safe CRM create/update & dedupe
│ ├─ crm_pipeline_agent.py – Deal stage monitoring & nudges
│ ├─ csat_checker_agent.py – CSAT survey & recovery flows
│ ├─ lead_capture_agent.py – Normalize inbound lead data
│ ├─ lead_enrichment_agent.py – Firmographic & social enrichment
│ ├─ lead_scoring_agent.py – Rule/ML-based lead scoring
│ ├─ negotiation_agent.py – Price negotiation & discounts
│ ├─ onboarding_agent.py – Welcome sequences & tasks
│ ├─ outreach_agent.py – Draft & send emails via SendGrid
│ ├─ proposal_generator_agent.py – Generate Word/PDF proposals
│ ├─ referral_agent.py – Request & track referrals
│ ├─ scheduling_agent.py – Google Calendar event creation
│ ├─ segmentation_ad_targeting_agent.py – Audience clustering & ad triggers
│ ├─ upsell_agent.py – Cross-sell/upsell automation
│ └─ visitor_tracking_agent.py – Fingerprinting & page-view logging
├── Frameworks/
│ └─ sales_team_full/ – AutoGen JSON & orchestrator configs
├── Engines/
│ ├─ constants.py – Env vars & API keys
│ ├─ logger.py – Standardized structured logging
│ └─ disqualifier_engine.py – (Example) rule-based gating logic
├── Teams/
│ └─ sales_team_full.json – Full RoundRobinGroupChat definition
├── Tools/
│ ├─ crm_tools/ – CRM API wrappers
│ │ ├─ crm_tool.py
│ │ └─ pipeline_monitor.py
│ ├─ lead_enrichment_tools/ – Firmographic & social enrichment
│ │ └─ lead_enrichment.py
│ ├─ leadcapture_tools/ – Inbound form normalization
│ │ └─ lead_capture.py
│ ├─ memory_tools/ – Vector & session memory clients
│ │ ├─ memory_client.py
│ │ └─ memory_service.py
│ ├─ orchestration_tools/ – Custom workbench & event processors
│ │ ├─ AwaitHumanApproval.ts
│ │ ├─ event_processor.ts
│ │ ├─ ingest_event.ts
│ │ └─ OrchestratorWorker.ts
│ ├─ playbooks/ – Workflow definitions & lookup
│ │ ├─ playbook.json
│ │ └─ playbook_lookup.ts
│ ├─ scoring_service_tools/ – External scoring service wrappers
│ │ └─ scoring_service.py
│ ├─ segmentation_tools/ – Audience segmentation logic
│ │ └─ segmenter.py
│ └─ visitor_tracking_tools/ – Session stitching & analytics
│ └─ session_stitcher.py
├── Tests/
│ ├─ test_chatbot_agent.py
│ ├─ test_crm_pipeline_agent.py
│ ├─ test_lead_capture.py
│ ├─ test_segmentation.py
│ └─ … pytest suite for every Agent & orchestrator
└── README.md – YOU ARE HERE!