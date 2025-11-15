# GitHub Issues Generation Documentation

This directory contains scripts and data for generating GitHub issues for the portfolio repository feature requests.

## Overview

The feature request system includes 5 major feature requests (#7-#11) with 114 sub-issues (#130-#243) covering:

1. **Feature Request #7**: Member Management System Enhancement (35 sub-issues)
2. **Feature Request #8**: Campaign & Email Marketing Platform (24 sub-issues)
3. **Feature Request #9**: Learning Management System (19 sub-issues)
4. **Feature Request #10**: Advanced Reporting System (19 sub-issues)
5. **Feature Request #11**: Event Management System (17 sub-issues)

## Files

- `generate_feature_issues.py` - Python script that generates structured issue data
- `create_github_issues.sh` - Shell script that creates issues using GitHub CLI
- `github_issues.json` - Generated JSON data for all issues (1440 lines)
- `github_issues_summary.md` - Human-readable summary of all issues (277 lines)

## Agent Assignments

Each issue has been assigned to a specialized agent based on its domain:

### Backend Agents
- **Backend/Frontend Integration Agent** - Complex CRUD operations with UI components
- **Backend Schema Agent** - Database schema and custom field management
- **Backend Bug Fix Agent** - Backend issue resolution

### Frontend Agents
- **Frontend Data Grid Agent** - Editable grids, sorting, filtering
- **Frontend Form Agent** - Form handling and inline editing
- **Frontend Filter Agent** - Filtering UI components
- **Frontend CSS Agent** - Styling and layout
- **Frontend Display Agent** - Data presentation and visualization
- **Frontend UX Agent** - User experience improvements
- **Frontend Pagination Agent** - Pagination controls
- **Frontend Layout Agent** - Page layout and structure
- **Frontend Validation Agent** - Form validation and error display
- **Frontend Bug Fix Agent** - Frontend issue resolution

### Specialized Domain Agents
- **Marketing Automation Agent** - Email campaigns and analytics
- **Learning Management Agent** - Educational content and certifications
- **Analytics & Reporting Agent** - Data visualization and reports
- **Event Management Agent** - Event logistics and registration
- **Authentication Agent** - Login, password reset, 2FA
- **Security Agent** - Security features and 2FA

### Data & Integration Agents
- **Data Import Agent** - CSV/Excel imports
- **Data Quality Agent** - Duplicate detection and data cleaning
- **Query Builder Agent** - Visual query builders
- **A/B Testing Agent** - Campaign A/B testing
- **ML Optimization Agent** - AI/ML optimizations
- **SCORM Integration Agent** - SCORM compliance
- **Webinar Integration Agent** - Zoom/Teams integration

### Content & Document Agents
- **Email Template Agent** - Email template management
- **Email Editor Agent** - Drag-and-drop email editor
- **Email Preview Agent** - Email rendering preview
- **Certificate Generator Agent** - PDF certificate generation
- **PDF Generation Agent** - Document generation
- **Rich Text Editor Agent** - Rich text editing

### System & Infrastructure Agents
- **Messaging System Agent** - Internal messaging
- **Chat System Agent** - Real-time chat
- **Forum System Agent** - Discussion forums
- **Comment System Agent** - Comment systems
- **Survey Builder Agent** - Polls and surveys
- **Notification System Agent** - Announcements and banners

### Business Logic Agents
- **Enrollment Tracking Agent** - Course enrollment management
- **Progress Analytics Agent** - Learning progress tracking
- **Assessment Engine Agent** - Quiz and assessment engine
- **Capacity Management Agent** - Course capacity limits
- **Prerequisite Checker Agent** - Course prerequisites
- **Credit Tracking Agent** - CE credit management
- **Recommendation Engine Agent** - Course recommendations
- **Referral Tracking Agent** - Member referral programs
- **Rewards System Agent** - Reward and points systems
- **Membership Lifecycle Agent** - Membership management
- **Business Rules Agent** - Automated business logic

### UI/UX Specialized Agents
- **UI Components Agent** - Reusable UI components
- **UI Visualization Agent** - Data visualization components
- **UI Standardization Agent** - Consistent UI patterns
- **Dashboard Builder Agent** - Dashboard creation
- **Visual Builder Agent** - Drag-and-drop builders
- **Chart Integration Agent** - Chart libraries integration
- **Autocomplete Agent** - Autocomplete functionality

### Operations Agents
- **Report Scheduler Agent** - Scheduled report execution
- **Permissions Management Agent** - Access control
- **Subscription Management Agent** - Newsletter subscriptions
- **Preferences Management Agent** - User preferences
- **Session Scheduler Agent** - Event session management
- **Hotel Management Agent** - Hotel booking management
- **Guest Registration Agent** - Guest/companion registration
- **Sponsor Portal Agent** - Sponsor management
- **Photo Gallery Agent** - Photo galleries
- **Analytics Funnel Agent** - Conversion tracking

## Usage

### Step 1: Generate Issue Data

```bash
python scripts/generate_feature_issues.py
```

This creates:
- `github_issues.json` - Complete issue data in JSON format
- `github_issues_summary.md` - Human-readable summary

### Step 2: Review Generated Issues

Review the summary file to ensure all issues are correctly formatted:

```bash
cat github_issues_summary.md
```

### Step 3: Create Issues on GitHub

**Option A: Using GitHub CLI (Automated)**

```bash
# Ensure you're authenticated
gh auth login

# Run the creation script
./scripts/create_github_issues.sh
```

**Option B: Manual Creation**

Use the `github_issues.json` file to manually create issues through the GitHub web interface.

**Option C: Using GitHub API**

```python
import json
import requests

with open('github_issues.json') as f:
    data = json.load(f)

token = "your_github_token"
repo = "markus41/portfolio"
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# Create feature requests
for fr in data['feature_requests']:
    response = requests.post(
        f"https://api.github.com/repos/{repo}/issues",
        headers=headers,
        json={
            "title": fr["title"],
            "body": fr["body"],
            "labels": fr["labels"]
        }
    )
    print(f"Created: {fr['title']}")

# Create sub-issues
for issue in data['sub_issues']:
    response = requests.post(
        f"https://api.github.com/repos/{repo}/issues",
        headers=headers,
        json={
            "title": issue["title"],
            "body": issue["body"],
            "labels": issue["labels"]
        }
    )
    print(f"Created: {issue['title']}")
```

## Issue Structure

### Feature Request Format

```markdown
## Feature Category
{category}

## Problem Statement
{problem description}

## Proposed Solution
{solution description}

## Alternatives Considered
- Alternative 1
- Alternative 2
- Alternative 3

## Expected Impact
- **Priority**: {priority}
- **Affects**: {affected users}
- **Estimated Time**: {time estimate}
- **Impact**: {expected impact}

## Technical Considerations
{technical details}

## Assigned Agent
{agent name and description}
```

### Sub-Issue Format

```markdown
## Description
{detailed description}

## Parent Feature Request
This is a sub-issue of Feature Request #{parent_number}

## Related Issues
- Part of #{feature_request_number}

## Assigned Agent
{agent name}
```

## Labels

All issues are labeled with:

### Feature Requests
- `enhancement`
- `feature-request`
- `medium` (priority)

### Sub-Issues
- `enhancement`
- `sub-issue`
- `feature-{parent_number}` (e.g., `feature-7`)

## Statistics

- **Total Feature Requests**: 5
- **Total Sub-Issues**: 114
- **Feature Request Numbers**: 7, 8, 9, 10, 11
- **Sub-Issue Range**: #130 - #243

### Breakdown by Feature

| Feature | Sub-Issues | Range |
|---------|-----------|-------|
| FR #7 - Member Management | 35 | #130 - #164 |
| FR #8 - Campaign & Email | 24 | #165 - #188 |
| FR #9 - Learning Management | 19 | #189 - #207 |
| FR #10 - Advanced Reporting | 19 | #208 - #226 |
| FR #11 - Event Management | 17 | #227 - #243 |

## Customization

To customize the generated issues:

1. Edit `scripts/generate_feature_issues.py`
2. Modify the feature request definitions or sub-issue lists
3. Re-run: `python scripts/generate_feature_issues.py`
4. Review changes in `github_issues.json` and `github_issues_summary.md`

## Troubleshooting

### GitHub CLI Not Installed

```bash
# macOS
brew install gh

# Ubuntu/Debian
sudo apt install gh

# Windows
winget install --id GitHub.cli
```

### Authentication Issues

```bash
gh auth login
gh auth status
```

### Rate Limiting

If you hit GitHub's rate limit, the script includes 1-second delays between issue creation. If issues persist:

1. Wait for rate limit to reset (check: `gh api rate_limit`)
2. Create issues in smaller batches
3. Use a GitHub token with higher rate limits

### Permission Issues

Ensure your GitHub account has permission to create issues in the target repository:

```bash
gh repo view markus41/portfolio
```

## Integration with Project Board

After creating issues, they can be organized on the GitHub Project board:

1. Navigate to: https://github.com/users/markus41/projects/22
2. Add the issues to the project
3. Organize by labels: `feature-7`, `feature-8`, etc.
4. Set up automation rules for issue status tracking

See `PROJECT_BOARD_SETUP.md` for detailed instructions.

## Next Steps

1. Create the issues using one of the methods above
2. Assign team members to specific issues based on agent assignments
3. Set up milestones for each feature request
4. Configure project board automation
5. Begin implementation following the issue priorities

## Support

For questions or issues with the scripts:

1. Check this documentation
2. Review the generated `github_issues_summary.md`
3. Open an issue using the Question template
4. Contact the project maintainers
