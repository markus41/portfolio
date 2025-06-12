<!-- README.md -->

# 🚀 Brookside BI – Autonomous Sales & Marketing Agents

Welcome to the Brookside BI Agentic System! This repo contains a modular, turn-based framework of specialized AI “expert” agents that power everything from lead capture to contract delivery, all orchestrated under a central Orchestrator agent. Whether you’re adding a new campaign agent or tweaking your CRM integration, you’ll find a clean separation of concerns that makes extending and testing your workflow a breeze.

---

## 🔍 What’s Inside

├── .coding/
│ └─ Code-style & linting configs
├── src/
│ ├─ agents/ – Core agent implementations
│ │   ├─ base_agent.py
│ │   ├─ chatbot_agent.py
│ │   ├─ crm_pipeline_agent.py
│ │   ├─ lead_capture_agent.py
│ │   ├─ segmentation_ad_targeting_agent.py
│ │   └─ analytics_agent.py
│ ├─ tools/ – Helper utilities used by agents
│ ├─ constants.py – Env vars & API keys
│ └─ teams/ – RoundRobinGroupChat definitions
├── Frameworks/
│ └─ sales_team_full/ – Legacy AutoGen configs
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