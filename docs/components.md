# Component Guide

This guide describes the main modules that make up the Brookside BI agent system. Use it alongside `architecture.md` to understand how everything fits together.

## Orchestrators

Three orchestrators coordinate agent behavior:

* **`Orchestrator`** – the entry point for single-team workflows. Events are stored via the `MemoryService` and then routed to a specific agent based on the event `type`.
* **`TeamOrchestrator`** – loads an AutoGen team from JSON. Each participant becomes an AutoGen agent bound to a shared `EventBus`. This orchestrator exposes `handle_event()` to push messages into the chat loop.
* **`SolutionOrchestrator`** – manages multiple `TeamOrchestrator` instances. It accepts a mapping of team names to JSON paths and forwards events accordingly.

## Memory Services

The `MemoryService` abstraction allows the orchestrators to persist conversation history. Two variants are available:

1. `agentic_core.MemoryService` – an in-memory store used for local tests.
2. `src.memory_service.MemoryService` – a thin REST client calling `/store` and `/fetch` endpoints as shown in `architecture.md`.

The implementation can be swapped at runtime so your agents can persist data to any backend.

## Agents

Agents live under `src/agents/` and are simple Python classes with a `run()` method. Many derive from a small `BaseAgent` helper that handles event subscription. Each agent can optionally declare a list of `skills` describing its capabilities. Examples include:

* `ChatbotAgent` – responds to user queries.
* `LeadCaptureAgent` – parses forms and enters prospects into the CRM.
* `ProcurementAgent` – manages supplier quotes and approvals.

When AutoGen is used, these classes provide the business logic invoked by the AutoGen participants defined in your team JSON.
[See the agent catalog](agents_overview.md) for a complete list of available agents and tools.

## Tools

Reusable utilities live under `src/tools/`. They encapsulate third-party integrations or shared logic, for example:

* `crm_tool.py` – generic CRM operations such as creating contacts or updating deals.
* `real_estate_tools.py` – fetch MLS data and post listings.
* `ecommerce_tool.py` – manage product catalogs and shopping carts.

Tool classes can be registered as `FunctionTool` entries in a team JSON file so agents can call them during a conversation.

## EventBus

An in-memory publish/subscribe mechanism. Agents and orchestrators subscribe to topics and publish events to coordinate asynchronous workflows. The bus keeps all components loosely coupled.

## Adding New Functionality

1. Create an agent under `src/agents/` implementing the desired behavior.
2. Optionally build helper functions under `src/tools/`.
3. Add a team JSON file referencing your agent and tools.
4. Register the team with `SolutionOrchestrator` and send it events.

These steps let you compose new business flows without touching the core orchestrator logic.

### Registering Custom Agents via Plugins

Agents can also be distributed as standalone packages and discovered at runtime
through Python entry points. Register your agent class under the
``brookside.agents`` group in ``setup.cfg``:

```ini
[options.entry_points]
brookside.agents =
    lead_capture = src.agents.sales.lead_capture_agent:LeadCaptureAgent
```

With the entry point installed, :func:`src.utils.plugin_loader.load_agent` will
resolve ``lead_capture`` to ``LeadCaptureAgent`` without requiring explicit
imports. The ``TeamOrchestrator`` automatically uses this loader when
initialising agents from a team JSON file.

### Custom Tool Plugins

Utility classes can be plugged in using the same mechanism. Implement a
``BaseToolPlugin`` subclass under ``src/plugins`` or distribute it via an entry
point in the ``brookside.plugins`` group. At runtime
``src.utils.plugin_loader.load_plugin`` resolves the class so it can be
instantiated by agents or orchestrators. For example, to expose the
``EmailPlugin`` via entry points add the following to ``setup.cfg``:

```ini
[options.entry_points]
brookside.plugins =
    email = src.plugins.email_plugin:EmailPlugin
```

Once installed, ``load_plugin('email')`` will return ``EmailPlugin``. Plugins
placed directly in ``src/plugins/`` do not require registration and are
automatically importable by name.

You can also resolve components manually using the helper in
``src.utils.plugin_loader``:

```python
from src.utils.plugin_loader import load_agent, load_plugin

agent_cls = load_agent("lead_capture")
plugin_cls = load_plugin("email")
```

