# NABIP Custom GitHub Agents Quick Reference

This document provides a quick reference for all custom GitHub agents recommended for the NABIP project issues.

## Agent Categories

### 🎨 Frontend & UI Development
| Agent | Expertise | Example Tasks |
|-------|-----------|---------------|
| `frontend-agent` | General frontend development | React components, UI implementation |
| `ux-agent` | User experience design | User flows, interaction design |
| `design-agent` | Visual design | UI mockups, style guides |
| `mobile-agent` | Mobile responsiveness | Mobile layouts, touch interfaces |
| `animation-agent` | CSS animations | Transitions, effects, micro-interactions |
| `accessibility-agent` | A11y compliance | ARIA, keyboard navigation, screen readers |

### 📝 Content & Documentation
| Agent | Expertise | Example Tasks |
|-------|-----------|---------------|
| `content-agent` | Content creation | Writing, editing, content strategy |
| `documentation-agent` | Technical docs | API docs, user guides, tutorials |
| `blog-agent` | Blog management | Posts, articles, content calendars |
| `library-agent` | Content libraries | Resource organization, curation |

### 🔍 Search & Discovery
| Agent | Expertise | Example Tasks |
|-------|-----------|---------------|
| `search-agent` | Search functionality | Elasticsearch, filters, facets |
| `recommendation-agent` | Recommendation engines | Personalization, suggestions |

### 💳 Payment & Commerce
| Agent | Expertise | Example Tasks |
|-------|-----------|---------------|
| `payment-agent` | Payment processing | Stripe, payment gateways |
| `cart-agent` | Shopping cart | Cart logic, checkout flows |
| `invoice-agent` | Invoicing | Invoice generation, payment tracking |
| `discount-agent` | Discount systems | Pricing rules, promotions |
| `promo-agent` | Promo codes | Code validation, usage limits |
| `recurring-agent` | Subscriptions | Auto-renewal, recurring billing |
| `payment-plan-agent` | Installments | Payment plans, schedules |
| `gift-agent` | Gift purchases | Gift memberships, gift cards |
| `expense-agent` | Expenses | Reimbursements, expense tracking |

### 🔗 Integration & APIs
| Agent | Expertise | Example Tasks |
|-------|-----------|---------------|
| `integration-agent` | Third-party integrations | API connections, webhooks |
| `api-agent` | API development | REST APIs, GraphQL |
| `webhook-agent` | Webhook handling | Event processing, callbacks |
| `sync-agent` | Data synchronization | Real-time sync, batch updates |

### 🎓 Education & Training
| Agent | Expertise | Example Tasks |
|-------|-----------|---------------|
| `education-agent` | Online learning | LMS integration, courses |
| `certification-agent` | Certifications | Exams, certificates, tracking |
| `training-agent` | Training programs | Training modules, content |

### 📅 Events & Calendar
| Agent | Expertise | Example Tasks |
|-------|-----------|---------------|
| `events-agent` | Event management | Event listings, registration |
| `calendar-agent` | Calendar systems | Calendar integration, iCal |
| `scheduling-agent` | Meeting scheduling | Polls, availability, booking |
| `registration-agent` | Event registration | Sign-ups, attendee management |

### 📚 CMS & Content Management
| Agent | Expertise | Example Tasks |
|-------|-----------|---------------|
| `cms-agent` | CMS integration | Content editing, workflows |
| `asset-agent` | Digital assets | Media library, asset management |
| `media-agent` | Media handling | Video, audio, images |
| `pdf-agent` | PDF generation | Reports, documents, downloads |
| `archive-agent` | Archives | Historical data, backups |

### 📊 Analytics & Reporting
| Agent | Expertise | Example Tasks |
|-------|-----------|---------------|
| `analytics-agent` | Analytics | Metrics, dashboards, insights |
| `reporting-agent` | Report generation | Custom reports, exports |
| `tracking-agent` | Activity tracking | User behavior, progress tracking |
| `visualization-agent` | Data visualization | Charts, graphs, dashboards |

### ⚙️ Workflow & Automation
| Agent | Expertise | Example Tasks |
|-------|-----------|---------------|
| `workflow-agent` | Business workflows | Process automation, flows |
| `automation-agent` | Task automation | Scheduled tasks, triggers |
| `approval-agent` | Approval processes | Review workflows, permissions |
| `task-agent` | Task management | To-do lists, assignments |
| `forms-agent` | Form handling | Form builder, submissions |

