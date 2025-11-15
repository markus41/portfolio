#!/usr/bin/env python3
"""
Script to create GitHub issues for NABIP features programmatically.

This script reads the configuration from nabip_issues_config.json and creates
feature request issues and their sub-issues in the GitHub repository.

Usage:
    python scripts/create_nabip_issues.py --dry-run  # Preview without creating
    python scripts/create_nabip_issues.py             # Create issues

Requirements:
    - GitHub CLI (gh) installed and authenticated
    - Repository cloned and in current directory
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List


def load_config(config_path: str = "scripts/nabip_issues_config.json") -> Dict:
    """Load the issues configuration from JSON file."""
    with open(config_path, "r") as f:
        return json.load(f)


def format_issue_body(feature: Dict) -> str:
    """Format the feature request issue body."""
    body = f"""## {feature['description']}

### Feature Category
{feature['category']}

### Problem Statement
{feature['problem_statement']}

### Proposed Solution
{feature['proposed_solution']}

### Alternatives Considered
"""
    for alt in feature["alternatives"]:
        body += f"- {alt}\n"

    body += f"""
### Expected Impact
{feature['expected_impact']}

### Priority
{feature['priority']}

### Technical Considerations
{feature['technical_considerations']}

### Sub-Issues
This feature is broken down into the following sub-issues:
"""

    for sub_issue in feature["sub_issues"]:
        body += f"- #{sub_issue['number']}: {sub_issue['title']}\n"

    return body


def format_sub_issue_body(sub_issue: Dict, parent_number: int) -> str:
    """Format the sub-issue body."""
    body = f"""## {sub_issue['title']}

**Section:** {sub_issue['section']}

**Parent Feature:** #{parent_number}

### Description
{sub_issue['description']}

### Recommended Custom Agents
"""

    for agent in sub_issue["agents"]:
        body += f"- `{agent}`\n"

    body += "\n### Labels\n"

    for label in sub_issue["labels"]:
        body += f"- `{label}`\n"

    return body


def create_github_issue(
    title: str, body: str, labels: List[str], dry_run: bool = False
) -> int:
    """
    Create a GitHub issue using the gh CLI.

    Returns the issue number if successful, 0 otherwise.
    """
    if dry_run:
        sep = "=" * 80
        print(f"\n{sep}")
        print(f"TITLE: {title}")
        print(f"LABELS: {', '.join(labels)}")
        print(sep)
        print(body)
        print(f"{sep}\n")
        return 0

    # Create temporary file for issue body
    temp_file = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".md",
        delete=False,
    )
    with temp_file as f:
        f.write(body)
        body_file = f.name

    try:
        # Build gh command
        cmd = [
            "gh",
            "issue",
            "create",
            "--title",
            title,
            "--body-file",
            body_file,
        ]

        # Add labels
        for label in labels:
            cmd.extend(["--label", label])

        # Execute command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )

        # Extract issue number from output
        output = result.stdout.strip()
        issue_url = output.split("\n")[-1]
        issue_number = int(issue_url.split("/")[-1])

        print(f"✓ Created issue #{issue_number}: {title}")
        return issue_number

    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create issue: {title}")
        print(f"  Error: {e.stderr}")
        return 0
    finally:
        # Clean up temp file
        Path(body_file).unlink(missing_ok=True)


def create_feature_issues(config: Dict, dry_run: bool = False) -> None:
    """
    Create all feature request issues and sub-issues from config.
    """
    feature_requests = config["feature_requests"]

    sep = "=" * 80
    print(f"\n{sep}")
    msg = f"Creating {len(feature_requests)} feature requests"
    print(f"{msg} with sub-issues")
    print(f"{sep}\n")

    for feature in feature_requests:
        feature_number = feature["number"]
        feature_title = f"[Feature #{feature_number}]: {feature['title']}"
        feature_body = format_issue_body(feature)
        feature_labels = feature["labels"]

        # Create feature request issue
        created_number = create_github_issue(
            title=feature_title,
            body=feature_body,
            labels=feature_labels,
            dry_run=dry_run,
        )

        if not dry_run and created_number == 0:
            print(f"Skipping sub-issues for feature #{feature_number}")
            continue

        # Create sub-issues
        num_sub = len(feature["sub_issues"])
        msg = f"\nCreating {num_sub} sub-issues for feature "
        print(f"{msg}#{feature_number}...")

        for sub_issue in feature["sub_issues"]:
            num = sub_issue["number"]
            title_text = sub_issue["title"]
            sub_title = f"[Sub-Issue #{num}]: {title_text}"
            sub_body = format_sub_issue_body(sub_issue, feature_number)
            sub_labels = sub_issue["labels"]

            create_github_issue(
                title=sub_title,
                body=sub_body,
                labels=sub_labels,
                dry_run=dry_run,
            )

        sep = "=" * 80
        print(f"\n{sep}\n")


def check_gh_cli() -> bool:
    """Check if GitHub CLI is installed and authenticated."""
    try:
        # Check if gh is installed
        result = subprocess.run(
            ["gh", "--version"], capture_output=True, text=True, check=True
        )
        print(f"✓ GitHub CLI found: {result.stdout.split()[2]}")

        # Check if authenticated
        result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True,
            text=True,
            check=True,
        )
        print("✓ GitHub CLI authenticated")
        return True

    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ GitHub CLI not found or not authenticated")
        print("\nPlease install and authenticate GitHub CLI:")
        print("  1. Install: https://cli.github.com/")
        print("  2. Authenticate: gh auth login")
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Create NABIP feature request issues on GitHub"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview issues without creating them",
    )
    parser.add_argument(
        "--config",
        default="scripts/nabip_issues_config.json",
        help="Path to configuration file",
    )

    args = parser.parse_args()

    # Check for GitHub CLI
    if not args.dry_run and not check_gh_cli():
        sys.exit(1)

    # Load configuration
    try:
        config = load_config(args.config)
    except FileNotFoundError:
        print(f"✗ Configuration file not found: {args.config}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON in configuration file: {e}")
        sys.exit(1)

    # Create issues
    if args.dry_run:
        print("\n🔍 DRY RUN MODE - No issues will be created\n")

    create_feature_issues(config, dry_run=args.dry_run)

    if args.dry_run:
        msg = "\n✓ Dry run completed. Run without --dry-run to create issues."
        print(msg)
    else:
        print("\n✓ All issues created successfully!")


if __name__ == "__main__":
    main()
