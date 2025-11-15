# Feature Requests and Sub-Issues Overview

This document provides an overview of all feature requests and their sub-issues.

## Available Agent Types

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

---

## Feature Request #4: Document Distribution & Management System

**Hierarchical Document Distribution with OCR and Approval Workflows**

**Category:** Document Management/Navigation Enhancement

**Priority:** High

### Problem Statement

No system for distributing documents throughout the organization hierarchy. Cannot target documents to specific chapters, states, or nationwide. No OCR capability, no approval workflows, and no tracking of who viewed or downloaded documents.

### Proposed Solution

Build hierarchical document upload wizard with distribution targeting (all CA chapters, all state chapters, specific chapters), OCR integration for scanning paper documents, multi-stage approval workflow, view/download tracking, searchable document library with filters.

### Alternatives Considered

- Using Google Drive/SharePoint (lacks hierarchy targeting)
- Simple file upload (no tracking or workflow)
- Email-based distribution (no centralization)

### Expected Impact

High priority - Critical for organizational communication. Affects all admins and members. Estimated time: 5-6 weeks. Ensures consistent document distribution and compliance.

### Technical Considerations

OCR service integration (AWS Textract or Google Vision), S3/Azure Blob storage, CDN for delivery, document encryption, elasticsearch for search.

### Sub-Issues (13 total)

#### Issue #37: Build Hierarchical Document Upload Wizard

Create multi-step wizard for uploading documents. Step 1: Upload file. Step 2: Add metadata (title, description, category). Step 3: Select distribution targets. Step 4: Set permissions. Step 5: Review and publish.

**Labels:** enhancement, frontend, backend

**Suggested Agents:** Full-Stack Development Agent, UX/UI Design Agent

**Estimate:** 1 week

---

#### Issue #38: Add Distribution Targeting

Implement targeting options: All chapters nationwide, All chapters in specific state(s), Specific chapters only, Specific member segments, Leadership only. Allow combining multiple targeting rules.

**Labels:** enhancement, backend

**Suggested Agents:** Backend Development Agent, Database Agent

**Estimate:** 1 week

---

#### Issue #39: Implement Document Scanning/OCR Integration

Integrate with AWS Textract or Google Vision API to scan uploaded PDFs and images, extract text content, make documents searchable, and enable text selection in scanned documents.

**Labels:** enhancement, backend, ml

**Suggested Agents:** Backend Development Agent, Machine Learning Agent

**Estimate:** 1-2 weeks

---

#### Issue #40: Create Multi-Stage Approval Workflow

Build approval workflow where documents require approval before distribution. Route to appropriate approver based on distribution target (chapter docs to state admin, state docs to national admin). Track approval status and send notifications.

**Labels:** enhancement, backend

**Suggested Agents:** Backend Development Agent, Full-Stack Development Agent

**Estimate:** 1-2 weeks

---

#### Issue #41: Add Document View/Download Tracking

Track every time a document is viewed or downloaded. Record user, timestamp, document, and action. Provide analytics showing which documents are most accessed, who has/hasn't viewed required documents.

**Labels:** enhancement, backend, analytics

**Suggested Agents:** Backend Development Agent, Database Agent

**Estimate:** 1 week

---

#### Issue #42: Build Searchable Document Library

Create document library with full-text search, filters by category, date, chapter, document type, and tags. Show search results with highlighted search terms and relevance ranking.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent, Backend Development Agent

**Estimate:** 1-2 weeks

---

#### Issue #43: Create Resource Library with Categories

Organize documents into categories and subcategories (Policies, Forms, Templates, Guides, Compliance, Marketing). Add tags for cross-category discovery and create featured/recommended sections.

**Labels:** enhancement, frontend, backend

**Suggested Agents:** Full-Stack Development Agent, UX/UI Design Agent

**Estimate:** 1 week

---

#### Issue #44: Implement Document Version Control

Track document versions, allow viewing previous versions, show what changed between versions, enable reverting to previous version, and maintain complete version history with change descriptions.

**Labels:** enhancement, backend

**Suggested Agents:** Backend Development Agent, Database Agent

**Estimate:** 1 week

---

#### Issue #45: Add Video Content Library

