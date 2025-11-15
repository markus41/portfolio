"""
Test the issue generation script to ensure data integrity.
"""

import json
from pathlib import Path


def test_github_issues_file_exists():
    """Test that the github_issues.json file was created."""
    assert Path("github_issues.json").exists()


def test_github_issues_structure():
    """Test the structure of the generated issues."""
    with open("github_issues.json") as f:
        data = json.load(f)

    # Check top-level structure
    assert "feature_requests" in data
    assert "sub_issues" in data
    assert "summary" in data

    # Check summary
    assert data["summary"]["total_feature_requests"] == 5
    assert data["summary"]["total_sub_issues"] == 114


def test_feature_requests_content():
    """Test that feature requests have all required fields."""
    with open("github_issues.json") as f:
        data = json.load(f)

    feature_requests = data["feature_requests"]
    assert len(feature_requests) == 5

    for fr in feature_requests:
        # Check required fields
        assert "number" in fr
        assert "title" in fr
        assert "body" in fr
        assert "labels" in fr
        assert "assigned_agent" in fr

        # Check labels
        assert "enhancement" in fr["labels"]
        assert "feature-request" in fr["labels"]

        # Check body contains required sections
        assert "Feature Category" in fr["body"]
        assert "Problem Statement" in fr["body"]
        assert "Proposed Solution" in fr["body"]
        assert "Alternatives Considered" in fr["body"]
        assert "Expected Impact" in fr["body"]
        assert "Technical Considerations" in fr["body"]
        assert "Assigned Agent" in fr["body"]


def test_sub_issues_content():
    """Test that sub-issues have all required fields."""
    with open("github_issues.json") as f:
        data = json.load(f)

    sub_issues = data["sub_issues"]
    assert len(sub_issues) == 114

    for issue in sub_issues:
        # Check required fields
        assert "number" in issue
        assert "title" in issue
        assert "body" in issue
        assert "labels" in issue
        assert "parent_feature" in issue
        assert "assigned_agent" in issue

        # Check labels
        assert "enhancement" in issue["labels"]
        assert "sub-issue" in issue["labels"]

        # Check parent feature is valid
        assert issue["parent_feature"] in [7, 8, 9, 10, 11]

        # Check body contains required sections
        assert "Description" in issue["body"]
        assert "Parent Feature Request" in issue["body"]


def test_issue_numbering():
    """Test that issue numbers are correct and sequential."""
    with open("github_issues.json") as f:
        data = json.load(f)

    # Feature requests should be 7-11
    fr_numbers = [fr["number"] for fr in data["feature_requests"]]
    assert fr_numbers == [7, 8, 9, 10, 11]

    # Sub-issues should be 130-243
    sub_numbers = [issue["number"] for issue in data["sub_issues"]]
    assert sub_numbers[0] == 130
    assert sub_numbers[-1] == 243
    assert len(sub_numbers) == 114


def test_agent_assignments():
    """Test that all issues have agent assignments."""
    with open("github_issues.json") as f:
        data = json.load(f)

    # Check all feature requests have agents
    for fr in data["feature_requests"]:
        assert fr["assigned_agent"]
        assert len(fr["assigned_agent"]) > 0

    # Check all sub-issues have agents
    for issue in data["sub_issues"]:
        assert issue["assigned_agent"]
        assert len(issue["assigned_agent"]) > 0


def test_sub_issues_distribution():
    """
    Test that sub-issues are correctly distributed across feature
    requests.
    """
    with open("github_issues.json") as f:
        data = json.load(f)

    # Group by parent feature
    by_parent = {}
    for issue in data["sub_issues"]:
        parent = issue["parent_feature"]
        if parent not in by_parent:
            by_parent[parent] = []
        by_parent[parent].append(issue)

    # Expected distribution
    assert len(by_parent[7]) == 35  # Member Management
    assert len(by_parent[8]) == 24  # Campaign & Email
    assert len(by_parent[9]) == 19  # LMS
    assert len(by_parent[10]) == 19  # Reporting
    assert len(by_parent[11]) == 17  # Event Management


def test_summary_file_exists():
    """Test that the summary markdown file was created."""
    assert Path("github_issues_summary.md").exists()


def test_summary_file_content():
    """Test that the summary file contains expected content."""
    with open("github_issues_summary.md") as f:
        content = f.read()

    # Check headings
    assert "# GitHub Issues Summary" in content
    assert "## Feature Requests" in content
    assert "## Sub-Issues Summary" in content

    # Check feature request sections
    assert "[Feature #7]" in content
    assert "[Feature #8]" in content
    assert "[Feature #9]" in content
    assert "[Feature #10]" in content
    assert "[Feature #11]" in content

    # Check sub-issue ranges
    assert "Feature Request #7 (35 sub-issues)" in content
    assert "Feature Request #8 (24 sub-issues)" in content
    assert "Feature Request #9 (19 sub-issues)" in content
    assert "Feature Request #10 (19 sub-issues)" in content
    assert "Feature Request #11 (17 sub-issues)" in content
