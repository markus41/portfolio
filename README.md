<!-- README.md -->

# 🚀 Brookside BI – Autonomous Sales & Marketing Agents

Welcome to the Brookside BI Agentic System! This repo contains a modular, turn-based framework of specialized AI “expert” agents that power everything from lead capture to contract delivery, all orchestrated under a central Orchestrator agent. Whether you’re adding a new campaign agent or tweaking your CRM integration, you’ll find a clean separation of concerns that makes extending and testing your workflow a breeze.

For a deeper explanation of the architecture—including the event bus, memory service and how AutoGen teams are loaded and how teams start running—see [docs/architecture.md](docs/architecture.md).

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

## 📦 Installation

Install the Python dependencies with pip using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

The optional packages listed in that file (such as `openai` and `google-api-python-client`) are not needed when running the unit tests but enable additional runtime integrations.

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
