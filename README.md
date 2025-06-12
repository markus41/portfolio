<!-- README.md -->

# 🚀 Brookside BI – Autonomous Sales & Marketing Agents

Welcome to the Brookside BI Agentic System! This repo contains a modular, turn-based framework of specialized AI “expert” agents that power everything from lead capture to contract delivery, all orchestrated under a central Orchestrator agent. Whether you’re adding a new campaign agent or tweaking your CRM integration, you’ll find a clean separation of concerns that makes extending and testing your workflow a breeze.

---

## 🔍 What’s Inside

```
├── src/
│   ├── agents/                # Core agent implementations
│   ├── tools/                 # Reusable utilities used by agents
│   ├── constants.py           # Env vars & API keys
│   └── teams/                 # RoundRobinGroupChat definitions
├── tests/                     # pytest suite
└── README.md                  # You are here!
```

The `tools` package contains submodules for CRM integrations, email and doc generation, ad campaign helpers and more. Each agent has a corresponding unit test under `tests/`.
