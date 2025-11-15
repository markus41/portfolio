# Using the Issue Management System

This guide explains how to use the comprehensive issue management system that has been created for managing large feature requests with multiple sub-issues.

## Overview

The system manages **3 major feature requests** with a total of **93 sub-issues**:

1. **Feature Request #4**: Document Distribution & Management System (13 sub-issues)
2. **Feature Request #5**: Dashboard & Analytics Platform (37 sub-issues)
3. **Feature Request #6**: Navigation & User Experience Overhaul (43 sub-issues)

## Quick Start

### Option 1: Using the Python Script

The primary tool is the Python script at `scripts/generate_issues.py`.

**Preview what issues would be created:**
```bash
python scripts/generate_issues.py --dry-run
```

**Create issues on GitHub (requires GitHub CLI):**
```bash
python scripts/generate_issues.py --create
```

**Export documentation:**
```bash
python scripts/generate_issues.py --export-md --export-json
```

### Option 2: Using GitHub Actions

1. Navigate to the **Actions** tab in your GitHub repository
2. Select the **"Issue Management Automation"** workflow
3. Click **"Run workflow"**
4. Choose an action:
   - **preview**: View what issues would be created
   - **create-issues**: Create issues on GitHub
   - **export-docs**: Generate documentation files

### Option 3: Using Issue Templates

When creating issues manually:

1. Go to **Issues** → **New Issue**
2. Choose the appropriate template:
   - **Epic Feature Request**: For large features with sub-issues
   - **Sub-Issue**: For individual tasks within a feature
   - Standard templates (Bug, Enhancement, etc.) for other issues

## Prerequisites

### For Python Script

1. **Python 3.9+** installed
2. **GitHub CLI** installed and authenticated (for `--create` option):
   ```bash
   # Install GitHub CLI
   # See: https://cli.github.com/
   
   # Authenticate
   gh auth login
   ```

3. **Repository write access** to create issues

### For GitHub Actions

- Repository must have Actions enabled
- Workflow will use `GITHUB_TOKEN` automatically

## Feature Requests Details

### Feature Request #4: Document Distribution & Management System

**Priority**: High  
**Category**: Document Management/Navigation Enhancement  
**Estimated Time**: 5-6 weeks

**Problem**: No system for distributing documents throughout the organization hierarchy. Cannot target documents to specific chapters, states, or nationwide. No OCR capability, no approval workflows, and no tracking.