Integrate video streaming capability for training videos, webinar recordings, and educational content. Support multiple video formats, add video player with playback controls, and track video viewing completion.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent, Backend Development Agent

**Estimate:** 1-2 weeks

---

#### Issue #46: Integrate Podcast Player

Add podcast player for NABIP podcast episodes. Include playlist functionality, playback speed control, show notes display, and subscribe to podcast feed.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent, Full-Stack Development Agent

**Estimate:** 1 week

---

#### Issue #47: Build Blog/News Article System

Create blog system for publishing news, updates, and articles. Include rich text editor, image upload, categories, tags, commenting system, and RSS feed for subscriptions.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent, Backend Development Agent

**Estimate:** 1-2 weeks

---

#### Issue #48: Create FAQ Management System

Build FAQ system with categories, search functionality, most viewed questions, related questions suggestions, and ability for members to submit new questions.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent, Backend Development Agent

**Estimate:** 1 week

---

#### Issue #49: Add Knowledge Base with Search

Create comprehensive knowledge base with articles, how-to guides, troubleshooting docs, and best practices. Include full-text search, breadcrumb navigation, related articles, and helpful/not helpful voting.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent, Backend Development Agent

**Estimate:** 1-2 weeks

---


## Feature Request #5: Dashboard & Analytics Platform

**Customizable Dashboard with Advanced Analytics and Drill-Through**

**Category:** Analytics/Dashboard Enhancement

**Priority:** Medium-High

### Problem Statement

Dashboard has poor UX: vertical bar charts should be horizontal, no data labels, non-clickable elements, no period comparisons, default colors instead of NABIP branding, and no customization options. Users cannot drill down into data or export.

### Proposed Solution

Redesign dashboard with horizontal bar charts, direct data labels, clickable drill-through on all elements, period comparison toggles (YoY, MoM, QoQ), drag-and-drop widget customization, NABIP brand colors throughout, export functionality.

### Alternatives Considered

