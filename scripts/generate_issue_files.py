#!/usr/bin/env python3
"""
Script to generate GitHub issue markdown files from feature request
documentation.

This script reads the feature request documentation and creates individual
markdown files for each sub-issue that can be used to create GitHub issues.

Usage:
    python scripts/generate_issue_files.py

Output:
    Creates markdown files in /tmp/github_issues/ that can be used to
    manually create GitHub issues via the web interface.
"""

import re
from pathlib import Path


# Feature request metadata
FEATURE_REQUESTS = {
    "FR-015": {
        "title": "Automation & Workflow Engine",
        "filename": "automation-workflow-engine",
        "issues": range(343, 350),
        "labels": ["enhancement", "automation", "workflow"],
    },
    "FR-016": {
        "title": "Integration Hub & API Platform",
        "filename": "integration-hub-api-platform",
        "issues": range(350, 358),
        "labels": ["enhancement", "integration", "api"],
    },
    "FR-017": {
        "title": "Mobile-First Experience & PWA",
        "filename": "mobile-first-pwa",
        "issues": range(358, 370),
        "labels": ["enhancement", "mobile", "pwa"],
    },
    "FR-018": {
        "title": "User Experience & Design System",
        "filename": "ux-design-system",
        "issues": range(370, 415),
        "labels": ["enhancement", "ux", "design-system"],
    },
    "FR-019": {
        "title": "Analytics & Business Intelligence",
        "filename": "analytics-business-intelligence",
        "issues": range(415, 420),
        "labels": ["enhancement", "analytics", "bi"],
    },
}


def extract_issue_details(doc_path: Path, issue_num: int) -> dict:
    """
    Extract details for a specific issue from feature request documentation.

    Args:
        doc_path: Path to the feature request markdown file
        issue_num: Issue number to extract

    Returns:
        Dictionary containing issue details
    """
    with open(doc_path, "r") as f:
        content = f.read()

    # Find the issue section
    pattern = rf"### Issue #{issue_num}:([^\n]+)\n(.*?)(?=### Issue #|\Z)"
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        return None

    title = match.group(1).strip()
    body = match.group(2).strip()

    # Extract components
    description = ""
    implementation = ""
    technical_req = ""
    acceptance = ""
    agent = ""

    # Extract description
    desc_match = re.search(r"\*\*Description:\*\*\s*([^\n]+)", body)
    if desc_match:
        description = desc_match.group(1).strip()

    # Extract implementation details
    impl_pattern = (
        r"\*\*Implementation Details:\*\*(.*?)"
        r"(?=\*\*Technical Requirements:\*\*|"
        r"\*\*Acceptance Criteria:\*\*)"
    )
    impl_match = re.search(impl_pattern, body, re.DOTALL)
    if impl_match:
        implementation = impl_match.group(1).strip()

    # Extract technical requirements
    tech_pattern = (
        r"\*\*Technical Requirements:\*\*(.*?)"
        r"(?=\*\*Acceptance Criteria:\*\*)"
    )
    tech_match = re.search(tech_pattern, body, re.DOTALL)
    if tech_match:
        technical_req = tech_match.group(1).strip()

    # Extract acceptance criteria
    acc_pattern = (
        r"\*\*Acceptance Criteria:\*\*(.*?)"
        r"(?=\*\*Recommended Agent:\*\*|\Z)"
    )
    acc_match = re.search(acc_pattern, body, re.DOTALL)
    if acc_match:
        acceptance = acc_match.group(1).strip()

    # Extract recommended agent
    agent_match = re.search(r"\*\*Recommended Agent:\*\*\s*([^\n]+)", body)
    if agent_match:
        agent = agent_match.group(1).strip()

    return {
        "title": title,
        "description": description,
        "implementation": implementation,
        "technical": technical_req,
        "acceptance": acceptance,
        "agent": agent,
    }


def generate_issue_markdown(
    issue_num: int, details: dict, fr_id: str, fr_title: str, labels: list
) -> str:
    """
    Generate GitHub issue markdown content.

    Args:
        issue_num: Issue number
        details: Issue details dictionary
        fr_id: Feature request ID (e.g., "FR-015")
        fr_title: Feature request title
        labels: List of labels to apply

    Returns:
        Markdown formatted issue content
    """
    fr_doc_path = fr_id.replace("-", "-").lower()
    markdown = f"""---
title: "Issue #{issue_num}: {details['title']}"
labels: {', '.join(labels)}
feature_request: {fr_id}
---

# Issue #{issue_num}: {details['title']}

**Part of:** [{fr_id}: {fr_title}](
    ../../../docs/feature_requests/{fr_doc_path}.md
)

## Description

{details['description']}

## Implementation Details

{details['implementation']}

## Technical Requirements

{details['technical']}

## Acceptance Criteria

{details['acceptance']}

## Recommended Agent

{details['agent']}

---

## How to Implement

1. Review the feature request documentation in
   `docs/feature_requests/{fr_doc_path}.md`
2. Assign this issue to the recommended agent if available
3. Create a feature branch:
   `git checkout -b issue-{issue_num}-<short-description>`
4. Implement the changes following the acceptance criteria
5. Write tests for the new functionality
6. Submit a pull request referencing this issue

## Related Issues

- Feature Request: #{fr_id.replace('FR-', '')}
- See other sub-issues in the feature request documentation

## Resources

- [Feature Request Documentation](../../../docs/feature_requests/)
- [Project Board](https://github.com/users/markus41/projects/22)
- [Contributing Guidelines](../../../CONTRIBUTING.md)
"""
    return markdown


def main():
    """Generate issue markdown files for all sub-issues."""
    # Create output directory
    output_dir = Path("/tmp/github_issues")
    output_dir.mkdir(exist_ok=True)

    # Path to feature request docs
    docs_dir = Path(__file__).parent.parent / "docs" / "feature_requests"

    total_issues = 0

    for fr_id, fr_data in FEATURE_REQUESTS.items():
        fr_title = fr_data["title"]
        filename = fr_data["filename"]
        labels = fr_data["labels"]

        # Find the documentation file
        doc_file = docs_dir / f"{fr_id}-{filename}.md"

        if not doc_file.exists():
            print(f"Warning: Documentation file not found: {doc_file}")
            continue

        print(f"\nProcessing {fr_id}: {fr_title}")
        print(f"Documentation: {doc_file}")

        for issue_num in fr_data["issues"]:
            details = extract_issue_details(doc_file, issue_num)

            if not details:
                msg = (
                    f"  Warning: Could not extract details for issue "
                    f"#{issue_num}"
                )
                print(msg)
                continue

            # Generate markdown
            markdown = generate_issue_markdown(
                issue_num, details, fr_id, fr_title, labels
            )

            # Write to file
            output_file = output_dir / f"issue-{issue_num}.md"
            with open(output_file, "w") as f:
                f.write(markdown)

            print(f"  ✓ Generated: issue-{issue_num}.md - {details['title']}")
            total_issues += 1

    print(f"\n{'='*60}")
    print(f"Successfully generated {total_issues} issue files")
    print(f"Output directory: {output_dir}")
    print(f"{'='*60}\n")
    print("Next steps:")
    print("1. Review the generated markdown files")
    print("2. Create GitHub issues manually using the content")
    print("3. Or use GitHub CLI: gh issue create -F <file>")
    print("4. Set up project board tracking")


if __name__ == "__main__":
    main()
