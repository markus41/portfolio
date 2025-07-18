#!/usr/bin/env bash
# Setup script for the Brookside BI project
# Installs runtime and development dependencies to run tests and linters.
set -euo pipefail

# Upgrade pip and install requirements
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks if available
if command -v pre-commit >/dev/null 2>&1; then
    pre-commit install
fi

# Output versions for debugging
python -V
pip list