### 📖 Directory & Listings
| Agent | Expertise | Example Tasks |
|-------|-----------|---------------|
| `directory-agent` | Directory systems | Member directories, listings |
| `jobs-agent` | Job boards | Job postings, applications |
| `matching-agent` | Matching algorithms | Mentor matching, recommendations |

### 🏢 Portal & Dashboard
| Agent | Expertise | Example Tasks |
|-------|-----------|---------------|
| `portal-agent` | Member portals | Dashboards, personalized views |
| `dashboard-agent` | Admin dashboards | Management interfaces, controls |
| `membership-agent` | Membership systems | Member data, benefits |

### 🎯 Specialized Domains
| Agent | Expertise | Example Tasks |
|-------|-----------|---------------|
| `maps-agent` | Interactive maps | Geographic visualization, locations |
| `survey-agent` | Surveys | Survey creation, response analysis |
| `compliance-agent` | Compliance | Regulatory requirements, audits |
| `advocacy-agent` | Advocacy tools | Campaign tools, outreach |
| `volunteer-agent` | Volunteer management | Hour logging, volunteer tracking |
| `medicare-agent` | Medicare-specific | Medicare plans, compliance |
| `donation-agent` | Donations | Donation processing, receipts |
| `foundation-agent` | Foundation management | Grants, scholarships |
| `calculator-agent` | Calculators | ROI calculators, pricing tools |
| `tools-agent` | Utility tools | Helper utilities, generators |
| `template-agent` | Templates | Document templates, generators |

### 🔐 Security & Authentication
| Agent | Expertise | Example Tasks |
|-------|-----------|---------------|
| `auth-agent` | Authentication | Login, SSO, OAuth |
| `security-agent` | Security | Vulnerability scanning, encryption |

### 📢 Support & Communication
| Agent | Expertise | Example Tasks |
|-------|-----------|---------------|
| `support-agent` | Customer support | Help desk, tickets |
| `notification-agent` | Notifications | Email, SMS, push notifications |
| `email-agent` | Email systems | Email templates, campaigns |

### 🏗️ Specialized Features
| Agent | Expertise | Example Tasks |
|-------|-----------|---------------|
| `feed-agent` | RSS/News feeds | Content aggregation, syndication |
| `showcase-agent` | Showcases | Galleries, featured content |
| `collaboration-agent` | Real-time collaboration | Document editing, comments |
| `document-agent` | Document management | Version control, sharing |
| `committee-agent` | Committee management | Committee portals, meetings |

## Assignment Guidelines

### High Priority Agents
These agents should be assigned first as they handle critical functionality:
- `payment-agent` - All payment-related issues
- `auth-agent` - Authentication and security
- `frontend-agent` - Core UI development
- `search-agent` - Search functionality

### Cross-Functional Agents
These agents often work together:
- `frontend-agent` + `backend-agent` - Full-stack features
- `content-agent` + `cms-agent` - Content management
- `payment-agent` + `cart-agent` - E-commerce features
- `events-agent` + `calendar-agent` - Event management

### Specialized Agents
Assign these for domain-specific work:
- `medicare-agent` - Medicare-specific features only
- `compliance-agent` - Regulatory and compliance features
- `advocacy-agent` - Advocacy and campaign tools
- `volunteer-agent` - Volunteer management features

## Usage in Issues

Each sub-issue in the configuration includes a "Recommended Custom Agents" section:

```markdown
### Recommended Custom Agents
- `frontend-agent`
- `search-agent`
```

Use these recommendations when:
1. Assigning issues to team members
2. Requesting specialized expertise
3. Planning sprint capacity
4. Estimating effort

## Notes

- Most issues require 1-2 agents
- Complex features may need 3+ agents
- Agents can be re-assigned if recommendations don't fit
- New specialized agents can be created as needed
- Agent names are suggestions - adapt to your team structure

## Quick Assignment Commands

Using GitHub CLI:
```bash
# Assign single issue
gh issue edit 244 --add-assignee @frontend-agent

# Assign multiple issues
gh issue list --label "search" --json number --jq '.[].number' | \
  xargs -I {} gh issue edit {} --add-assignee @search-agent
```

## Finding Issues by Agent

To find all issues for a specific agent type:
```bash
# Search issue descriptions for agent recommendations
gh issue list --search "frontend-agent" --json number,title,labels

# Filter by label
gh issue list --label "frontend" --json number,title
```

---

**Total Agents**: 60+  
**Categories**: 15  
**Coverage**: All 99 sub-issues mapped to appropriate agents
