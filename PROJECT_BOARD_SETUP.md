# GitHub Project Board Setup Guide

This guide explains how to configure columns in the GitHub Project board at https://github.com/users/markus41/projects/22/views/1 to organize issues based on the available issue templates.

## Overview

The repository now includes comprehensive issue templates that automatically label issues. These labels can be used to organize issues into columns on the GitHub Project board.

## Available Issue Templates

The following issue templates are available in `.github/ISSUE_TEMPLATE/`:

| Template File | Title Prefix | Labels | Purpose |
|--------------|--------------|---------|---------|
| `bug_report.yml` | `[Bug]:` | `bug` | Report reproducible problems |
| `feature_request.yml` | `[Feature]:` | `enhancement` | Suggest improvements or new ideas |
| `accessibility.yml` | `[A11y]:` | `accessibility`, `enhancement` | Report accessibility issues |
| `documentation_request.yml` | `[Docs]:` | `documentation`, `enhancement` | Request new or improved documentation |
| `performance.yml` | `[Performance]:` | `performance`, `enhancement` | Report performance issues |
| `question.yml` | `[Question]:` | `question` | Ask questions about the project |
| `security.yml` | `[Security]:` | `security`, `priority-high` | Report security vulnerabilities |

## Recommended Project Board Columns

To effectively organize issues on the project board, create the following columns:

### 1. Triage
- **Purpose**: Newly created issues that haven't been reviewed yet
- **Filter**: No status assigned
- **Workflow**: Review and assign to appropriate column

### 2. Bug
- **Purpose**: Confirmed bugs that need to be fixed
- **Filter**: Label = `bug`
- **Workflow**: Move to "In Progress" when work starts

### 3. Enhancement
- **Purpose**: New features and general improvements
- **Filter**: Label = `enhancement` AND NOT (`accessibility` OR `documentation` OR `performance`)
- **Workflow**: Prioritize and move to "In Progress" when ready

### 4. Accessibility
- **Purpose**: Accessibility improvements and issues
- **Filter**: Label = `accessibility`
- **Workflow**: Prioritize based on severity

### 5. Documentation
- **Purpose**: Documentation requests and improvements
- **Filter**: Label = `documentation`
- **Workflow**: Assign to documentation writers

### 6. Performance
- **Purpose**: Performance optimization tasks
- **Filter**: Label = `performance`
- **Workflow**: Benchmark and prioritize improvements

### 7. Security
- **Purpose**: Security-related issues and improvements
- **Filter**: Label = `security`
- **Workflow**: High priority, address immediately

### 8. Question
- **Purpose**: Questions needing answers
- **Filter**: Label = `question`
- **Workflow**: Answer and close when resolved

### 9. In Progress
- **Purpose**: Issues currently being worked on
- **Filter**: Status = "In Progress" or assignee is not empty
- **Workflow**: Move to "Review" when PR is created

### 10. Review
- **Purpose**: Issues with open pull requests
- **Filter**: Linked PR exists and PR status = "Open"
- **Workflow**: Move to "Done" when PR is merged

### 11. Done
- **Purpose**: Completed issues
- **Filter**: Status = "Done" or issue is closed
- **Workflow**: Archive after verification

## How to Set Up Columns in GitHub Projects (v2)

Since GitHub Projects now uses a more flexible board system, follow these steps:

### Step 1: Access the Project
1. Navigate to https://github.com/users/markus41/projects/22
2. Click on the project to open it

### Step 2: Add Single Select Field for Issue Types
1. Click the "+" button next to field headers
2. Select "Single select" as the field type
3. Name it "Type" or "Issue Type"
4. Add the following options:
   - Bug
   - Enhancement
   - Accessibility
   - Documentation
   - Performance
   - Security
   - Question

### Step 3: Configure Views
Create filtered views for each type:

1. Click on the current view name (e.g., "Table" or "Board")
2. Click "+ New view"
3. Choose "Board" layout
4. Name it appropriately (e.g., "By Issue Type")
5. Group by: "Labels" or your custom "Type" field

### Step 4: Set Up Automation (Optional)

GitHub Projects can automatically move cards based on certain triggers:

1. Go to Project Settings (⚙️ icon)
2. Click on "Workflows"
3. Enable these workflows:
   - **Item added to project**: Set default status to "Triage"
   - **Item closed**: Move to "Done"
   - **Pull request merged**: Move linked issues to "Done"

### Step 5: Bulk Organize Existing Issues

If you have existing issues:

1. Use the bulk edit feature (select multiple issues)
2. Apply appropriate labels based on issue content
3. Assign to relevant columns/statuses

## Alternative: Using Built-in Project Templates

GitHub provides project templates that you can customize:

1. Go to your project
2. Click on "..." (more options)
3. Select "Settings"
4. Look for template options or field configurations
5. Create custom fields and views based on your needs

## Automation with GitHub Actions

For advanced automation, you can create GitHub Actions workflows that:

- Automatically label issues based on templates
- Move issues between columns
- Send notifications for specific issue types
- Generate reports on issue distribution

Example workflow location: `.github/workflows/project-automation.yml`

## Tips for Effective Project Management

1. **Prioritize Security Issues**: Always address security issues first
2. **Group Related Issues**: Use labels and milestones to group related work
3. **Regular Triage**: Schedule regular triage sessions to review new issues
4. **Use Milestones**: Create milestones for releases and major features
5. **Link PRs**: Always link pull requests to their related issues
6. **Update Status**: Keep issue statuses up to date as work progresses

## Label Management

All labels are automatically applied by the issue templates. If you need to add or modify labels:

1. Go to https://github.com/markus41/portfolio/labels
2. Create or edit labels as needed
3. Update issue templates to use the new labels

## Common Labels

| Label | Color | Description |
|-------|-------|-------------|
| `bug` | Red | Something isn't working |
| `enhancement` | Blue | New feature or request |
| `accessibility` | Purple | Accessibility improvements |
| `documentation` | Light blue | Documentation improvements |
| `performance` | Orange | Performance optimizations |
| `question` | Pink | Questions or help needed |
| `security` | Dark red | Security issues |
| `priority-high` | Red | High priority items |

## Manual Setup Instructions

If you prefer to set up columns manually:

1. Open the project board
2. Click "+ Add column" or equivalent
3. Name the column (e.g., "Bug", "Enhancement", etc.)
4. Configure column automation rules:
   - **Preset**: Choose "To do", "In progress", or "Done"
   - **Move issues here when**: Set conditions based on labels or status
5. Repeat for each column type

## Need Help?

If you need assistance setting up the project board:

1. Check [GitHub Projects documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
2. Create an issue using the Question template
3. Contact the project maintainers

## Summary

By following this guide, you'll have a well-organized project board that automatically categorizes issues based on their type, making it easier to prioritize and manage work across different areas of the project.