**Sub-Issues (13 total)**:
- Build Hierarchical Document Upload Wizard (#37)
- Add Distribution Targeting (#38)
- Implement Document Scanning/OCR Integration (#39)
- Create Multi-Stage Approval Workflow (#40)
- Add Document View/Download Tracking (#41)
- Build Searchable Document Library (#42)
- Create Resource Library with Categories (#43)
- Implement Document Version Control (#44)
- Add Video Content Library (#45)
- Integrate Podcast Player (#46)
- Build Blog/News Article System (#47)
- Create FAQ Management System (#48)
- Add Knowledge Base with Search (#49)

### Feature Request #5: Dashboard & Analytics Platform

**Priority**: Medium-High  
**Category**: Analytics/Dashboard Enhancement  
**Estimated Time**: 4-5 weeks

**Problem**: Dashboard has poor UX with vertical bar charts, no data labels, non-clickable elements, no period comparisons, and no customization options.

**Sub-Issues (37 total)**:
- Redesign Revenue Chart to Horizontal Bars (#50)
- Add Data Labels Directly on Chart Bars (#51)
- Make All Dashboard Elements Clickable (#52)
- Add Period Comparison Toggles (#53)
- Implement Dashboard Customization (#54)
- [... and 32 more]

### Feature Request #6: Navigation & User Experience Overhaul

**Priority**: High  
**Category**: Navigation/UX Enhancement  
**Estimated Time**: 3-4 weeks

**Problem**: Current navigation is limited with narrow search bar, no AI-powered search, missing breadcrumbs, no notifications, and no quick access menu.

**Sub-Issues (43 total)**:
- Expand Search Bar to 400px Width (#87)
- Add AI-Powered Search (#88)
- Implement Breadcrumb Navigation (#89)
- Add User Profile/Settings Dropdown (#90)
- Include Notification Bell with Count (#91)
- [... and 38 more]

## Agent Assignment System

Issues are automatically assigned to specialized agent types based on their requirements:

| Agent Type | Responsibilities |
|------------|------------------|
| **Frontend Development Agent** | UI/UX implementation, React components, styling |
| **Backend Development Agent** | Server-side logic, APIs, data processing |
| **Full-Stack Development Agent** | End-to-end feature implementation |
| **Database Agent** | Schema design, queries, migrations |
| **DevOps/Infrastructure Agent** | Deployment, infrastructure, monitoring |
| **Security Agent** | Security features, audits, vulnerability fixes |
| **UX/UI Design Agent** | User experience design, mockups, prototypes |
| **Machine Learning Agent** | AI/ML features, model training, predictions |
| **Documentation Agent** | Documentation, guides, tutorials |
| **Testing/QA Agent** | Testing, quality assurance, test automation |

## Issue Labels

The system uses these labels to categorize issues:

- `enhancement` - New features and improvements
- `needs-breakdown` - Epic features that need sub-issues
- `sub-issue` - Tasks that are part of a larger feature
- `priority-high` - High priority items
- `priority-medium-high` - Medium-high priority items
- `document-management` - Document-related features
- `analytics` - Analytics and reporting features
- `dashboard` - Dashboard-related features
- `navigation` - Navigation and UX features
- `ux` - User experience improvements
- `frontend` - Frontend development work
- `backend` - Backend development work
- `ml` - Machine learning features

## Project Board Organization

Add these columns to your GitHub Project board:

1. **Triage** - New issues awaiting review
2. **Bug** - Confirmed bugs (`bug` label)
3. **Epic Features** - Large features (`needs-breakdown` label)
4. **Enhancement** - Standard enhancements
5. **Sub-Issues** - Sub-tasks (`sub-issue` label)
6. **In Progress** - Active work
7. **Review** - Pull requests under review
8. **Done** - Completed work

See [PROJECT_BOARD_SETUP.md](PROJECT_BOARD_SETUP.md) for detailed setup instructions.

## Generated Documentation

The system generates two documentation files:

### ISSUES_OVERVIEW.md
Comprehensive markdown documentation with:
- Full description of each feature request
- All sub-issues with descriptions
- Agent assignments
- Estimates
- Labels

### issues_data.json
Structured JSON data containing:
- All feature request data
- All sub-issue data
- Agent type definitions

Use this for:
- Programmatic access to issue data
- Integration with other tools
- Custom reporting

## Workflow Integration

The GitHub Actions workflow (`.github/workflows/issue-automation.yml`) provides:

1. **Preview Mode**: See what issues would be created without actually creating them
2. **Create Mode**: Automatically create all issues with proper labels and relationships
3. **Export Mode**: Generate/update documentation files
4. **Validation**: Check that all issue templates are valid

## Common Tasks

### Create All Issues at Once

```bash
# Preview first
python scripts/generate_issues.py --dry-run

# Create on GitHub
python scripts/generate_issues.py --create
```

### Update Documentation

```bash
python scripts/generate_issues.py --export-md --export-json
git add ISSUES_OVERVIEW.md issues_data.json
git commit -m "docs: update issue documentation"
git push
```

### Create a Single Feature Request Manually

1. Go to **Issues** → **New Issue**
2. Select **"Epic Feature Request"** template
3. Fill in the form:
   - Feature number (e.g., FR-4)
   - Subtitle
   - Category
   - Problem statement
   - Solution
   - Alternatives
   - Impact
   - Priority
   - Technical considerations
   - Sub-issues list
   - Required agent types

### Create a Sub-Issue Manually

1. Go to **Issues** → **New Issue**
2. Select **"Sub-Issue"** template
3. Fill in the form:
   - Parent issue reference (e.g., #4)
   - Description
   - Acceptance criteria
   - Component area
   - Suggested agents
   - Estimate

## Customization

### Adding New Feature Requests

Edit `scripts/generate_issues.py` and add your feature request to the data structure:

```python
FEATURE_REQUEST_X = {
    "number": X,
    "title": "Your Feature Title",
    "subtitle": "Descriptive Subtitle",
    "category": "Category Name",
    "problem": "Problem description",
    "solution": "Solution description",
    # ... more fields
    "sub_issues": [
        {
            "number": YY,
            "title": "Sub-issue title",
            "description": "What needs to be done",
            # ... more fields
        },
    ],
}

# Add to ALL_FEATURE_REQUESTS
ALL_FEATURE_REQUESTS = [FEATURE_REQUEST_4, FEATURE_REQUEST_5, FEATURE_REQUEST_6, FEATURE_REQUEST_X]
```

### Adding New Agent Types

Update the `AGENT_TYPES` dictionary in `scripts/generate_issues.py`:

```python
AGENT_TYPES = {
    "your_agent": "Your Agent Name",
    # ... existing agents
}
```

Then reference it in sub-issues:

```python
{
    "number": 100,
    "title": "Your Issue",
    # ...
    "agents": ["your_agent", "backend"],
}
```

## Troubleshooting

### GitHub CLI Issues

```bash
# Check if gh is installed
gh --version

# Login
gh auth login

# Check authentication
gh auth status
```

### Permission Issues

```bash
# Make script executable
chmod +x scripts/generate_issues.py
```

### Import Errors

```bash
# Install dependencies
pip install -r requirements.txt
```

## Best Practices

1. **Preview First**: Always use `--dry-run` before creating issues
2. **Batch Creation**: Create all issues at once to maintain proper numbering
3. **Link Issues**: Link sub-issues to their parent feature request
4. **Use Labels**: Apply appropriate labels for filtering and organization
5. **Update Progress**: Check off completed sub-issues in the parent feature description
6. **Documentation**: Keep `ISSUES_OVERVIEW.md` up to date

## Support

For questions or issues with the issue management system:

1. Check [scripts/README.md](scripts/README.md) for script documentation
2. Check [PROJECT_BOARD_SETUP.md](PROJECT_BOARD_SETUP.md) for board setup
3. Review [ISSUES_OVERVIEW.md](ISSUES_OVERVIEW.md) for issue details
4. Create an issue using the **Question** template

## Next Steps

1. **Review the generated issues** in `ISSUES_OVERVIEW.md`
2. **Set up your project board** using [PROJECT_BOARD_SETUP.md](PROJECT_BOARD_SETUP.md)
3. **Create the issues** using `python scripts/generate_issues.py --create`
4. **Assign team members** to appropriate issues based on agent types
5. **Start working** on high-priority items first

---

For more information about the repository itself, see the main [README.md](README.md).
