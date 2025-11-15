# GitHub Issues Creation Guide

This guide explains how to create GitHub issues for Feature Requests #15-19 and their 77 sub-issues.

## Overview

We have documented 5 major feature requests with 77 sub-issues. This guide will help you:
1. Understand the documentation structure
2. Create GitHub issues efficiently
3. Assign them to the appropriate agents
4. Track progress on the project board

## Documentation Structure

```
docs/feature_requests/
├── README.md                                    # Master index
├── FR-015-automation-workflow-engine.md         # Feature #15 + Issues #343-349
├── FR-016-integration-hub-api-platform.md       # Feature #16 + Issues #350-357
├── FR-017-mobile-first-pwa.md                   # Feature #17 + Issues #358-369
├── FR-018-ux-design-system.md                   # Feature #18 + Issues #370-414
└── FR-019-analytics-business-intelligence.md    # Feature #19 + Issues #415-419
```

## Methods for Creating Issues

### Method 1: Manual Creation via GitHub UI (Recommended for Small Batches)

**Best for:** Creating 1-5 issues at a time

1. Navigate to: https://github.com/markus41/portfolio/issues/new/choose
2. Select the appropriate template:
   - Use "Feature Request - Batch Creation Template" for feature-related issues
   - Use standard "Feature Request" template for individual issues
3. Fill in the details from the documentation
4. Reference the parent feature request number
5. Apply appropriate labels
6. Assign to recommended agents if available
7. Add to project board

**Example for Issue #343:**
```
Title: [Feature]: Create Welcome Series for New Members
Labels: enhancement, automation, workflow, email
Feature Request: FR-015
Description: [Copy from FR-015-automation-workflow-engine.md]
```

### Method 2: Using the Issue Generation Script

**Best for:** Generating markdown files for batch creation

1. Run the script to generate markdown files:
   ```bash
   python scripts/generate_issue_files.py
   ```

2. Review generated files in `/tmp/github_issues/`:
   ```bash
   ls -la /tmp/github_issues/
   ```

3. For each issue, you can either:
   
   **Option A: Use GitHub CLI (if installed)**
   ```bash
   gh issue create -F /tmp/github_issues/issue-343.md
   ```
   
   **Option B: Copy-paste into GitHub UI**
   - Open the markdown file
   - Copy the content
   - Navigate to GitHub > New Issue
   - Paste the content
   - Adjust as needed

### Method 3: Bulk Import via GitHub API (Advanced)

**Best for:** Creating all 77+ issues at once

**Prerequisites:**
- GitHub Personal Access Token with `repo` scope
- Python with `requests` library installed

**Script to create issues programmatically:**

```python
import os
import requests
from pathlib import Path

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Set this environment variable
REPO_OWNER = "markus41"
REPO_NAME = "portfolio"
ISSUE_DIR = Path("/tmp/github_issues")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def create_issue(title, body, labels, milestone=None, assignees=None):
    """Create a GitHub issue via API."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    
    data = {
        "title": title,
        "body": body,
        "labels": labels,
    }
    
    if milestone:
        data["milestone"] = milestone
    if assignees:
        data["assignees"] = assignees
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 201:
        issue = response.json()
        print(f"✓ Created: #{issue['number']} - {title}")
        return issue
    else:
        print(f"✗ Failed: {title}")
        print(f"  Error: {response.json()}")
        return None

def main():
    """Create all issues from generated markdown files."""
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN environment variable not set")
        return
    
    # Iterate through all issue files
    for issue_file in sorted(ISSUE_DIR.glob("issue-*.md")):
        with open(issue_file, "r") as f:
            content = f.read()
        
        # Extract title from markdown frontmatter
        title_match = re.search(r'title: "([^"]+)"', content)
        if not title_match:
            print(f"Warning: Could not extract title from {issue_file}")
            continue
        
        title = title_match.group(1)
        
        # Extract labels
        labels_match = re.search(r'labels: (.+)', content)
        labels = labels_match.group(1).split(", ") if labels_match else []
        
        # Extract body (everything after frontmatter)
        body_match = re.search(r'---\n\n(.+)', content, re.DOTALL)
        body = body_match.group(1) if body_match else content
        
        # Create the issue
        create_issue(title, body, labels)

if __name__ == "__main__":
    main()
```

**To use this script:**
```bash
export GITHUB_TOKEN="your_github_personal_access_token"
python scripts/create_issues_bulk.py
```

## Organizing Issues on Project Board

### Step 1: Create Milestones

Create milestones for each feature request:

1. Go to: https://github.com/markus41/portfolio/milestones
2. Click "New milestone"
3. Create these milestones:
   - **FR-015: Automation & Workflow Engine** (Due: +6 weeks)
   - **FR-016: Integration Hub & API Platform** (Due: +8 weeks)
   - **FR-017: Mobile-First Experience & PWA** (Due: +8 weeks)
   - **FR-018: User Experience & Design System** (Due: +5 weeks)
   - **FR-019: Analytics & Business Intelligence** (Due: +8 weeks)

### Step 2: Configure Project Board

1. Navigate to: https://github.com/users/markus41/projects/22
2. Set up these columns (if not already present):
   - **Backlog** - Not yet started
   - **Ready** - Ready to start work
   - **In Progress** - Currently being worked on
   - **Review** - Awaiting review/testing
   - **Done** - Completed

### Step 3: Add Custom Fields

Add these custom fields to the project:
- **Feature Request** (Single select): FR-015, FR-016, FR-017, FR-018, FR-019
- **Priority** (Single select): Critical, High, Medium, Low
- **Estimated Time** (Number): In hours or days
- **Assigned Agent** (Text): Name of assigned GitHub agent

