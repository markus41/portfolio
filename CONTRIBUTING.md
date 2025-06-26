# Contributing Guide

Thank you for considering a contribution to this project! This document outlines how to set up a development environment and the conventions we follow for code style and commit messages.

## Development Environment

1. **Install Dependencies**

   Install the runtime requirements alongside the development tools from
   `requirements-dev.txt`. These include the test runner, `pre-commit`
   hooks and documentation utilities:

   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   # If the project defines extras for development use:
   pip install -e '.[dev]'
   ```

2. **Set Up Pre-commit Hooks**
   
   ```bash
   pre-commit install
   ```
   This installs git hooks that automatically format code with **black**, lint with **flake8**, and run the unit tests via **pytest** before each commit.

3. **Run the Test Suite**
   
   ```bash
   pytest -q
   ```
   Ensure all tests pass before opening a pull request.

## Code Style

We follow **PEP8** conventions and require type hints for new code. The `pre-commit` hooks run **black** and **flake8** to enforce formatting and style automatically.

## Commit Messages

Use the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) format in the *imperative mood*.
Example messages:

- `feat: add new CRM connector`
- `fix: handle missing API key`
- `docs: update README`

This style ensures a consistent and readable project history.

All commits are automatically validated when you run `pre-commit`. The commit
message hook will reject commits that do not follow the Conventional Commits
style.

---

For further details about the project architecture and workflow, see the [README](README.md).
