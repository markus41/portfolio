"""Command line assistant using the NLP parameter parser."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:  # pragma: no cover - script execution support
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    __package__ = "src"

from .utils.nlp_params import parse_parameters
from .utils.logging_config import setup_logging


def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser for the assistant."""

    parser = argparse.ArgumentParser(
        prog="brookside-assistant",
        description="Extract campaign parameters from free text",
    )
    parser.add_argument(
        "text", nargs="?", help="Text to parse; read from stdin if omitted"
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    """Entry point for the CLI assistant."""

    setup_logging()
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.text:
        text = args.text
    else:
        text = sys.stdin.read()

    params = parse_parameters(text)
    print(json.dumps(params))


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
