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

from .utils.logging_config import setup_logging
from .utils.team_mapping import parse_team_mapping


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


# ---------------------------------------------------------------------------
# Command implementations
# ---------------------------------------------------------------------------


def cmd_start(args: argparse.Namespace) -> None:
    """Start the orchestrator server and block forever."""
    from .solution_orchestrator import SolutionOrchestrator

    try:
        teams = parse_team_mapping(args.teams)
    except ValueError as exc:
        raise SystemExit(str(exc))
    orch = SolutionOrchestrator(teams)

    async def _run() -> None:
        async with orch:
            server = await asyncio.start_server(
                lambda r, w: _handle_client(r, w, orch),
                host=args.host,
                port=args.port,
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


def _send_payload(host: str, port: int, payload: dict, timeout: float = 5.0) -> dict:
    """Send ``payload`` to the orchestrator and return the JSON reply.

    Parameters
    ----------
    host:
        Server host name or IP address.
    port:
        Server port number.
    payload:
        JSON-serialisable object describing the command to execute.
    timeout:
        Optional timeout in seconds for both connecting and reading.  Defaults
        to ``5`` seconds.

    Returns
    -------
    dict
        Parsed JSON response from the server.

    Raises
    ------
    SystemExit
        If the connection fails, times out or the response cannot be decoded
        as JSON.  The exit message is a user friendly error description.
    """

    data = json.dumps(payload).encode() + b"\n"

    try:
        # ``create_connection`` also accepts a timeout which covers DNS lookup
        # and the initial TCP handshake.  ``sock.settimeout`` below applies to
        # subsequent send/recv operations.
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            try:
                sock.sendall(data)
                resp = b""
                while not resp.endswith(b"\n"):
                    chunk = sock.recv(4096)
                    if not chunk:
                        break
                    resp += chunk
            except socket.timeout as exc:
                raise SystemExit(
                    f"Timed out waiting for server response after {timeout}s"
                ) from exc
    except ConnectionRefusedError as exc:
        raise SystemExit(f"Failed to connect to {host}:{port}") from exc
    except socket.timeout as exc:
        raise SystemExit(
            f"Connection to {host}:{port} timed out after {timeout}s"
        ) from exc
    except OSError as exc:
        # Other networking errors (e.g. unreachable network)
        raise SystemExit(str(exc)) from exc

    try:
        return json.loads(resp.decode())
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON response: {exc}") from exc


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
    resp = _send_payload(args.host, args.port, payload, timeout=args.timeout)
    print(json.dumps(resp))


def cmd_status(args: argparse.Namespace) -> None:
    """Retrieve team statuses from the orchestrator."""
    payload = {"cmd": "status"}
    resp = _send_payload(args.host, args.port, payload, timeout=args.timeout)
    print(json.dumps(resp))


def cmd_validate_team(args: argparse.Namespace) -> None:
    """Validate a team JSON file against ``team_schema.json``.

    The command prints a JSON object describing the validation result. On
    success the output is ``{"valid": true}``. When validation fails the
    ``error`` field contains the reason extracted from the underlying
    :class:`jsonschema.ValidationError` or raised exception.
    """

    from .team_orchestrator import validate_team_config

    try:
        data = json.loads(Path(args.path).read_text())
        validate_team_config(data)
    except Exception as exc:  # jsonschema.ValidationError or I/O errors
        # ``exc`` may include contextual information such as the failing JSON
        # pointer.  The ``message`` attribute is shorter and more suitable for
        # end users when available.
        error_msg = getattr(exc, "message", str(exc))
        print(json.dumps({"valid": False, "error": error_msg}))
    else:
        print(json.dumps({"valid": True}))


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


def cmd_run_integration(args: argparse.Namespace) -> None:
    """Trigger an integration pipeline on the orchestrator."""

    if not args.team:
        raise SystemExit("--team is required")
    event = {"type": "integration_request", "payload": {"name": args.name}}
    payload = {"cmd": "send", "team": args.team, "event": event}
    resp = _send_payload(args.host, args.port, payload, timeout=args.timeout)
    print(json.dumps(resp))


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
    send_p.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Connection timeout in seconds (default: 5)",
    )
    send_p.set_defaults(func=cmd_send)

    run_int = sub.add_parser(
        "run-integration", help="Execute a configured integration pipeline"
    )
    run_int.add_argument("name", help="Integration name")
    run_int.add_argument("--team", required=False, help="Target team name")
    run_int.add_argument("--host", default=DEFAULT_HOST, help="Server address")
    run_int.add_argument("--port", type=int, default=DEFAULT_PORT, help="Server port")
    run_int.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Connection timeout in seconds (default: 5)",
    )
    run_int.set_defaults(func=cmd_run_integration)

    assist_p = sub.add_parser(
        "assist",
        help="Suggest a workflow template for a natural language task",
    )
    assist_p.add_argument("task", help="Task description")
    assist_p.set_defaults(func=cmd_assist)

    status_p = sub.add_parser("status", help="Fetch latest team statuses")
    status_p.add_argument("--host", default=DEFAULT_HOST, help="Server address")
    status_p.add_argument("--port", type=int, default=DEFAULT_PORT, help="Server port")
    status_p.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Connection timeout in seconds (default: 5)",
    )
    status_p.set_defaults(func=cmd_status)

    validate_p = sub.add_parser(
        "validate-team", help="Validate a team JSON configuration file"
    )
    validate_p.add_argument("path", help="Path to team JSON file")
    validate_p.set_defaults(func=cmd_validate_team)

    return parser


def main(argv: list[str] | None = None) -> None:
    """Entry point used by ``brookside-cli`` console script."""
    setup_logging()
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
