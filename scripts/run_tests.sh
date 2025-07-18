#!/usr/bin/env bash
# Run formatting checks, type checks, and the unit tests.
set -euo pipefail

black --check .
flake8
mypy .
pytest -q
