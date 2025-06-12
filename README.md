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
├── tests/
│ ├─ test_chatbot_agent.py
│ ├─ test_crm_pipeline_agent.py
│ ├─ test_lead_capture.py
│ ├─ test_segmentation.py
│ └─ … pytest suite for every Agent & orchestrator
└── README.md – YOU ARE HERE!
