# NABIP Super Menu & Content Integration - Issue Creation Guide

This document explains the approach and tools for creating GitHub issues for the NABIP website integration features.

## Overview

This solution automates the creation of GitHub issues for three major feature requests and their 99 sub-issues:

- **Feature Request #12**: NABIP Super Menu & Content Integration (84 sub-issues)
- **Feature Request #13**: Committee & Volunteer Management (7 sub-issues)
- **Feature Request #14**: Financial & Commerce Platform (8 sub-issues)

## Files Created

### 1. `scripts/nabip_issues_config.json`
A comprehensive JSON configuration file containing all feature requests and sub-issues with:
- Feature descriptions and problem statements
- Proposed solutions and alternatives
- Expected impact and priorities
- Technical considerations
- Sub-issue details with recommended custom GitHub agents
- Appropriate labels for organization

### 2. `scripts/create_nabip_issues.py`
A Python script that reads the configuration and creates GitHub issues using the GitHub CLI (`gh`).

## GitHub Custom Agents Mapping

The configuration includes recommended custom GitHub agents for each sub-issue. These agents are specialized for specific tasks:

### Content & Documentation Agents
- **content-agent**: General content creation and management
- **documentation-agent**: Technical and user documentation
- **blog-agent**: Blog posts and article management

### Frontend & UI Agents
- **frontend-agent**: General frontend development
- **ux-agent**: User experience and interaction design
- **design-agent**: Visual design and styling
- **mobile-agent**: Mobile-responsive development
- **animation-agent**: CSS animations and transitions

### Search & Discovery Agents
- **search-agent**: Search functionality implementation
- **recommendation-agent**: Recommendation systems

### Data & Integration Agents
- **cms-agent**: Content management system integration
- **integration-agent**: Third-party integrations
- **directory-agent**: Directory and listing management
- **database-agent**: Database operations

### Specialized Domain Agents
- **payment-agent**: Payment processing and financial transactions
- **auth-agent**: Authentication and authorization
- **workflow-agent**: Business workflow automation
- **forms-agent**: Form creation and handling
- **calendar-agent**: Calendar and scheduling
- **events-agent**: Event management
- **education-agent**: Educational content and courses

### Media & Assets Agents
- **media-agent**: Media file management
- **pdf-agent**: PDF generation and handling
- **asset-agent**: Digital asset management
- **archive-agent**: Archive and historical data

### Analytics & Reporting Agents
- **analytics-agent**: Analytics and metrics
- **reporting-agent**: Report generation
- **tracking-agent**: Progress and activity tracking
- **visualization-agent**: Data visualization

### Specialized Features Agents
- **maps-agent**: Interactive maps
- **survey-agent**: Survey creation and analysis
- **jobs-agent**: Job board functionality
- **cart-agent**: Shopping cart functionality
- **compliance-agent**: Compliance and regulatory features

### Management & Admin Agents
- **portal-agent**: Member portals and dashboards
- **dashboard-agent**: Administrative dashboards
- **volunteer-agent**: Volunteer management
- **committee-agent**: Committee management

### Support & Communication Agents
- **support-agent**: Customer support features
- **notification-agent**: Notification systems
- **advocacy-agent**: Advocacy tools and campaigns

### Automation & Tools Agents
- **automation-agent**: Workflow automation
- **tools-agent**: Utility tools
- **template-agent**: Template management
- **approval-agent**: Approval workflows

## Usage

### Prerequisites

1. **GitHub CLI**: Install and authenticate the GitHub CLI tool
   ```bash
   # Install GitHub CLI (if not already installed)
   # macOS: brew install gh
   # Linux: See https://github.com/cli/cli/blob/trunk/docs/install_linux.md
   # Windows: See https://github.com/cli/cli#windows
   
   # Authenticate with GitHub
   gh auth login
   ```

2. **Repository Access**: You must have write access to the repository to create issues.

### Preview Issues (Dry Run)

Before creating issues, you can preview them:

```bash
cd /home/runner/work/portfolio/portfolio
python scripts/create_nabip_issues.py --dry-run
```

This will display all issues that would be created without actually creating them.

### Create Issues

To create all issues in the GitHub repository:

```bash
cd /home/runner/work/portfolio/portfolio
python scripts/create_nabip_issues.py
```

The script will:
1. Check for GitHub CLI installation and authentication
2. Load the configuration from `nabip_issues_config.json`
3. Create each feature request issue
4. Create all sub-issues for each feature
5. Apply appropriate labels to each issue
6. Display progress and confirmation

### Custom Configuration

You can specify a different configuration file:

```bash
python scripts/create_nabip_issues.py --config path/to/custom_config.json
```

## Issue Structure

### Feature Request Issues

