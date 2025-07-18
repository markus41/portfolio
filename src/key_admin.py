import argparse
import json
from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    __package__ = "src"

from . import db
from .config import settings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Manage API keys")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_create = sub.add_parser("create", help="create a new API key")
    p_create.add_argument("tenant", help="tenant name")
    p_create.add_argument(
        "--scopes",
        default="read,write",
        help="comma separated list of scopes",
    )

    p_rotate = sub.add_parser("rotate", help="rotate an existing key")
    p_rotate.add_argument("key", help="key to rotate")

    args = parser.parse_args(argv)
    settings.DB_CONNECTION_STRING = settings.DB_CONNECTION_STRING  # ensure loaded
    db.init_db()

    if args.cmd == "create":
        scopes = [s.strip() for s in args.scopes.split(",") if s.strip()]
        key = db.create_api_key(args.tenant, scopes)
        print(json.dumps({"key": key}))
        return 0

    if args.cmd == "rotate":
        try:
            new_key = db.rotate_api_key(args.key)
        except KeyError as exc:
            print(json.dumps({"error": str(exc)}))
            return 1
        print(json.dumps({"key": new_key}))
        return 0
    return 1


if __name__ == "__main__":  # pragma: no cover - manual use
    raise SystemExit(main())
