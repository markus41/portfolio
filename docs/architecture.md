# Architecture Overview

This document explains how the Brookside BI agent system fits together and how AutoGen driven teams are constructed.

```
                 +-----------------------+
                 |  SolutionOrchestrator |
                 +-----------+-----------+
                             |
          +------------------+------------------+
          |                                     |
  +-------v--------+                     +-------v--------+
  | TeamOrchestrator|                     | TeamOrchestrator|
  |     (sales)     |                     |      (ops)     |
  +-------+--------+                     +-------+--------+
          |                                     |
        EventBus                             EventBus
          |                                     |
        Agents                               Agents
          |
    MemoryService
```

## EventBus

`EventBus` is a minimal in-memory pub/sub utility defined in `agentic_core.EventBus`.  Agents subscribe to topics and publish events synchronously.  For asynchronous flows an `AsyncEventBus` is also available which awaits subscriber tasks using `asyncio.create_task`.

```
from agentic_core import EventBus
bus = EventBus()
bus.subscribe("greet", lambda p: print(p))
bus.publish("greet", {"msg": "hello"})
```

Async variant:

```
from agentic_core import AsyncEventBus
bus = AsyncEventBus()

async def handler(p):
    print(p)

bus.subscribe("greet", handler)
await bus.publish("greet", {"msg": "hi"})
```

## MemoryService

`MemoryService` provides persistence.  Two implementations exist:

* `src.memory_service.MemoryService` – REST client used by the main `Orchestrator`.
* `agentic_core.MemoryService` – simple in-memory store used in tests and demos.

Events handled by the orchestrators are stored via this service so that later agents can query previous context.
For a deeper dive into the REST client and ways to swap in other backends see
[memory_service.md](memory_service.md).

Example HTTP calls when the REST variant is used:

```http
POST /store
{
  "key": "lead_capture:42",
  "data": {"email": "user@example.com"}
}

GET /fetch?key=lead_capture:42&top_k=5
[
  {"key": "lead_capture:42", "data": {"email": "user@example.com"}}
]
```

## Orchestrator Flow

### Orchestrator

`src.orchestrator.Orchestrator` wires a handful of Python agents together.  `handle_event()` (an async method) stores incoming payloads via `MemoryService` and then awaits the agent associated with the event `type`.
The mapping of event types to agent classes can be supplied via a small JSON file. When the orchestrator is constructed with ``config_path`` it loads this file and imports the listed modules dynamically. An example can be found in ``src/orchestrator_config.json``:

```json
{
  "lead_capture": "src.agents.sales.lead_capture_agent.LeadCaptureAgent",
  "chatbot": "src.agents.sales.chatbot_agent.ChatbotAgent"
}
```

If ``config_path`` is not provided, a built-in default mapping identical to the example above is used.

### TeamOrchestrator

`src.team_orchestrator.TeamOrchestrator` loads a single AutoGen team from JSON or YAML.  When instantiated it:

1. Reads the team configuration file.
2. For each participant entry, dynamically imports the agent class using
   `importlib.import_module(f"src.agents.{name}")`.
3. Builds the AutoGen agents (e.g. `src.agents.roles.AssistantAgent`) and registers them on an internal `EventBus`.

All AutoGen import statements therefore execute when the team orchestrator is constructed.  The modules remain loaded for the lifetime of the orchestrator.

### Team Initialization Sequence

`SolutionOrchestrator` creates each team orchestrator when it is instantiated.
For every entry in the `team_configs` mapping the following steps occur:

1. A :class:`TeamOrchestrator` is constructed which loads the team file.
2. AutoGen reads the `provider` settings for every participant and instantiates the matching agent classes and model clients (for example `OpenAIChatCompletionClient`).
3. Each agent registers callback functions on the team's :class:`EventBus` so messages can be routed internally.

At this point all AutoGen agents are live and waiting for events. Teams remain active until `SolutionOrchestrator` is destroyed or the team is removed from its registry.


### SolutionOrchestrator