### Step 4: Create Views

Create filtered views for each feature request:

**View: FR-015 Automation**
- Filter: `feature_request:FR-015`
- Group by: Priority
- Sort by: Issue number

**View: FR-016 Integration**
- Filter: `feature_request:FR-016`
- Group by: Priority
- Sort by: Issue number

(Repeat for FR-017, FR-018, FR-019)

## Assigning to GitHub Agents

Each sub-issue documentation includes a "Recommended Agent" section. When creating issues:

1. Check available custom GitHub agents in your organization
2. Match the recommended agent type to available agents
3. Assign in the issue description or as an assignee
4. If agent not available, assign to team member with relevant expertise

### Agent Assignment Examples

**For Issue #343 (Welcome Series):**
- Recommended: Email automation specialist
- Available agents: Check `.github/agents/` directory
- Assign to: The agent that handles email/notification workflows

**For Issue #350 (Calendar Sync):**
- Recommended: Integration specialist or calendar sync agent
- Available agents: Check for OAuth/integration agents
- Assign to: The agent that handles third-party integrations

## Labels to Use

Apply these labels when creating issues:

**Feature Labels:**
- `enhancement` - All feature requests
- `automation` - FR-015 issues
- `integration` - FR-016 issues
- `mobile` - FR-017 issues
- `pwa` - FR-017 PWA-specific issues
- `ux` - FR-018 issues
- `design-system` - FR-018 design issues
- `analytics` - FR-019 issues
- `bi` - FR-019 BI issues

**Priority Labels:**
- `priority-critical` - Must be done first
- `priority-high` - Important for success
- `priority-medium` - Should be done
- `priority-low` - Nice to have

**Status Labels:**
- `status-blocked` - Blocked by dependency
- `status-needs-review` - Needs stakeholder review
- `status-ready` - Ready to start

## Issue Dependencies

Some issues have dependencies. Document these using:

1. **GitHub Task Lists** in the issue description:
   ```markdown
   ## Dependencies
   - [ ] #349 must be completed first (approval engine)
   - [ ] Requires Twilio account setup
   ```

2. **Issue References** in comments:
   ```markdown
   Blocked by #349 - waiting for approval workflow engine
   ```

3. **Project Board** - Don't move to "Ready" until dependencies resolved

### Key Dependencies to Note

- **Issue #349** (Approval Workflow Engine) enables:
  - #348 (Chapter Transfer Workflow)
  - #347 (Certification Warnings)

- **Issue #363** (PWA Capability) enables:
  - #364 (Offline Mode)
  - #365 (Push Notifications)

- **Issue #383** (Loading Skeletons) should be completed before:
  - Other UX improvements

## Tracking Progress

### Weekly Review

Every week, review:
1. Issues completed vs. planned
2. Blockers and dependencies
3. Agent workload balance
4. Timeline adjustments needed

### Metrics Dashboard

Track these metrics:
- Issues created vs. completed
- Average time to close
- Issues by priority
- Issues by feature request
- Agent utilization

### Reporting

Generate reports using:

**GitHub CLI:**
```bash
# List all FR-015 issues
gh issue list --label "automation" --json number,title,state

# Count issues by state
gh issue list --label "enhancement" --json state --jq 'group_by(.state)|map({state: .[0].state, count: length})'
```

**Project Board Views:**
- Use the built-in insights tab
- Export to CSV for external reporting
- Set up automation rules for status updates

## Best Practices

### When Creating Issues

1. ✅ **Include all acceptance criteria** from documentation
2. ✅ **Reference the parent feature request**
3. ✅ **Apply all relevant labels**
4. ✅ **Assign to recommended agent if available**
5. ✅ **Add to project board immediately**
6. ✅ **Link related issues**
7. ✅ **Set appropriate milestone**

### When Working on Issues

1. ✅ **Comment when starting work**
2. ✅ **Update status on project board**
3. ✅ **Reference issue in commit messages**: `feat: add welcome series emails (#343)`
4. ✅ **Request review when ready**
5. ✅ **Update documentation if needed**
6. ✅ **Close only when acceptance criteria met**

### When Completing Issues

1. ✅ **Verify all acceptance criteria checked**
2. ✅ **Link to pull request**
3. ✅ **Update documentation**
4. ✅ **Add testing notes**
5. ✅ **Move to Done on project board**

## Troubleshooting

### Problem: Too many issues to create manually

**Solution:** Use the bulk creation script (Method 3) or generate markdown files (Method 2) and use GitHub CLI.

### Problem: Agent assignments unclear

**Solution:** Review the "Recommended Agent" section in each issue documentation. If unsure, assign to a team lead for delegation.

### Problem: Dependencies not clear

**Solution:** Review the implementation priority section in each feature request document. Check the dependency notes in the master README.

### Problem: Can't see custom fields in project board

**Solution:** Ensure you're using GitHub Projects v2. Legacy project boards don't support custom fields.

## Resources

- [Feature Request Documentation](../docs/feature_requests/)
- [Project Board](https://github.com/users/markus41/projects/22)
- [GitHub Issues Documentation](https://docs.github.com/en/issues)
- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [GitHub CLI Documentation](https://cli.github.com/manual/)

## Support

For questions or issues with this process:
1. Create a question issue using the [question template](.github/ISSUE_TEMPLATE/question.yml)
2. Tag with `help-wanted` label
3. Reference this guide in your question

---

**Last Updated:** 2025-11-15  
**Maintained by:** Project Management Team