- Fixed dashboard layout (not flexible)
- Third-party BI tool (adds cost)
- Simple static charts (doesn't support analysis)

### Expected Impact

Medium-high priority. Affects all admin users. Estimated time: 4-5 weeks. Increases data-driven decision making.

### Technical Considerations

Chart.js or Recharts for visualizations, WebSockets for real-time updates, caching for queries, user preference storage, potential data warehouse for analytics.

### Sub-Issues (37 total)

#### Issue #50: Redesign Revenue Chart to Horizontal Bars

Convert the vertical revenue bar chart to horizontal bars with categories on left and values extending right. This makes category labels more readable and follows better data visualization practices.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent, UX/UI Design Agent

**Estimate:** 2-3 days

---

#### Issue #51: Add Data Labels Directly on Chart Bars

Display the actual dollar amounts directly on or next to each bar in revenue chart instead of requiring users to hover or reference axis. Makes data immediately readable at a glance.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent

**Estimate:** 1-2 days

---

#### Issue #52: Make All Dashboard Elements Clickable

Add click handlers to all dashboard widgets, charts, and metrics. Clicking should drill down to detailed view. For example, clicking revenue chart bar shows transaction details for that category.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent

**Estimate:** 3-4 days

---

#### Issue #53: Add Period Comparison Toggles

Add toggles to all dashboard widgets for Year-over-Year, Month-over-Month, and Quarter-over-Quarter comparisons. Show comparison values and percentage change with up/down indicators.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent, Backend Development Agent

**Estimate:** 1 week

---

#### Issue #54: Implement Dashboard Customization

Add 'Edit Dashboard' mode where users can drag-and-drop widgets to rearrange, resize widgets, add/remove widgets from library, and save custom layouts per user.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent, Frontend Development Agent

**Estimate:** 1-2 weeks

---

#### Issue #55: Add Export Functionality

Add export button to dashboard and individual widgets. Allow exporting to CSV for data, Excel for formatted reports, and PDF for presentations. Maintain chart formatting in exports.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent, Backend Development Agent

**Estimate:** 1 week

---

#### Issue #56: Add More Chart Type Options

Expand beyond bar charts to include line charts for trends, area charts for cumulative data, scatter plots for correlations, pie charts for proportions, and combo charts mixing types.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent

**Estimate:** 1 week

---

#### Issue #57: Implement Interactive Tooltips

Add detailed tooltips on chart hover showing exact values, percentages, comparison to previous period, and trend indicators. Make tooltips appear quickly and be easy to read.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent

**Estimate:** 3-4 days

---

#### Issue #58: Add Data Export from Individual Charts

Allow exporting data from individual charts without exporting entire dashboard. Click export icon on chart to get just that chart's data in chosen format.

**Labels:** enhancement, frontend, backend

**Suggested Agents:** Full-Stack Development Agent

**Estimate:** 3-4 days

---

#### Issue #59: Create Comparison Views

Build comparison mode for viewing multiple metrics side-by-side. Select 2-4 metrics to compare across same time period and see correlations and patterns.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent

**Estimate:** 1 week

---

#### Issue #60: Build Trend Analysis Tools

Add trend lines to time-series charts, show moving averages, highlight anomalies, predict future trends based on historical data, and show confidence intervals.

**Labels:** enhancement, backend, ml

**Suggested Agents:** Backend Development Agent, Machine Learning Agent

**Estimate:** 1-2 weeks

---

#### Issue #61: Add Revenue Percentage Breakdown

Show revenue breakdown as both dollar amounts and percentages. Display what percent each category contributes to total revenue for better proportion understanding.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent

**Estimate:** 2-3 days

---

#### Issue #62: Implement Date Range Selector

Replace hardcoded 'This Month' with actual date range selector. Allow selecting preset ranges (Today, This Week, This Month, This Quarter, This Year) or custom date ranges.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent

**Estimate:** 3-4 days

---

#### Issue #63: Make Revenue Categories Clickable

When clicking a revenue category, show detailed transaction list for that category. Include filtering, sorting, and export of transaction details.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent

**Estimate:** 1 week

---

#### Issue #64: Add YoY and MoM Comparison Indicators

Show Year-over-Year and Month-over-Month comparisons with trend arrows (↑ for increase, ↓ for decrease) and color coding (green for positive, red for negative) based on context.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent

**Estimate:** 2-3 days

---

#### Issue #65: Add Revenue Data Export

Add dedicated export button for revenue data with options for different formats and date ranges. Include all revenue categories and comparison data in export.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent

**Estimate:** 3-4 days

---

#### Issue #66: Build Refund History Tracking

In the refund modal, add complete refund history showing all refunds issued, amounts, reasons, dates, processed by whom, and original transaction details.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent, Backend Development Agent

**Estimate:** 3-4 days

---

#### Issue #67: Add Personalization Options to Greeting

Allow users to customize dashboard greeting, choose whether to show it, set preferred name format, and personalize which widgets appear above the fold.

**Labels:** enhancement, frontend, backend

**Suggested Agents:** Full-Stack Development Agent

**Estimate:** 3-4 days

---

#### Issue #68: Use Specific Icons for Alert Types

Replace generic warning icon with specific icons for different alert types: exclamation for urgent, info icon for FYI, calendar for upcoming deadlines, dollar sign for financial alerts.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent, UX/UI Design Agent

**Estimate:** 1-2 days

---

#### Issue #69: Add Registration CTAs to Event Progress Bars

In upcoming events widget, add 'Register Now' or 'View Details' buttons directly on event cards. Show registration progress bar and spots remaining.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent

**Estimate:** 2-3 days

---

#### Issue #70: Improve Email Engagement Visual Hierarchy

Redesign email engagement metrics section with better visual hierarchy. Use size to show importance, color to show performance, and clear labels for each metric.

**Labels:** enhancement, frontend, ux

**Suggested Agents:** Frontend Development Agent, UX/UI Design Agent

**Estimate:** 2-3 days

---

#### Issue #71: Add Quick Access to Active Campaigns

Make the 'Active Campaigns' count clickable to jump directly to campaign list. Add preview of most recent campaigns with quick action buttons (View, Edit, Clone).

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent

**Estimate:** 3-4 days

---

#### Issue #72: Apply NABIP Brand Colors Consistently

Update all charts and dashboard elements to use NABIP brand colors (Navy #003366, Teal #008B8B, Gold #FFD700). Create color scheme for different data types that aligns with brand.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent, UX/UI Design Agent

**Estimate:** 2-3 days

---

#### Issue #73: Add Edit Dashboard Mode

Create 'Edit Dashboard' toggle that enters edit mode where users can drag widgets to reorder, click X to remove widgets, and add new widgets from a widget library.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent, Full-Stack Development Agent

**Estimate:** 1 week

---

#### Issue #74: Create Widget Library

Build library of available dashboard widgets (revenue, events, members, campaigns, courses, etc.). Allow users to browse and add widgets to their dashboard with preview before adding.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent

**Estimate:** 1 week

---

#### Issue #75: Save Custom Dashboard Layouts

Allow users to save their custom dashboard layout preferences. Store widget positions, sizes, which widgets are shown/hidden, and apply automatically on login.

**Labels:** enhancement, backend

**Suggested Agents:** Backend Development Agent, Database Agent

**Estimate:** 3-4 days

---

#### Issue #76: Set Default Dashboard View

Let users set which dashboard layout is their default. Provide system default layouts (Executive View, Operations View, Financial View) plus ability to create custom defaults.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent

**Estimate:** 3-4 days

---

#### Issue #77: Add Widget Size Options

Allow resizing widgets to small (1x1 grid), medium (2x1), large (2x2), or full-width. Widgets should reflow responsively based on screen size.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent

**Estimate:** 3-4 days

---

#### Issue #78: Include Widget Settings Panel

Add settings icon to each widget opening configuration panel. Allow customizing widget-specific settings like date range, metrics shown, chart type, refresh frequency.

**Labels:** enhancement, frontend, backend

**Suggested Agents:** Full-Stack Development Agent

**Estimate:** 1 week

---

#### Issue #79: Add Member Journey Visualization

Create visual timeline showing typical member journey from join → attend event → take course → renew. Show conversion rates at each stage and identify drop-off points.

**Labels:** enhancement, fullstack, analytics

**Suggested Agents:** Full-Stack Development Agent, Backend Development Agent

**Estimate:** 1-2 weeks

---

#### Issue #80: Implement Predictive Churn Analysis

Use machine learning to predict which members are at risk of not renewing. Show churn risk score, contributing factors, and recommended retention actions.

**Labels:** enhancement, ml, backend

**Suggested Agents:** Machine Learning Agent, Backend Development Agent

**Estimate:** 2-3 weeks

---

#### Issue #81: Create Event ROI Calculator

Build calculator showing event costs vs revenue and member engagement value. Include attendee count, ticket revenue, sponsor revenue, costs, and net ROI with benchmarks.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent, Backend Development Agent

**Estimate:** 1 week

---

#### Issue #82: Build Chapter Benchmarking Tools

Allow comparing any chapter against state averages, national averages, or peer chapters of similar size. Show where they excel and where they need improvement.

**Labels:** enhancement, fullstack, analytics

**Suggested Agents:** Full-Stack Development Agent, Backend Development Agent

**Estimate:** 1-2 weeks

---

#### Issue #83: Add Engagement Heat Maps

Create heat map visualizations showing when members are most active (time of day, day of week, month of year). Use this to optimize event scheduling and email send times.

**Labels:** enhancement, frontend, analytics

**Suggested Agents:** Frontend Development Agent, Backend Development Agent

**Estimate:** 1 week

---

#### Issue #84: Implement Cohort Analysis

Analyze member retention by cohort (members who joined in same month/year). Show retention curves and identify which cohorts have best/worst retention for targeting improvements.

**Labels:** enhancement, backend, analytics

**Suggested Agents:** Backend Development Agent, Machine Learning Agent

**Estimate:** 1-2 weeks

---

#### Issue #85: Create Custom Dashboard Builder

Build advanced dashboard builder where power users can create completely custom dashboards with drag-and-drop widgets, custom metrics, SQL-like queries, and share with team.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent, Backend Development Agent

**Estimate:** 2-3 weeks

---

#### Issue #86: Add Automated Insights with AI

Use AI to automatically surface interesting insights from data like 'Member signups increased 32% this month' or 'Houston chapter has 80% higher engagement than average' proactively.

**Labels:** enhancement, ml, backend

**Suggested Agents:** Machine Learning Agent, Backend Development Agent

**Estimate:** 2-3 weeks

---


## Feature Request #6: Navigation & User Experience Overhaul

**Enhanced Navigation with AI Search and Quick Access**

**Category:** Navigation/UX Enhancement

**Priority:** High

### Problem Statement

Current navigation is limited: search bar too narrow, no AI-powered search, missing breadcrumbs, no user profile dropdown, no notifications, and no quick access menu. Users struggle to find features and navigate efficiently.

### Proposed Solution

Expand search bar to 400px with AI natural language search, implement breadcrumbs throughout, add user profile/settings dropdown, include notification bell with count, add Cmd/Ctrl+K command palette, enhance sidebar with badges/counts/sub-menus, add recently accessed items.

### Alternatives Considered

- Keeping simple navigation (doesn't scale)
- Multiple navigation patterns (inconsistent UX)
- Search-only interface (too radical)

### Expected Impact

High priority. Affects all users. Estimated time: 3-4 weeks. Reduces time to find features by ~80%.

### Technical Considerations

Algolia or Elasticsearch for search, AI/LLM integration for natural language, user preference storage, keyboard shortcut system, analytics tracking.

### Sub-Issues (43 total)

#### Issue #87: Expand Search Bar to 400px Width

Increase the header search bar from its current narrow width to minimum 400px. This makes it more prominent and easier to type longer search queries without horizontal scrolling.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent, UX/UI Design Agent

**Estimate:** 1 day

---

#### Issue #88: Add AI-Powered Search

Integrate AI natural language processing so users can search with phrases like 'show me all members in California who joined this year' instead of having to use specific filter syntax.

**Labels:** enhancement, backend, ml

**Suggested Agents:** Machine Learning Agent, Backend Development Agent

**Estimate:** 2-3 weeks

---

#### Issue #89: Implement Breadcrumb Navigation

Add breadcrumb navigation below header showing current location in site hierarchy. For example: 'Home > Chapters > California > Los Angeles Chapter > Members' with each level clickable.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent

**Estimate:** 3-4 days

---

#### Issue #90: Add User Profile/Settings Dropdown

Add user profile icon in top right that opens dropdown menu with options like My Profile, Account Settings, Preferences, Help, and Logout. Show user name and role.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent

**Estimate:** 2-3 days

---

#### Issue #91: Include Notification Bell with Count

Add notification bell icon in header that shows count badge for unread notifications. Clicking opens dropdown with recent notifications and link to view all.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent

**Estimate:** 1 week

---

#### Issue #92: Add Quick Access Menu

Create quick access menu (like bookmarks) where users can pin frequently used pages/features for one-click access. Allow customizing which items appear in quick access.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent

**Estimate:** 1 week

---

#### Issue #93: Add Notification Badges to Sidebar

Show notification badges (red dots or numbers) on sidebar items that have pending actions. For example, show '5' on Members if 5 new member applications are pending approval.

**Labels:** enhancement, frontend, backend

**Suggested Agents:** Full-Stack Development Agent

**Estimate:** 3-4 days

---

#### Issue #94: Show Counts in Sidebar

Display actual counts next to sidebar items like 'Members (1,247)' and 'Events (23)' so users know how many items exist in each section without clicking.

**Labels:** enhancement, backend

**Suggested Agents:** Backend Development Agent

**Estimate:** 2-3 days

---

#### Issue #95: Add Expandable Sub-Menus to Sidebar

Make sidebar items expandable with arrow icons. Clicking Members expands to show 'All Members', 'Pending Approvals', 'Lapsed Members' etc. without leaving current page.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent

**Estimate:** 3-4 days

---

#### Issue #96: Include Recently Accessed Items

Add 'Recent' section at top of sidebar showing last 5 pages/items user accessed for quick return. Auto-updates as user navigates around the system.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent

**Estimate:** 3-4 days

---

#### Issue #97: Add Quick Stats/KPIs Per Section

Show mini stats in sidebar next to each section. For example, Members shows '+12 this week' or Events shows '3 upcoming'. Gives overview without clicking through.

**Labels:** enhancement, backend

**Suggested Agents:** Backend Development Agent

**Estimate:** 3-4 days

---

#### Issue #98: Implement Collapsible Sidebar

Add collapse/expand button to sidebar. Collapsed mode shows only icons to save screen space. Expanded mode shows icons and labels. Remember user preference.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent

**Estimate:** 2-3 days

---

#### Issue #99: Implement Cmd/Ctrl+K Command Palette

Add keyboard shortcut (Cmd+K on Mac, Ctrl+K on Windows) that opens command palette for quick navigation and actions. Type to filter available commands and hit enter to execute.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent

**Estimate:** 1 week

---

#### Issue #100: Add Natural Language Command Processing

In command palette, allow natural language like 'create new event' or 'show California members' and have system interpret intent and execute appropriate action.

**Labels:** enhancement, ml, backend

**Suggested Agents:** Machine Learning Agent, Backend Development Agent

**Estimate:** 2-3 weeks

---

#### Issue #101: Include AI-Powered Suggestions

Command palette should suggest relevant actions based on context. If viewing a member, suggest 'Edit member', 'Send email', 'View history'. Learn from user behavior over time.

**Labels:** enhancement, ml

**Suggested Agents:** Machine Learning Agent, Backend Development Agent

**Estimate:** 2-3 weeks

---

#### Issue #102: Add Command History

Command palette should remember recently used commands and show them at top of list for quick re-execution. Allow clearing history.

**Labels:** enhancement, frontend, backend

**Suggested Agents:** Full-Stack Development Agent

**Estimate:** 2-3 days

---

#### Issue #103: Implement Keyboard Shortcuts Throughout

Add keyboard shortcuts for common actions (N for new, E for edit, / for search, Esc to close, etc.). Show shortcuts in tooltips and command palette.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent

**Estimate:** 1 week

---

#### Issue #104: Expand Search Beyond Basic Navigation

Make search work across all data types: members, chapters, events, documents, courses, campaigns. Show results grouped by type with count in each category.

**Labels:** enhancement, backend

**Suggested Agents:** Backend Development Agent

**Estimate:** 1-2 weeks

---

#### Issue #105: Show Recent/Popular Searches

In search dropdown, show user's recent searches and organization's popular searches to help discover what others are looking for and re-run previous searches.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent

**Estimate:** 3-4 days

---

#### Issue #106: Display Keyboard Shortcuts in Search

When search dropdown opens, show helpful keyboard shortcuts like '↑↓ to navigate, Enter to select, Esc to close' so users learn to navigate without mouse.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent

**Estimate:** 1-2 days

---

#### Issue #107: Show Record Counts in Search Results

When showing search results grouped by type, include count like 'Members (47)' or 'Events (12)' so users know how many results exist in each category.

**Labels:** enhancement, backend

**Suggested Agents:** Backend Development Agent

**Estimate:** 2-3 days

---

#### Issue #108: Add Search Filters

Provide filters in search results to narrow down by type, date range, status, chapter, etc. Allow combining multiple filters and saving filter combinations.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent

**Estimate:** 1 week

---

#### Issue #109: Add Breadcrumbs on Detail Pages

Ensure every detail page (member detail, event detail, etc.) has breadcrumb navigation showing path to get there and allowing jump back to any level.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent

**Estimate:** 2-3 days

---

#### Issue #110: Add Back Button on Modal Views

Add 'Back' or 'Close' button in top-left of modals and detail panels. Also support Esc key to close and browser back button to return to previous view.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent

**Estimate:** 2-3 days

---

#### Issue #111: Make Tab Navigation Remember Last Selected

When switching between tabs (like Event Details vs Attendees), remember which tab was last selected and return to it when coming back to the page.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent

**Estimate:** 2-3 days

---

#### Issue #112: Add Keyboard Navigation Indicators

When navigating with keyboard (Tab, arrow keys), show clear focus indicators with outline or highlight so users know where they are in the interface.

**Labels:** enhancement, frontend, accessibility

**Suggested Agents:** Frontend Development Agent, UX/UI Design Agent

**Estimate:** 2-3 days

---

#### Issue #113: Add Page Titles in All Sections

Ensure every page has clear title indicating current section and view (like 'Member Management' or 'Los Angeles Chapter - Members') for orientation.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent

**Estimate:** 2-3 days

---

#### Issue #114: Fix Command+K / Ctrl+K Keyboard Shortcut

Repair the keyboard event listener for Cmd+K/Ctrl+K so it properly opens the command palette instead of being ignored or triggering browser default behavior.

**Labels:** bug, frontend

**Suggested Agents:** Frontend Development Agent

**Estimate:** 1-2 days

---

#### Issue #115: Implement Proper Keyboard Event Listeners

Set up global keyboard event handlers that work across all pages, don't conflict with form inputs, and properly handle platform differences (Mac vs Windows vs Linux).

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent

**Estimate:** 3-4 days

---

#### Issue #116: Add Visual Indicator for Command Palette

When command palette is active, show clear visual indicator like backdrop dim, focus highlight, or modal border so users know the palette has keyboard focus.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent, UX/UI Design Agent

**Estimate:** 1-2 days

---

#### Issue #117: Include Command History and Suggestions

In command palette, show recently used commands at top for quick access and AI-powered suggestions based on current context and user behavior patterns.

**Labels:** enhancement, frontend, ml

**Suggested Agents:** Frontend Development Agent, Machine Learning Agent

**Estimate:** 1 week

---

#### Issue #118: Implement Real-Time Notification Bell

Make notification bell update in real-time using WebSockets or polling. Show toast notification when new notification arrives even if user isn't on notifications page.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent, Backend Development Agent

**Estimate:** 1 week

---

#### Issue #119: Create Notification Center/Dropdown

Build dropdown panel that opens from notification bell showing recent notifications with icons, timestamps, and quick actions. Mark as read/unread, delete, or view details.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent

**Estimate:** 1 week

---

#### Issue #120: Add Notification Preferences

Let users control which notifications they receive, how they're delivered (in-app, email, push), and frequency. Allow muting certain notification types.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent

**Estimate:** 1 week

---

#### Issue #121: Include Email Notification Options

For each notification type, allow users to choose whether they also want email notification. Include digest option to batch notifications into daily or weekly email.

**Labels:** enhancement, backend

**Suggested Agents:** Backend Development Agent

**Estimate:** 1 week

---

#### Issue #122: Add Desktop Push Notifications

Implement browser push notifications for high-priority alerts when user has app open. Require permission opt-in and allow disabling per notification type.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent

**Estimate:** 1 week

---

#### Issue #123: Create Notification Categories

Organize notifications into categories like Urgent (red), Informational (blue), Success (green), and allow filtering notification list by category.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent

**Estimate:** 3-4 days

---

#### Issue #124: Build Global Search with Filters

Enhance search to work across members, events, documents, courses simultaneously. Add filter pills to narrow results by type, date, status, etc.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent, Backend Development Agent

**Estimate:** 1-2 weeks

---

#### Issue #125: Add Saved Searches

Allow saving search queries with filters for quick re-use. Name saved searches like 'California Active Members' and access from search dropdown or sidebar.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent

**Estimate:** 1 week

---

#### Issue #126: Show Search Suggestions Based on Popular Queries

In search autocomplete, show what other users commonly search for. Helps discovery and teaches users what data is available to search.

**Labels:** enhancement, backend

**Suggested Agents:** Backend Development Agent

**Estimate:** 3-4 days

---

#### Issue #127: Enable Advanced Filter Combinations

Build advanced filter builder with AND/OR logic. For example: 'Members in (California OR Texas) AND (status = Active) AND (joined > 2024-01-01)'.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent

**Estimate:** 1-2 weeks

---

#### Issue #128: Add Search Within Results

After getting search results, allow narrowing them further with 'search within results' feature instead of starting search over with different terms.

**Labels:** enhancement, frontend

**Suggested Agents:** Frontend Development Agent

**Estimate:** 3-4 days

---

#### Issue #129: Add Export Search Results

Provide export button on search results page to download current result set to CSV or Excel for offline analysis or import into other systems.

**Labels:** enhancement, fullstack

**Suggested Agents:** Full-Stack Development Agent

**Estimate:** 3-4 days

---