Each feature request issue contains:
- **Title**: `[Feature #N]: Feature Name`
- **Description**: Detailed problem statement and proposed solution
- **Category**: Feature category classification
- **Alternatives**: Alternative approaches considered
- **Expected Impact**: Priority, estimated time, and impact assessment
- **Technical Considerations**: Technical requirements and constraints
- **Sub-Issues**: List of related sub-issues

### Sub-Issues

Each sub-issue contains:
- **Title**: `[Sub-Issue #N]: Issue Title`
- **Section**: The NABIP section this issue belongs to
- **Parent Feature**: Reference to parent feature request
- **Description**: Detailed description of the task
- **Recommended Agents**: List of suggested custom GitHub agents
- **Labels**: Categorization labels

## Issue Labels

Issues are tagged with appropriate labels:

### Feature Request Labels
- `enhancement`: All feature requests
- `navigation`: Navigation-related features
- `content-management`: CMS and content features
- `mega-menu`: Mega-menu specific features
- `committee-management`: Committee management features
- `collaboration`: Collaboration features
- `ecommerce`: E-commerce features
- `payment`: Payment processing features

### Sub-Issue Labels
- `enhancement`: General improvements
- `frontend`: Frontend development
- `backend`: Backend development
- `search`: Search functionality
- `content`: Content creation/management
- `documentation`: Documentation work
- `cms`: CMS integration
- `authentication`: Auth features
- `payment`: Payment features
- `calendar`: Calendar features
- `forms`: Form features
- `portal`: Portal development
- `mobile`: Mobile features
- `accessibility`: Accessibility improvements
- `security`: Security features
- And many more domain-specific labels

## Assigning Issues to Custom Agents

After issues are created, you can assign them to the recommended custom agents:

1. **Manual Assignment**: Use GitHub's interface to assign issues based on the "Recommended Custom Agents" section in each issue.

2. **Automated Assignment**: You can extend the script to automatically assign issues using the GitHub API:
   ```python
   # Example (not implemented in current script)
   gh issue edit <issue-number> --add-assignee <agent-username>
   ```

3. **Project Board Organization**: Create a GitHub Project board and organize issues by:
   - Feature category
   - Priority
   - Assigned agent
   - Status (To Do, In Progress, Done)

## Project Board Setup

Follow these steps to organize the issues:

1. **Create Project Board**: Go to the repository's Projects tab and create a new project board.

2. **Add Views**:
   - By Feature (group by parent feature)
   - By Agent (group by assigned custom agent)
   - By Priority (group by priority level)
   - By Section (group by NABIP section)

3. **Set Up Automation**:
   - Auto-add new issues to project
   - Move issues to "Done" when closed
   - Link pull requests to issues

## Extending the Configuration

To add more issues or modify existing ones:

1. Edit `scripts/nabip_issues_config.json`
2. Follow the existing JSON structure
3. Add or modify feature requests and sub-issues
4. Run the script with `--dry-run` to preview changes
5. Run the script to create new issues

## Best Practices

1. **Start with Dry Run**: Always preview with `--dry-run` before creating issues
2. **Batch Creation**: Create all issues at once for consistency
3. **Issue Numbering**: The script includes issue numbers in titles for easy reference
4. **Label Consistency**: Use consistent labels across related issues
5. **Agent Assignment**: Assign issues to agents based on their expertise
6. **Regular Updates**: Update issue status and progress regularly
7. **Link Dependencies**: Use GitHub's issue linking to connect related issues

## Troubleshooting

### GitHub CLI Not Found
```
✗ GitHub CLI not found or not authenticated
```
**Solution**: Install GitHub CLI from https://cli.github.com/ and run `gh auth login`

### Authentication Failed
```
✗ Failed to create issue: authentication required
```
**Solution**: Run `gh auth login` to authenticate with GitHub

### Rate Limiting
If you hit GitHub API rate limits:
- Wait for the rate limit to reset (usually 1 hour)
- Consider creating issues in smaller batches
- Check your rate limit: `gh api rate_limit`

### Invalid JSON Configuration
```
✗ Invalid JSON in configuration file
```
**Solution**: Validate your JSON using a JSON validator or linter

## Summary

This solution provides a comprehensive, automated approach to creating and organizing the NABIP website integration issues. The configuration-driven approach makes it easy to:

- Maintain a clear overview of all features and sub-issues
- Assign work to specialized custom agents
- Track progress using GitHub's native features
- Scale to additional features in the future

## Next Steps

1. Review the configuration file to ensure all details are accurate
2. Run the script in dry-run mode to preview issues
3. Create the issues in GitHub
4. Set up a project board for tracking
5. Assign issues to appropriate custom agents
6. Begin implementation following the defined priorities

---

For questions or issues with this tooling, please create an issue in the repository.
