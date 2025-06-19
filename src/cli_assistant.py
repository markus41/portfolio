"""Command line assistant using the NLP parameter parser."""

from __future__ import annotations

import argparse
import json
import sys

from .utils.nlp_params import parse_parameters


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
