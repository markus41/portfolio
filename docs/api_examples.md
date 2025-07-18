# API Examples

This page demonstrates common interactions with the `SolutionOrchestrator` HTTP interface and its Python API. Copy the commands below to quickly integrate the orchestrator into your own tooling or scripts.

## Running the API server

Launch the FastAPI server that exposes your teams:

```bash
python -m src.api --sales=src/teams/sales_team_full.json
```

The server listens on port `8000` by default. Set the `PORT` environment variable to change it.

## Sending an event via `curl`

```bash
curl -X POST \
     -H 'Content-Type: application/json' \
     -d '{"type": "lead_capture", "payload": {"email": "alice@example.com"}}' \
     http://localhost:8000/teams/sales/event
```

The response contains the orchestrator result as JSON.

## Streaming team status

```bash
curl http://localhost:8000/teams/sales/stream
```

This command prints a Server-Sent Events stream of status updates and activity messages.

## Python usage

```python
from src.solution_orchestrator import SolutionOrchestrator

async def main() -> None:
    async with SolutionOrchestrator({"sales": "src/teams/sales_team_full.json"}) as orch:
        result = await orch.handle_event(
            "sales",
            {"type": "lead_capture", "payload": {"email": "alice@example.com"}},
        )
        print(result)
```

Executing `main()` dispatches an event to the `sales` team and prints the structured result.

