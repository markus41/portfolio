"""Command line interface for the Brookside orchestrator."""

from __future__ import annotations

import argparse
import asyncio
import json
import socket
import sys
from pathlib import Path
from typing import Dict, Iterable, Tuple

if __package__ in {None, ""}:  # pragma: no cover - script execution support
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    __package__ = "src"

from . import plugin_manager


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765

# Mapping of keywords to workflow JSON templates used by :func:`cmd_assist`.
# Each key can be a single word or phrase. The value is the path to the
# template under ``src/teams``. Matching is case-insensitive and performed on
# substrings.
TASK_WORKFLOW_MAP: Dict[Iterable[str], str] = {
    ("lead", "prospect", "sales"): "src/teams/sales_team_full.json",
    ("fulfillment", "ship", "order"): "src/teams/fulfillment_pipeline_team.json",
    ("inventory", "stock"): "src/teams/inventory_management_team.json",
    ("logistics", "operations"): "src/teams/operations_team.json",
    ("driver", "tracking", "shipment"): "src/teams/on_the_road_team.json",
    ("listing", "real estate"): "src/teams/real_estate_team.json",
    ("ecommerce", "shopping", "cart"): "src/teams/ecommerce_team.json",
}


# ---------------------------------------------------------------------------
# Utility networking helpers
# ---------------------------------------------------------------------------
async def _handle_client(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    orch: "SolutionOrchestrator",
) -> None:
    """Process a single client connection.

    Clients send one JSON line with a ``cmd`` field. Supported commands are
    ``send`` for dispatching an event and ``status`` to fetch the latest team
    statuses.  Results are written back as a single JSON line.
    """

    try:
        data = await reader.readline()
        if not data:
            return
        message = json.loads(data.decode())
    except json.JSONDecodeError:
        writer.write(b'{"error": "invalid_json"}\n')
        await writer.drain()
        writer.close()
        return

    cmd = message.get("cmd")
    if cmd == "send":
        team = message.get("team")
        event = message.get("event", {})
        try:
            result = await orch.handle_event(team, event)
            orch.report_status(team, "handled")
        except Exception as exc:  # pragma: no cover - defensive
            result = {"error": str(exc)}
        writer.write(json.dumps(result).encode() + b"\n")
    elif cmd == "status":
        writer.write(json.dumps(orch.status).encode() + b"\n")
    else:
        writer.write(b'{"error": "unknown_command"}\n')

    await writer.drain()
    writer.close()


def _parse_team_mapping(pairs: Tuple[str, ...]) -> Dict[str, str]:
    """Convert ``NAME=PATH`` pairs into a mapping."""
    mapping = {}
    for pair in pairs:
        if "=" not in pair:
            raise argparse.ArgumentTypeError(
                f"Invalid team spec '{pair}'. Use NAME=PATH"
            )
        name, path = pair.split("=", 1)
        mapping[name] = path
    return mapping


# ---------------------------------------------------------------------------
# Command implementations
# ---------------------------------------------------------------------------


def cmd_start(args: argparse.Namespace) -> None:
    """Start the orchestrator server and block forever."""
    from .solution_orchestrator import SolutionOrchestrator

    teams = _parse_team_mapping(tuple(args.teams))
    orch = SolutionOrchestrator(teams)

    async def _run() -> None:
        server = await asyncio.start_server(
            lambda r, w: _handle_client(r, w, orch), host=args.host, port=args.port
        )
        addr = server.sockets[0].getsockname()
        print(f"Listening on {addr[0]}:{addr[1]}", file=sys.stderr)
        async with server:
            try:
                await server.serve_forever()
            except asyncio.CancelledError:  # pragma: no cover - server shutdown
                pass

    try:
        asyncio.run(_run())
    except KeyboardInterrupt:  # pragma: no cover - manual stop
        pass


def _send_payload(host: str, port: int, payload: dict) -> dict:
    """Send ``payload`` to the orchestrator server and return the JSON reply."""
    data = json.dumps(payload).encode() + b"\n"
    with socket.create_connection((host, port)) as sock:
        sock.sendall(data)
        resp = b""
        while not resp.endswith(b"\n"):
            chunk = sock.recv(4096)
            if not chunk:
                break
            resp += chunk
    return json.loads(resp.decode())


