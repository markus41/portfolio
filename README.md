<!-- README.md -->

# 🚀 Brookside BI – Autonomous Sales & Marketing Agents

Welcome to the Brookside BI Agentic System! This repo contains a modular, turn-based framework of specialized AI “expert” agents that power everything from lead capture to contract delivery, all orchestrated under a central Orchestrator agent. Whether you’re adding a new campaign agent or tweaking your CRM integration, you’ll find a clean separation of concerns that makes extending and testing your workflow a breeze.

For a deeper explanation of the architecture—including the event bus, memory service and how AutoGen teams are loaded and how teams start running—see [docs/architecture.md](docs/architecture.md).

## ⚡ Quick Start

Install the requirements and run the unit tests to make sure everything is wired correctly:

```bash
pip install -r requirements.txt
pytest -q
```

You can exercise the orchestrator with a single team using a few lines of Python:

```python
from src.solution_orchestrator import SolutionOrchestrator

orch = SolutionOrchestrator({"sales": "src/teams/sales_team_full.json"})
orch.handle_event("sales", {"type": "lead_capture", "payload": {"email": "alice@example.com"}})
```

---

## 🔍 What’s Inside

```
├── src/
│   ├── agents/                # Core agent implementations
│   ├── tools/                 # Reusable utilities used by agents
│   ├── constants.py           # Env vars & API keys
│   ├── orchestrator.py        # Event bus wiring
│   ├── crm_connector.py       # CRM interface stubs
│   ├── dev_assist.py          # Boilerplate generator
│   ├── debugger_agent.py      # Auto patch suggestions
│   ├── qa_agent.py            # Conversation tester
│   └── teams/                 # RoundRobinGroupChat definitions
├── tests/                     # pytest suite
└── README.md                  # You are here!
```

The `tools` package contains submodules for CRM integrations, email and doc generation, ad campaign helpers and more. Each agent has a corresponding unit test under `tests/`.

### 🏡 Real Estate Expansion

A new `Real Estate Team` demonstrates how the framework can be adapted for other industries. It bundles agents for finding leads, pulling MLS data, creating listings and posting them to major portals. See `src/teams/real_estate_team.json` for the configuration and the accompanying tools under `src/tools/real_estate_tools`.

### 🚚 Operations & Fulfillment Teams

Several additional JSON configs showcase logistics workflows. New teams cover warehouse operations, inventory management, order fulfillment, driver tracking and e-commerce. These rely on the tools in `src/tools/operations_tools` and `src/tools/ecommerce_tool.py` for TMS, inventory and shopping cart integrations along with Microsoft Teams notifications.

### 🚧 Building Modular AutoGen Teams

The JSON files under `src/teams/` showcase how to wire multiple agents together
using [AutoGen](https://github.com/microsoft/autogen). Each file describes a
`RoundRobinGroupChat` with a list of **participants** and optional tools. To
create a new industry workflow:

1. Copy one of the existing team JSONs and update the `participants` section
   with your agents.
2. Add `FunctionTool` entries for any custom business logic your agents need.
3. Adjust the termination conditions (for example `MaxMessageTermination`) to
   control when the team conversation stops.

By editing these declarative configs you can quickly deploy specialised agent
teams for finance, healthcare, manufacturing or any other domain without
changing the core orchestrator code.

A trimmed example from `sales_team_full.json` looks like:

```json
{
  "provider": "autogen_agentchat.teams.RoundRobinGroupChat",
  "config": {
    "participants": [
      {"provider": "autogen_agentchat.agents.AssistantAgent", "config": {"name": "orchestrator_agent"}},
      {"provider": "autogen_agentchat.agents.AssistantAgent", "config": {"name": "lead_agent"}}
    ],
    "tools": [
      {"provider": "src.tools.crm_tool.CRMTool"}
    ]
  }
}
```

### 🧩 Team & Solution Orchestrators

Teams packaged as JSON in `src/teams/` can now be loaded at runtime using `TeamOrchestrator`. It creates all agents listed under `participants` and provides an `EventBus` for intra-team messaging. Multiple teams are combined with `SolutionOrchestrator` which routes events to the appropriate team and collects their results.

To initialise:
```python
from src.solution_orchestrator import SolutionOrchestrator

orch = SolutionOrchestrator({
    "sales": "src/teams/sales_team_full.json",
    "operations": "src/teams/operations_team.json",
})
orch.handle_event("sales", {"type": "lead_capture", "payload": {}})
```

Teams can report progress upward via `orch.report_status(team, status)`.

### 🌟 Creating Custom Teams

To design your own workflow start with one of the JSON files under
`src/teams/` and follow these steps:

1. **Add participants** – list your agent modules under the `participants`
   section. The orchestrator imports these modules dynamically at startup.
2. **Include tools** – provide any helper classes via `FunctionTool` entries so
   agents can call them directly in conversation.
3. **Set termination** – configure AutoGen options like
   `MaxMessageTermination` to decide when the conversation should stop.
4. **Register the file** – pass the JSON path to `SolutionOrchestrator` when
   constructing it. Events sent with the corresponding team name will trigger
   this new chat workflow.

Because teams are purely declarative you can spin up experimental flows without
editing the core Python code.

## 📦 Installation

Install the Python dependencies with pip using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

The optional packages listed in that file (such as `openai` and `google-api-python-client`) are not needed when running the unit tests but enable additional runtime integrations.

### Optional Packages and Features

| Package | Enables |
|---------|---------|
| `openai` | LLM backed agents and chat completions |
| `google-api-python-client` | Google Calendar and other Google service integrations |
| `requests` | HTTP-based memory service |

## 📐 Environment Variables

The system relies on a number of environment variables for API keys and service
endpoints. The most common ones are summarised below. Any of them can be set in
your shell before running the orchestrator or tests.

| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` | Used by agents that call OpenAI models |
| `CRM_API_URL` / `CRM_API_KEY` | Endpoint and key for your CRM integration |
| `SENDGRID_API_KEY` | Sending transactional email |
| `REDIS_URL` | Backend store for caching and message passing |
| `SLACK_WEBHOOK_URL` | Post notifications to Slack channels |
| `TEAMS_WEBHOOK_URL` | Microsoft Teams notifications |
| `PROMETHEUS_PUSHGATEWAY` | Metrics aggregation endpoint |
| `MLS_API_URL` / `MLS_API_KEY` | Real estate data feed |

See [`src/constants.py`](src/constants.py) for the full list.

## 🔬 Testing

The repository contains a suite of unit tests under `tests/`. Execute them with
`pytest`:

```bash
pytest -q
```

## 📊 RevOps & Tooling

Recent updates introduce a `RevOpsAgent` that summarizes CRM pipeline KPIs and
publishes revenue forecasts. The orchestrator wires this agent into a global
`EventBus` and triggers it on a monthly cron tick. Several internal utilities are
also included:

* `dev_assist.py` – generate boilerplate modules and matching tests.
* `debugger_agent.py` – listen for `*.Error` events and propose patches.
* `qa_agent.py` – run scripted conversations against `SupportAgent` and emit QA
  reports.

These helper scripts keep network calls behind feature flags so they remain
test-safe by default.

## 📚 Component Guide

For a deeper explanation of each module see
[docs/components.md](docs/components.md). It walks through the orchestrators,
memory services, agents, tools and the in-memory event bus with pointers on how
to extend them.

---

This project is released under the [MIT License](LICENSE).

