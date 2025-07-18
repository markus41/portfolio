# Codex Instructions

This repository is a Python package with a comprehensive test suite.
To work effectively:

1. **Setup** – Use `scripts/setup.sh` to install dependencies and configure
   pre-commit hooks.  The script installs packages from `requirements.txt`
   and `requirements-dev.txt` and then installs pre-commit if available.

   ```bash
   ./scripts/setup.sh
   ```

2. **Testing** – Run `scripts/run_tests.sh` before committing changes. This
   performs formatting, linting and runs the unit tests.

   ```bash
   ./scripts/run_tests.sh
   ```

3. **Style** – Follow PEP8 and type-hint new code. The repository uses
   `black`, `flake8` and `mypy` via pre-commit hooks to enforce style.

4. **Commits** – Use Conventional Commits messages in the imperative mood
   (e.g. `feat: add CRM connector`).

These guidelines ensure Codex mirrors the CI workflow for accurate results.