def cmd_send(args: argparse.Namespace) -> None:
    """Dispatch an event to the running orchestrator."""
    if args.event:
        try:
            event = json.loads(args.event)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSON event: {exc}")
    else:
        try:
            event = json.load(sys.stdin)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSON from stdin: {exc}")

    if not args.team:
        raise SystemExit("--team is required")

    payload = {"cmd": "send", "team": args.team, "event": event}
    resp = _send_payload(args.host, args.port, payload)
    print(json.dumps(resp))


def cmd_status(args: argparse.Namespace) -> None:
    """Retrieve team statuses from the orchestrator."""
    payload = {"cmd": "status"}
    resp = _send_payload(args.host, args.port, payload)
    print(json.dumps(resp))


def cmd_list_agents(args: argparse.Namespace) -> None:
    """Print available agent identifiers."""
    print(json.dumps({"agents": plugin_manager.list_agents()}))


def cmd_list_plugins(args: argparse.Namespace) -> None:
    """Print available tool plugin identifiers."""
    print(json.dumps({"plugins": plugin_manager.list_plugins()}))


def cmd_show_plugin(args: argparse.Namespace) -> None:
    """Display details about a specific plugin."""
    info = plugin_manager.get_plugin_details(args.name)
    print(json.dumps(info))


def _match_workflow(task: str) -> str | None:
    """Return the workflow template matching ``task`` if any."""

    task_lower = task.lower()
    for keywords, template in TASK_WORKFLOW_MAP.items():
        if any(key in task_lower for key in keywords):
            return template
    return None


def cmd_assist(args: argparse.Namespace) -> None:
    """Map ``task`` to a workflow template and print the result as JSON."""

    template = _match_workflow(args.task)
    if template is None:
        print(json.dumps({"template": None, "error": "no_match"}))
    else:
        print(json.dumps({"template": template}))


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    """Construct and return the top-level argument parser."""

    parser = argparse.ArgumentParser(
        prog="brookside-cli",
        description="Control the Brookside SolutionOrchestrator",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    start_p = sub.add_parser("start", help="Run the orchestrator server")
    start_p.add_argument("teams", nargs="+", help="Team config as NAME=PATH pairs")
    start_p.add_argument("--host", default=DEFAULT_HOST, help="Bind address")
    start_p.add_argument("--port", type=int, default=DEFAULT_PORT, help="Bind port")
    start_p.set_defaults(func=cmd_start)

    send_p = sub.add_parser("send", help="Send an event to the orchestrator")
    send_p.add_argument("--team", required=False, help="Target team name")
    send_p.add_argument("--event", required=False, help="Event JSON string")
    send_p.add_argument("--host", default=DEFAULT_HOST, help="Server address")
    send_p.add_argument("--port", type=int, default=DEFAULT_PORT, help="Server port")
    send_p.set_defaults(func=cmd_send)

    assist_p = sub.add_parser(
        "assist",
        help="Suggest a workflow template for a natural language task",
    )
    assist_p.add_argument("task", help="Task description")
    assist_p.set_defaults(func=cmd_assist)

    status_p = sub.add_parser("status", help="Fetch latest team statuses")
    status_p.add_argument("--host", default=DEFAULT_HOST, help="Server address")
    status_p.add_argument("--port", type=int, default=DEFAULT_PORT, help="Server port")
    status_p.set_defaults(func=cmd_status)

    sub.add_parser("list-agents", help="List available agents").set_defaults(
        func=cmd_list_agents
    )
    sub.add_parser("list-plugins", help="List available tool plugins").set_defaults(
        func=cmd_list_plugins
    )
    show_p = sub.add_parser("show-plugin", help="Show details about a plugin")
    show_p.add_argument("name", help="Plugin entry point or module name")
    show_p.set_defaults(func=cmd_show_plugin)

    return parser


def main(argv: list[str] | None = None) -> None:
    """Entry point used by ``brookside-cli`` console script."""
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