`src.solution_orchestrator.SolutionOrchestrator` manages multiple `TeamOrchestrator` instances.  It routes events to a named team via the async `handle_event(team, event)` method and records the results. For higher throughput, events may be queued with `enqueue_event()` which are processed by a pool of worker tasks limited by `max_workers`.

## AutoGen Agents and Providers

Team configuration files under `src/teams/` (either JSON or YAML) describe `RoundRobinGroupChat` configurations.  Each agent entry specifies a `provider` such as `src.agents.roles.AssistantAgent` or `autogen.models.openai.OpenAIChatCompletionClient`.  When a team is loaded, these providers are instantiated and stitched together by AutoGen.  The full structure of a team file is defined in [`team_schema.json`](team_schema.json) and can be checked using `brookside-cli validate-team`.

Each team file may optionally include a `responsibilities` array listing the
agent names allowed to operate within that team.  When a team is loaded the
`TeamOrchestrator` validates that every participant's `config.name` appears in
this list and raises an error otherwise.

OpenAI powered components (via `OpenAIChatCompletionClient`) are created using API keys provided by `src.config.settings`.  The settings object reads values from environment variables and the relevant `.env` file.  Whenever an AutoGen agent needs a model response, the provider invokes the OpenAI API to generate the next message.

### AutoGen Invocation

When `TeamOrchestrator.handle_event` receives an event it forwards the payload to the corresponding AutoGen agent. The agent's `model_client` (such as `OpenAIChatCompletionClient`) sends the message to the LLM and returns the response. AutoGen then orchestrates the conversation flow defined in the team configuration, cycling through the participants until a termination condition is met.

## Execution Sequence

1. External code awaits `SolutionOrchestrator.handle_event()` with a team name and event.
2. The `SolutionOrchestrator` forwards the event to the appropriate `TeamOrchestrator`.
3. The team orchestrator dispatches the event to the matching agent using its `EventBus`.
4. Agents may call tools, publish additional events or interact with AutoGen models.
5. Providers (e.g. OpenAI clients) are called by AutoGen whenever a message requires LLM output.
6. The original orchestrator persists the event through `MemoryService` for auditing.

### Graph Workflow Engine

`GraphWorkflowEngine` executes workflows described as nodes and edges.  Each node
may specify a `team` and `event` that are dispatched through
`SolutionOrchestrator`.  Calls can be synchronous using `step()` / `run()` or
fully asynchronous via `async_step()` / `async_run()` which await the
orchestrator's `handle_event` method.

## Building New Agents and Teams

1. Implement a new agent class under `src/agents/` deriving from `BaseAgent` and providing a `run()` method.
2. Add any helper tools under `src/tools/` and register them with `@Tool` if using `agentic_core` utilities.
3. Create a new team file (JSON or YAML) mirroring those in `src/teams/`.  The `participants` section should reference your agent module names so that `TeamOrchestrator` can import them. Optionally include a `responsibilities` array listing the allowed agent names.
4. Register the team with `SolutionOrchestrator` by mapping a name to the file path.

With these pieces in place, events sent to the solution orchestrator will automatically activate your new team alongside the existing ones.

## Advanced Customization

Beyond the standard setup you can extend almost every component:

* **Swap MemoryService** – implement the simple `store()` and `fetch()` REST
  endpoints in your favorite database or caching layer and point
  `src.memory_service.MemoryService` to the new base URL.
* **Pluggable EventBus** – the in-memory bus works for single-process demos. In
  production you might adapt it to wrap Redis pub/sub or Kafka topics. As long
  as the API exposes `subscribe(topic, handler)` and `publish(topic, data)` the
  orchestrators will function the same.
* **Custom Providers** – AutoGen agents rely on model providers for LLM access.
  You can create new providers for different AI services by implementing the
  same interface that `OpenAIChatCompletionClient` exposes and referencing that
  class in your team file.

These extension points allow the Brookside framework to scale from unit tests to
real-world deployments with minimal changes.
