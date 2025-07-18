# Command Line Reference

`brookside-cli` provides a thin wrapper around the `SolutionOrchestrator` so you can start teams, send events and perform maintenance tasks from your terminal.

## start

Run the orchestrator as a background server. You must supply one or more `NAME=PATH` pairs that map team names to JSON or YAML configuration files.

```bash
brookside-cli start sales=src/teams/sales_team_full.json
```

Arguments:

- `--host` – Bind address. Defaults to `127.0.0.1`.
- `--port` – Port to listen on. Defaults to `8765`.

The command prints the address on `stderr` and blocks until interrupted.

## send

Dispatch an event to the running orchestrator. Provide the target team name with `--team` and the event payload as JSON via `--event` or standard input.
Use `--timeout` to adjust the network timeout (default 5 seconds).

```bash
brookside-cli send --team sales --event '{"type": "lead_capture", "payload": {"email": "alice@example.com"}}'
```

Use `--host` and `--port` if the server is running on another address.
The `--timeout` flag is also honoured by `status` and `run-integration`.

## status

Retrieve the latest status of all teams from the orchestrator.

```bash
brookside-cli status
```

The command returns a JSON object mapping each team to its last reported status.

## validate-team

Validate a team configuration file against `team_schema.json`.

```bash
brookside-cli validate-team src/teams/sales_team_full.json
```

The output indicates whether the file is valid and prints an error message if not.

## assist

Suggest a workflow template based on a natural language task description.

```bash
brookside-cli assist "handle new inventory"
# {"template": "src/teams/inventory_management_team.json"}
```

This utility performs simple keyword matching to pick an appropriate template.

## run-integration

Execute a configured integration pipeline via the running orchestrator.

```bash
brookside-cli run-integration CRM_to_ERP_Contacts --team sales
```

The command sends an `integration_request` task to the orchestrator and prints
the JSON result.

## Troubleshooting

- **Connection refused** – If the server is not running or the wrong address is used, commands print `Failed to connect to HOST:PORT`.
- **Timeouts** – Operations abort with `Timed out waiting for server response` when the orchestrator does not reply within the configured `--timeout` value.
- **Invalid JSON event** – If the payload passed to `--event` cannot be parsed, the command exits with `Invalid JSON event`.
- **Invalid response** – When the server sends malformed JSON, the CLI reports `Invalid JSON response`.
- **Schema errors** – `validate-team` prints `{"valid": false}` when the file does not match the schema. Inspect the accompanying `error` field for details.

