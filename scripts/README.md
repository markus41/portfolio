# Scripts Directory

This directory contains utility scripts for managing the repository.

## Available Scripts

### setup.sh
Installs dependencies and configures pre-commit hooks. Run this first when setting up a development environment.

```bash
./scripts/setup.sh
```

### run_tests.sh
Performs formatting, linting, and runs the unit tests. Always run this before committing changes.

```bash
./scripts/run_tests.sh
```

### generate_issues.py
Generates GitHub issues programmatically for large feature requests with multiple sub-issues.

#### Usage

**Preview issues without creating them:**
```bash
python scripts/generate_issues.py --dry-run
```

**Create issues on GitHub (requires GitHub CLI):**
```bash
python scripts/generate_issues.py --create
```

**Export issue data to JSON:**
```bash
python scripts/generate_issues.py --export-json
```

**Export issue overview to Markdown:**
```bash
python scripts/generate_issues.py --export-md
```

#### Features

- Manages 3 major feature requests with 93 sub-issues
- Assigns appropriate GitHub agent types based on issue category
- Creates hierarchical issue relationships
- Supports labels, estimates, and agent assignments
- Can export to JSON and Markdown for documentation

#### Agent Types

The script assigns issues to specialized agents:

- **frontend**: Frontend Development Agent
- **backend**: Backend Development Agent
- **fullstack**: Full-Stack Development Agent
- **database**: Database Agent
- **devops**: DevOps/Infrastructure Agent
- **security**: Security Agent
- **ux**: UX/UI Design Agent
- **ml**: Machine Learning Agent
- **documentation**: Documentation Agent
- **testing**: Testing/QA Agent

#### Prerequisites for GitHub Creation

To use the `--create` flag, you need:

1. **GitHub CLI installed**: https://cli.github.com/
2. **Authentication**: Run `gh auth login` first
3. **Repository access**: You must have write access to the repository

#### Feature Requests Managed

1. **Feature Request #4**: Document Distribution & Management System (13 sub-issues)
2. **Feature Request #5**: Dashboard & Analytics Platform (37 sub-issues)
3. **Feature Request #6**: Navigation & User Experience Overhaul (43 sub-issues)

#### Output Files

- `ISSUES_OVERVIEW.md`: Comprehensive markdown documentation of all issues
- `issues_data.json`: Structured JSON data for programmatic access

## Adding New Scripts

When adding new scripts to this directory:

1. Make them executable: `chmod +x scripts/your_script.sh`
2. Add proper shebang line (e.g., `#!/usr/bin/env bash` or `#!/usr/bin/env python3`)
3. Include usage documentation in this README
4. Follow the existing naming conventions
5. Include error handling and validation

## Script Dependencies

Scripts may have dependencies on:

- Python 3.9+
- GitHub CLI (`gh`)
- Standard Unix utilities (`bash`, `git`, etc.)
- Python packages from `requirements.txt` and `requirements-dev.txt`

## Troubleshooting

### GitHub CLI Issues

If `gh` commands fail:
```bash
# Check if gh is installed
gh --version

# Login to GitHub
gh auth login

# Check authentication status
gh auth status
```

### Permission Issues

If you get permission denied errors:
```bash
# Make script executable
chmod +x scripts/script_name.sh
```

### Python Import Errors

Make sure you've installed dependencies:
```bash
./scripts/setup.sh
# or
pip install -r requirements.txt -r requirements-dev.txt
```
