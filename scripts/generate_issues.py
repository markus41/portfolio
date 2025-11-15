#!/usr/bin/env python3
"""
GitHub Issue Generator for Feature Requests and Sub-Issues

This script generates GitHub issues programmatically for large feature requests
with multiple sub-issues. It uses the GitHub CLI (gh) or GitHub API to create
issues with proper hierarchy, labels, and assignments.

Usage:
    python scripts/generate_issues.py --dry-run  # Preview issues
    python scripts/generate_issues.py --create   # Create issues on GitHub
    python scripts/generate_issues.py --export   # Export to JSON/Markdown
"""

import argparse
import json
import subprocess
from typing import Dict, List, Optional


# Agent types that can be assigned to issues
AGENT_TYPES = {
    "frontend": "Frontend Development Agent",
    "backend": "Backend Development Agent",
    "fullstack": "Full-Stack Development Agent",
    "database": "Database Agent",
    "devops": "DevOps/Infrastructure Agent",
    "security": "Security Agent",
    "ux": "UX/UI Design Agent",
    "ml": "Machine Learning Agent",
    "documentation": "Documentation Agent",
    "testing": "Testing/QA Agent",
}


# Feature Request #4: Document Distribution & Management System
FEATURE_REQUEST_4 = {
    "number": 4,
    "title": "Document Distribution & Management System",
    "subtitle": "Hierarchical Document Distribution with OCR and Approval Workflows",
    "category": "Document Management/Navigation Enhancement",
    "problem": "No system for distributing documents throughout the organization hierarchy. Cannot target documents to specific chapters, states, or nationwide. No OCR capability, no approval workflows, and no tracking of who viewed or downloaded documents.",
    "solution": "Build hierarchical document upload wizard with distribution targeting (all CA chapters, all state chapters, specific chapters), OCR integration for scanning paper documents, multi-stage approval workflow, view/download tracking, searchable document library with filters.",
    "alternatives": [
        "Using Google Drive/SharePoint (lacks hierarchy targeting)",
        "Simple file upload (no tracking or workflow)",
        "Email-based distribution (no centralization)",
    ],
    "impact": "High priority - Critical for organizational communication. Affects all admins and members. Estimated time: 5-6 weeks. Ensures consistent document distribution and compliance.",
    "priority": "High",
    "technical": "OCR service integration (AWS Textract or Google Vision), S3/Azure Blob storage, CDN for delivery, document encryption, elasticsearch for search.",
    "labels": ["enhancement", "priority-high", "document-management"],
    "sub_issues": [
        {
            "number": 37,
            "title": "Build Hierarchical Document Upload Wizard",
            "description": "Create multi-step wizard for uploading documents. Step 1: Upload file. Step 2: Add metadata (title, description, category). Step 3: Select distribution targets. Step 4: Set permissions. Step 5: Review and publish.",
            "labels": ["enhancement", "frontend", "backend"],
            "agents": ["fullstack", "ux"],
            "estimate": "1 week",
        },
        {
            "number": 38,
            "title": "Add Distribution Targeting",
            "description": "Implement targeting options: All chapters nationwide, All chapters in specific state(s), Specific chapters only, Specific member segments, Leadership only. Allow combining multiple targeting rules.",
            "labels": ["enhancement", "backend"],
            "agents": ["backend", "database"],
            "estimate": "1 week",
        },
        {
            "number": 39,
            "title": "Implement Document Scanning/OCR Integration",
            "description": "Integrate with AWS Textract or Google Vision API to scan uploaded PDFs and images, extract text content, make documents searchable, and enable text selection in scanned documents.",
            "labels": ["enhancement", "backend", "ml"],
            "agents": ["backend", "ml"],
            "estimate": "1-2 weeks",
        },
        {
            "number": 40,
            "title": "Create Multi-Stage Approval Workflow",
            "description": "Build approval workflow where documents require approval before distribution. Route to appropriate approver based on distribution target (chapter docs to state admin, state docs to national admin). Track approval status and send notifications.",
            "labels": ["enhancement", "backend"],
            "agents": ["backend", "fullstack"],
            "estimate": "1-2 weeks",
        },
        {
            "number": 41,
            "title": "Add Document View/Download Tracking",
            "description": "Track every time a document is viewed or downloaded. Record user, timestamp, document, and action. Provide analytics showing which documents are most accessed, who has/hasn't viewed required documents.",
            "labels": ["enhancement", "backend", "analytics"],
            "agents": ["backend", "database"],
            "estimate": "1 week",
        },
        {
            "number": 42,
            "title": "Build Searchable Document Library",
            "description": "Create document library with full-text search, filters by category, date, chapter, document type, and tags. Show search results with highlighted search terms and relevance ranking.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack", "backend"],
            "estimate": "1-2 weeks",
        },
        {
            "number": 43,
            "title": "Create Resource Library with Categories",
            "description": "Organize documents into categories and subcategories (Policies, Forms, Templates, Guides, Compliance, Marketing). Add tags for cross-category discovery and create featured/recommended sections.",
            "labels": ["enhancement", "frontend", "backend"],
            "agents": ["fullstack", "ux"],
            "estimate": "1 week",
        },
        {
            "number": 44,
            "title": "Implement Document Version Control",
            "description": "Track document versions, allow viewing previous versions, show what changed between versions, enable reverting to previous version, and maintain complete version history with change descriptions.",
            "labels": ["enhancement", "backend"],
            "agents": ["backend", "database"],
            "estimate": "1 week",
        },
        {
            "number": 45,
            "title": "Add Video Content Library",
            "description": "Integrate video streaming capability for training videos, webinar recordings, and educational content. Support multiple video formats, add video player with playback controls, and track video viewing completion.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack", "backend"],
            "estimate": "1-2 weeks",
        },
        {
            "number": 46,
            "title": "Integrate Podcast Player",
            "description": "Add podcast player for NABIP podcast episodes. Include playlist functionality, playback speed control, show notes display, and subscribe to podcast feed.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend", "fullstack"],
            "estimate": "1 week",
        },
        {
            "number": 47,
            "title": "Build Blog/News Article System",
            "description": "Create blog system for publishing news, updates, and articles. Include rich text editor, image upload, categories, tags, commenting system, and RSS feed for subscriptions.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack", "backend"],
            "estimate": "1-2 weeks",
        },
        {
            "number": 48,
            "title": "Create FAQ Management System",
            "description": "Build FAQ system with categories, search functionality, most viewed questions, related questions suggestions, and ability for members to submit new questions.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack", "backend"],
            "estimate": "1 week",
        },
        {
            "number": 49,
            "title": "Add Knowledge Base with Search",
            "description": "Create comprehensive knowledge base with articles, how-to guides, troubleshooting docs, and best practices. Include full-text search, breadcrumb navigation, related articles, and helpful/not helpful voting.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack", "backend"],
            "estimate": "1-2 weeks",
        },
    ],
}


# Feature Request #5: Dashboard & Analytics Platform
FEATURE_REQUEST_5 = {
    "number": 5,
    "title": "Dashboard & Analytics Platform",
    "subtitle": "Customizable Dashboard with Advanced Analytics and Drill-Through",
    "category": "Analytics/Dashboard Enhancement",
    "problem": "Dashboard has poor UX: vertical bar charts should be horizontal, no data labels, non-clickable elements, no period comparisons, default colors instead of NABIP branding, and no customization options. Users cannot drill down into data or export.",
    "solution": "Redesign dashboard with horizontal bar charts, direct data labels, clickable drill-through on all elements, period comparison toggles (YoY, MoM, QoQ), drag-and-drop widget customization, NABIP brand colors throughout, export functionality.",
    "alternatives": [
        "Fixed dashboard layout (not flexible)",
        "Third-party BI tool (adds cost)",
        "Simple static charts (doesn't support analysis)",
    ],
    "impact": "Medium-high priority. Affects all admin users. Estimated time: 4-5 weeks. Increases data-driven decision making.",
    "priority": "Medium-High",
    "technical": "Chart.js or Recharts for visualizations, WebSockets for real-time updates, caching for queries, user preference storage, potential data warehouse for analytics.",
    "labels": ["enhancement", "priority-medium-high", "analytics", "dashboard"],
    "sub_issues": [
        {
            "number": 50,
            "title": "Redesign Revenue Chart to Horizontal Bars",
            "description": "Convert the vertical revenue bar chart to horizontal bars with categories on left and values extending right. This makes category labels more readable and follows better data visualization practices.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend", "ux"],
            "estimate": "2-3 days",
        },
        {
            "number": 51,
            "title": "Add Data Labels Directly on Chart Bars",
            "description": "Display the actual dollar amounts directly on or next to each bar in revenue chart instead of requiring users to hover or reference axis. Makes data immediately readable at a glance.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend"],
            "estimate": "1-2 days",
        },
        {
            "number": 52,
            "title": "Make All Dashboard Elements Clickable",
            "description": "Add click handlers to all dashboard widgets, charts, and metrics. Clicking should drill down to detailed view. For example, clicking revenue chart bar shows transaction details for that category.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack"],
            "estimate": "3-4 days",
        },
        {
            "number": 53,
            "title": "Add Period Comparison Toggles",
            "description": "Add toggles to all dashboard widgets for Year-over-Year, Month-over-Month, and Quarter-over-Quarter comparisons. Show comparison values and percentage change with up/down indicators.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack", "backend"],
            "estimate": "1 week",
        },
        {
            "number": 54,
            "title": "Implement Dashboard Customization",
            "description": "Add 'Edit Dashboard' mode where users can drag-and-drop widgets to rearrange, resize widgets, add/remove widgets from library, and save custom layouts per user.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack", "frontend"],
            "estimate": "1-2 weeks",
        },
        {
            "number": 55,
            "title": "Add Export Functionality",
            "description": "Add export button to dashboard and individual widgets. Allow exporting to CSV for data, Excel for formatted reports, and PDF for presentations. Maintain chart formatting in exports.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack", "backend"],
            "estimate": "1 week",
        },
        {
            "number": 56,
            "title": "Add More Chart Type Options",
            "description": "Expand beyond bar charts to include line charts for trends, area charts for cumulative data, scatter plots for correlations, pie charts for proportions, and combo charts mixing types.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend"],
            "estimate": "1 week",
        },
        {
            "number": 57,
            "title": "Implement Interactive Tooltips",
            "description": "Add detailed tooltips on chart hover showing exact values, percentages, comparison to previous period, and trend indicators. Make tooltips appear quickly and be easy to read.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend"],
            "estimate": "3-4 days",
        },
        {
            "number": 58,
            "title": "Add Data Export from Individual Charts",
            "description": "Allow exporting data from individual charts without exporting entire dashboard. Click export icon on chart to get just that chart's data in chosen format.",
            "labels": ["enhancement", "frontend", "backend"],
            "agents": ["fullstack"],
            "estimate": "3-4 days",
        },
        {
            "number": 59,
            "title": "Create Comparison Views",
            "description": "Build comparison mode for viewing multiple metrics side-by-side. Select 2-4 metrics to compare across same time period and see correlations and patterns.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack"],
            "estimate": "1 week",
        },
        {
            "number": 60,
            "title": "Build Trend Analysis Tools",
            "description": "Add trend lines to time-series charts, show moving averages, highlight anomalies, predict future trends based on historical data, and show confidence intervals.",
            "labels": ["enhancement", "backend", "ml"],
            "agents": ["backend", "ml"],
            "estimate": "1-2 weeks",
        },
        {
            "number": 61,
            "title": "Add Revenue Percentage Breakdown",
            "description": "Show revenue breakdown as both dollar amounts and percentages. Display what percent each category contributes to total revenue for better proportion understanding.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend"],
            "estimate": "2-3 days",
        },
        {
            "number": 62,
            "title": "Implement Date Range Selector",
            "description": "Replace hardcoded 'This Month' with actual date range selector. Allow selecting preset ranges (Today, This Week, This Month, This Quarter, This Year) or custom date ranges.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack"],
            "estimate": "3-4 days",
        },
        {
            "number": 63,
            "title": "Make Revenue Categories Clickable",
            "description": "When clicking a revenue category, show detailed transaction list for that category. Include filtering, sorting, and export of transaction details.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack"],
            "estimate": "1 week",
        },
        {
            "number": 64,
            "title": "Add YoY and MoM Comparison Indicators",
            "description": "Show Year-over-Year and Month-over-Month comparisons with trend arrows (↑ for increase, ↓ for decrease) and color coding (green for positive, red for negative) based on context.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend"],
            "estimate": "2-3 days",
        },
        {
            "number": 65,
            "title": "Add Revenue Data Export",
            "description": "Add dedicated export button for revenue data with options for different formats and date ranges. Include all revenue categories and comparison data in export.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack"],
            "estimate": "3-4 days",
        },
        {
            "number": 66,
            "title": "Build Refund History Tracking",
            "description": "In the refund modal, add complete refund history showing all refunds issued, amounts, reasons, dates, processed by whom, and original transaction details.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack", "backend"],
            "estimate": "3-4 days",
        },
        {
            "number": 67,
            "title": "Add Personalization Options to Greeting",
            "description": "Allow users to customize dashboard greeting, choose whether to show it, set preferred name format, and personalize which widgets appear above the fold.",
            "labels": ["enhancement", "frontend", "backend"],
            "agents": ["fullstack"],
            "estimate": "3-4 days",
        },
        {
            "number": 68,
            "title": "Use Specific Icons for Alert Types",
            "description": "Replace generic warning icon with specific icons for different alert types: exclamation for urgent, info icon for FYI, calendar for upcoming deadlines, dollar sign for financial alerts.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend", "ux"],
            "estimate": "1-2 days",
        },
        {
            "number": 69,
            "title": "Add Registration CTAs to Event Progress Bars",
            "description": "In upcoming events widget, add 'Register Now' or 'View Details' buttons directly on event cards. Show registration progress bar and spots remaining.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend"],
            "estimate": "2-3 days",
        },
        {
            "number": 70,
            "title": "Improve Email Engagement Visual Hierarchy",
            "description": "Redesign email engagement metrics section with better visual hierarchy. Use size to show importance, color to show performance, and clear labels for each metric.",
            "labels": ["enhancement", "frontend", "ux"],
            "agents": ["frontend", "ux"],
            "estimate": "2-3 days",
        },
        {
            "number": 71,
            "title": "Add Quick Access to Active Campaigns",
            "description": "Make the 'Active Campaigns' count clickable to jump directly to campaign list. Add preview of most recent campaigns with quick action buttons (View, Edit, Clone).",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack"],
            "estimate": "3-4 days",
        },
        {
            "number": 72,
            "title": "Apply NABIP Brand Colors Consistently",
            "description": "Update all charts and dashboard elements to use NABIP brand colors (Navy #003366, Teal #008B8B, Gold #FFD700). Create color scheme for different data types that aligns with brand.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend", "ux"],
            "estimate": "2-3 days",
        },
        {
            "number": 73,
            "title": "Add Edit Dashboard Mode",
            "description": "Create 'Edit Dashboard' toggle that enters edit mode where users can drag widgets to reorder, click X to remove widgets, and add new widgets from a widget library.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend", "fullstack"],
            "estimate": "1 week",
        },
        {
            "number": 74,
            "title": "Create Widget Library",
            "description": "Build library of available dashboard widgets (revenue, events, members, campaigns, courses, etc.). Allow users to browse and add widgets to their dashboard with preview before adding.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack"],
            "estimate": "1 week",
        },
        {
            "number": 75,
            "title": "Save Custom Dashboard Layouts",
            "description": "Allow users to save their custom dashboard layout preferences. Store widget positions, sizes, which widgets are shown/hidden, and apply automatically on login.",
            "labels": ["enhancement", "backend"],
            "agents": ["backend", "database"],
            "estimate": "3-4 days",
        },
        {
            "number": 76,
            "title": "Set Default Dashboard View",
            "description": "Let users set which dashboard layout is their default. Provide system default layouts (Executive View, Operations View, Financial View) plus ability to create custom defaults.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack"],
            "estimate": "3-4 days",
        },
        {
            "number": 77,
            "title": "Add Widget Size Options",
            "description": "Allow resizing widgets to small (1x1 grid), medium (2x1), large (2x2), or full-width. Widgets should reflow responsively based on screen size.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend"],
            "estimate": "3-4 days",
        },
        {
            "number": 78,
            "title": "Include Widget Settings Panel",
            "description": "Add settings icon to each widget opening configuration panel. Allow customizing widget-specific settings like date range, metrics shown, chart type, refresh frequency.",
            "labels": ["enhancement", "frontend", "backend"],
            "agents": ["fullstack"],
            "estimate": "1 week",
        },
        {
            "number": 79,
            "title": "Add Member Journey Visualization",
            "description": "Create visual timeline showing typical member journey from join → attend event → take course → renew. Show conversion rates at each stage and identify drop-off points.",
            "labels": ["enhancement", "fullstack", "analytics"],
            "agents": ["fullstack", "backend"],
            "estimate": "1-2 weeks",
        },
        {
            "number": 80,
            "title": "Implement Predictive Churn Analysis",
            "description": "Use machine learning to predict which members are at risk of not renewing. Show churn risk score, contributing factors, and recommended retention actions.",
            "labels": ["enhancement", "ml", "backend"],
            "agents": ["ml", "backend"],
            "estimate": "2-3 weeks",
        },
        {
            "number": 81,
            "title": "Create Event ROI Calculator",
            "description": "Build calculator showing event costs vs revenue and member engagement value. Include attendee count, ticket revenue, sponsor revenue, costs, and net ROI with benchmarks.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack", "backend"],
            "estimate": "1 week",
        },
        {
            "number": 82,
            "title": "Build Chapter Benchmarking Tools",
            "description": "Allow comparing any chapter against state averages, national averages, or peer chapters of similar size. Show where they excel and where they need improvement.",
            "labels": ["enhancement", "fullstack", "analytics"],
            "agents": ["fullstack", "backend"],
            "estimate": "1-2 weeks",
        },
        {
            "number": 83,
            "title": "Add Engagement Heat Maps",
            "description": "Create heat map visualizations showing when members are most active (time of day, day of week, month of year). Use this to optimize event scheduling and email send times.",
            "labels": ["enhancement", "frontend", "analytics"],
            "agents": ["frontend", "backend"],
            "estimate": "1 week",
        },
        {
            "number": 84,
            "title": "Implement Cohort Analysis",
            "description": "Analyze member retention by cohort (members who joined in same month/year). Show retention curves and identify which cohorts have best/worst retention for targeting improvements.",
            "labels": ["enhancement", "backend", "analytics"],
            "agents": ["backend", "ml"],
            "estimate": "1-2 weeks",
        },
        {
            "number": 85,
            "title": "Create Custom Dashboard Builder",
            "description": "Build advanced dashboard builder where power users can create completely custom dashboards with drag-and-drop widgets, custom metrics, SQL-like queries, and share with team.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack", "backend"],
            "estimate": "2-3 weeks",
        },
        {
            "number": 86,
            "title": "Add Automated Insights with AI",
            "description": "Use AI to automatically surface interesting insights from data like 'Member signups increased 32% this month' or 'Houston chapter has 80% higher engagement than average' proactively.",
            "labels": ["enhancement", "ml", "backend"],
            "agents": ["ml", "backend"],
            "estimate": "2-3 weeks",
        },
    ],
}


# Feature Request #6: Navigation & User Experience Overhaul
FEATURE_REQUEST_6 = {
    "number": 6,
    "title": "Navigation & User Experience Overhaul",
    "subtitle": "Enhanced Navigation with AI Search and Quick Access",
    "category": "Navigation/UX Enhancement",
    "problem": "Current navigation is limited: search bar too narrow, no AI-powered search, missing breadcrumbs, no user profile dropdown, no notifications, and no quick access menu. Users struggle to find features and navigate efficiently.",
    "solution": "Expand search bar to 400px with AI natural language search, implement breadcrumbs throughout, add user profile/settings dropdown, include notification bell with count, add Cmd/Ctrl+K command palette, enhance sidebar with badges/counts/sub-menus, add recently accessed items.",
    "alternatives": [
        "Keeping simple navigation (doesn't scale)",
        "Multiple navigation patterns (inconsistent UX)",
        "Search-only interface (too radical)",
    ],
    "impact": "High priority. Affects all users. Estimated time: 3-4 weeks. Reduces time to find features by ~80%.",
    "priority": "High",
    "technical": "Algolia or Elasticsearch for search, AI/LLM integration for natural language, user preference storage, keyboard shortcut system, analytics tracking.",
    "labels": ["enhancement", "priority-high", "navigation", "ux"],
    "sub_issues": [
        {
            "number": 87,
            "title": "Expand Search Bar to 400px Width",
            "description": "Increase the header search bar from its current narrow width to minimum 400px. This makes it more prominent and easier to type longer search queries without horizontal scrolling.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend", "ux"],
            "estimate": "1 day",
        },
        {
            "number": 88,
            "title": "Add AI-Powered Search",
            "description": "Integrate AI natural language processing so users can search with phrases like 'show me all members in California who joined this year' instead of having to use specific filter syntax.",
            "labels": ["enhancement", "backend", "ml"],
            "agents": ["ml", "backend"],
            "estimate": "2-3 weeks",
        },
        {
            "number": 89,
            "title": "Implement Breadcrumb Navigation",
            "description": "Add breadcrumb navigation below header showing current location in site hierarchy. For example: 'Home > Chapters > California > Los Angeles Chapter > Members' with each level clickable.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend"],
            "estimate": "3-4 days",
        },
        {
            "number": 90,
            "title": "Add User Profile/Settings Dropdown",
            "description": "Add user profile icon in top right that opens dropdown menu with options like My Profile, Account Settings, Preferences, Help, and Logout. Show user name and role.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend"],
            "estimate": "2-3 days",
        },
        {
            "number": 91,
            "title": "Include Notification Bell with Count",
            "description": "Add notification bell icon in header that shows count badge for unread notifications. Clicking opens dropdown with recent notifications and link to view all.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack"],
            "estimate": "1 week",
        },
        {
            "number": 92,
            "title": "Add Quick Access Menu",
            "description": "Create quick access menu (like bookmarks) where users can pin frequently used pages/features for one-click access. Allow customizing which items appear in quick access.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack"],
            "estimate": "1 week",
        },
        {
            "number": 93,
            "title": "Add Notification Badges to Sidebar",
            "description": "Show notification badges (red dots or numbers) on sidebar items that have pending actions. For example, show '5' on Members if 5 new member applications are pending approval.",
            "labels": ["enhancement", "frontend", "backend"],
            "agents": ["fullstack"],
            "estimate": "3-4 days",
        },
        {
            "number": 94,
            "title": "Show Counts in Sidebar",
            "description": "Display actual counts next to sidebar items like 'Members (1,247)' and 'Events (23)' so users know how many items exist in each section without clicking.",
            "labels": ["enhancement", "backend"],
            "agents": ["backend"],
            "estimate": "2-3 days",
        },
        {
            "number": 95,
            "title": "Add Expandable Sub-Menus to Sidebar",
            "description": "Make sidebar items expandable with arrow icons. Clicking Members expands to show 'All Members', 'Pending Approvals', 'Lapsed Members' etc. without leaving current page.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend"],
            "estimate": "3-4 days",
        },
        {
            "number": 96,
            "title": "Include Recently Accessed Items",
            "description": "Add 'Recent' section at top of sidebar showing last 5 pages/items user accessed for quick return. Auto-updates as user navigates around the system.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack"],
            "estimate": "3-4 days",
        },
        {
            "number": 97,
            "title": "Add Quick Stats/KPIs Per Section",
            "description": "Show mini stats in sidebar next to each section. For example, Members shows '+12 this week' or Events shows '3 upcoming'. Gives overview without clicking through.",
            "labels": ["enhancement", "backend"],
            "agents": ["backend"],
            "estimate": "3-4 days",
        },
        {
            "number": 98,
            "title": "Implement Collapsible Sidebar",
            "description": "Add collapse/expand button to sidebar. Collapsed mode shows only icons to save screen space. Expanded mode shows icons and labels. Remember user preference.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend"],
            "estimate": "2-3 days",
        },
        {
            "number": 99,
            "title": "Implement Cmd/Ctrl+K Command Palette",
            "description": "Add keyboard shortcut (Cmd+K on Mac, Ctrl+K on Windows) that opens command palette for quick navigation and actions. Type to filter available commands and hit enter to execute.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend"],
            "estimate": "1 week",
        },
        {
            "number": 100,
            "title": "Add Natural Language Command Processing",
            "description": "In command palette, allow natural language like 'create new event' or 'show California members' and have system interpret intent and execute appropriate action.",
            "labels": ["enhancement", "ml", "backend"],
            "agents": ["ml", "backend"],
            "estimate": "2-3 weeks",
        },
        {
            "number": 101,
            "title": "Include AI-Powered Suggestions",
            "description": "Command palette should suggest relevant actions based on context. If viewing a member, suggest 'Edit member', 'Send email', 'View history'. Learn from user behavior over time.",
            "labels": ["enhancement", "ml"],
            "agents": ["ml", "backend"],
            "estimate": "2-3 weeks",
        },
        {
            "number": 102,
            "title": "Add Command History",
            "description": "Command palette should remember recently used commands and show them at top of list for quick re-execution. Allow clearing history.",
            "labels": ["enhancement", "frontend", "backend"],
            "agents": ["fullstack"],
            "estimate": "2-3 days",
        },
        {
            "number": 103,
            "title": "Implement Keyboard Shortcuts Throughout",
            "description": "Add keyboard shortcuts for common actions (N for new, E for edit, / for search, Esc to close, etc.). Show shortcuts in tooltips and command palette.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend"],
            "estimate": "1 week",
        },
        {
            "number": 104,
            "title": "Expand Search Beyond Basic Navigation",
            "description": "Make search work across all data types: members, chapters, events, documents, courses, campaigns. Show results grouped by type with count in each category.",
            "labels": ["enhancement", "backend"],
            "agents": ["backend"],
            "estimate": "1-2 weeks",
        },
        {
            "number": 105,
            "title": "Show Recent/Popular Searches",
            "description": "In search dropdown, show user's recent searches and organization's popular searches to help discover what others are looking for and re-run previous searches.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack"],
            "estimate": "3-4 days",
        },
        {
            "number": 106,
            "title": "Display Keyboard Shortcuts in Search",
            "description": "When search dropdown opens, show helpful keyboard shortcuts like '↑↓ to navigate, Enter to select, Esc to close' so users learn to navigate without mouse.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend"],
            "estimate": "1-2 days",
        },
        {
            "number": 107,
            "title": "Show Record Counts in Search Results",
            "description": "When showing search results grouped by type, include count like 'Members (47)' or 'Events (12)' so users know how many results exist in each category.",
            "labels": ["enhancement", "backend"],
            "agents": ["backend"],
            "estimate": "2-3 days",
        },
        {
            "number": 108,
            "title": "Add Search Filters",
            "description": "Provide filters in search results to narrow down by type, date range, status, chapter, etc. Allow combining multiple filters and saving filter combinations.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack"],
            "estimate": "1 week",
        },
        {
            "number": 109,
            "title": "Add Breadcrumbs on Detail Pages",
            "description": "Ensure every detail page (member detail, event detail, etc.) has breadcrumb navigation showing path to get there and allowing jump back to any level.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend"],
            "estimate": "2-3 days",
        },
        {
            "number": 110,
            "title": "Add Back Button on Modal Views",
            "description": "Add 'Back' or 'Close' button in top-left of modals and detail panels. Also support Esc key to close and browser back button to return to previous view.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend"],
            "estimate": "2-3 days",
        },
        {
            "number": 111,
            "title": "Make Tab Navigation Remember Last Selected",
            "description": "When switching between tabs (like Event Details vs Attendees), remember which tab was last selected and return to it when coming back to the page.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend"],
            "estimate": "2-3 days",
        },
        {
            "number": 112,
            "title": "Add Keyboard Navigation Indicators",
            "description": "When navigating with keyboard (Tab, arrow keys), show clear focus indicators with outline or highlight so users know where they are in the interface.",
            "labels": ["enhancement", "frontend", "accessibility"],
            "agents": ["frontend", "ux"],
            "estimate": "2-3 days",
        },
        {
            "number": 113,
            "title": "Add Page Titles in All Sections",
            "description": "Ensure every page has clear title indicating current section and view (like 'Member Management' or 'Los Angeles Chapter - Members') for orientation.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend"],
            "estimate": "2-3 days",
        },
        {
            "number": 114,
            "title": "Fix Command+K / Ctrl+K Keyboard Shortcut",
            "description": "Repair the keyboard event listener for Cmd+K/Ctrl+K so it properly opens the command palette instead of being ignored or triggering browser default behavior.",
            "labels": ["bug", "frontend"],
            "agents": ["frontend"],
            "estimate": "1-2 days",
        },
        {
            "number": 115,
            "title": "Implement Proper Keyboard Event Listeners",
            "description": "Set up global keyboard event handlers that work across all pages, don't conflict with form inputs, and properly handle platform differences (Mac vs Windows vs Linux).",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend"],
            "estimate": "3-4 days",
        },
        {
            "number": 116,
            "title": "Add Visual Indicator for Command Palette",
            "description": "When command palette is active, show clear visual indicator like backdrop dim, focus highlight, or modal border so users know the palette has keyboard focus.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend", "ux"],
            "estimate": "1-2 days",
        },
        {
            "number": 117,
            "title": "Include Command History and Suggestions",
            "description": "In command palette, show recently used commands at top for quick access and AI-powered suggestions based on current context and user behavior patterns.",
            "labels": ["enhancement", "frontend", "ml"],
            "agents": ["frontend", "ml"],
            "estimate": "1 week",
        },
        {
            "number": 118,
            "title": "Implement Real-Time Notification Bell",
            "description": "Make notification bell update in real-time using WebSockets or polling. Show toast notification when new notification arrives even if user isn't on notifications page.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack", "backend"],
            "estimate": "1 week",
        },
        {
            "number": 119,
            "title": "Create Notification Center/Dropdown",
            "description": "Build dropdown panel that opens from notification bell showing recent notifications with icons, timestamps, and quick actions. Mark as read/unread, delete, or view details.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend"],
            "estimate": "1 week",
        },
        {
            "number": 120,
            "title": "Add Notification Preferences",
            "description": "Let users control which notifications they receive, how they're delivered (in-app, email, push), and frequency. Allow muting certain notification types.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack"],
            "estimate": "1 week",
        },
        {
            "number": 121,
            "title": "Include Email Notification Options",
            "description": "For each notification type, allow users to choose whether they also want email notification. Include digest option to batch notifications into daily or weekly email.",
            "labels": ["enhancement", "backend"],
            "agents": ["backend"],
            "estimate": "1 week",
        },
        {
            "number": 122,
            "title": "Add Desktop Push Notifications",
            "description": "Implement browser push notifications for high-priority alerts when user has app open. Require permission opt-in and allow disabling per notification type.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend"],
            "estimate": "1 week",
        },
        {
            "number": 123,
            "title": "Create Notification Categories",
            "description": "Organize notifications into categories like Urgent (red), Informational (blue), Success (green), and allow filtering notification list by category.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack"],
            "estimate": "3-4 days",
        },
        {
            "number": 124,
            "title": "Build Global Search with Filters",
            "description": "Enhance search to work across members, events, documents, courses simultaneously. Add filter pills to narrow results by type, date, status, etc.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack", "backend"],
            "estimate": "1-2 weeks",
        },
        {
            "number": 125,
            "title": "Add Saved Searches",
            "description": "Allow saving search queries with filters for quick re-use. Name saved searches like 'California Active Members' and access from search dropdown or sidebar.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack"],
            "estimate": "1 week",
        },
        {
            "number": 126,
            "title": "Show Search Suggestions Based on Popular Queries",
            "description": "In search autocomplete, show what other users commonly search for. Helps discovery and teaches users what data is available to search.",
            "labels": ["enhancement", "backend"],
            "agents": ["backend"],
            "estimate": "3-4 days",
        },
        {
            "number": 127,
            "title": "Enable Advanced Filter Combinations",
            "description": "Build advanced filter builder with AND/OR logic. For example: 'Members in (California OR Texas) AND (status = Active) AND (joined > 2024-01-01)'.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack"],
            "estimate": "1-2 weeks",
        },
        {
            "number": 128,
            "title": "Add Search Within Results",
            "description": "After getting search results, allow narrowing them further with 'search within results' feature instead of starting search over with different terms.",
            "labels": ["enhancement", "frontend"],
            "agents": ["frontend"],
            "estimate": "3-4 days",
        },
        {
            "number": 129,
            "title": "Add Export Search Results",
            "description": "Provide export button on search results page to download current result set to CSV or Excel for offline analysis or import into other systems.",
            "labels": ["enhancement", "fullstack"],
            "agents": ["fullstack"],
            "estimate": "3-4 days",
        },
    ],
}


ALL_FEATURE_REQUESTS = [FEATURE_REQUEST_4, FEATURE_REQUEST_5, FEATURE_REQUEST_6]


def format_issue_body(feature_request: Dict, is_parent: bool = False) -> str:
    """Format the issue body for GitHub."""
    if is_parent:
        body = f"""## {feature_request['subtitle']}

**Feature Category:** {feature_request['category']}

### Problem Statement
{feature_request['problem']}

### Proposed Solution
{feature_request['solution']}

### Alternatives Considered
"""
        for alt in feature_request["alternatives"]:
            body += f"- {alt}\n"

        body += f"""
### Expected Impact
{feature_request['impact']}

**Priority:** {feature_request['priority']}

### Technical Considerations
{feature_request['technical']}

### Sub-Issues
This feature is broken down into {len(feature_request['sub_issues'])} sub-issues:

"""
        for sub in feature_request["sub_issues"]:
            body += f"- [ ] #{sub['number']}: {sub['title']}\n"

        return body
    else:
        # For sub-issues
        return feature_request["description"]


def generate_issue_command(
    issue: Dict, parent_number: Optional[int] = None
) -> List[str]:
    """Generate GitHub CLI command to create an issue."""
    cmd = ["gh", "issue", "create"]

    # Add title
    cmd.extend(["--title", issue["title"]])

    # Add body
    body = issue.get("body", issue.get("description", ""))
    if parent_number:
        body = f"Part of #{parent_number}\n\n{body}"
    cmd.extend(["--body", body])

    # Add labels
    if "labels" in issue:
        cmd.extend(["--label", ",".join(issue["labels"])])

    # Add assignees (agents)
    if "agents" in issue:
        agents_str = ", ".join([AGENT_TYPES.get(a, a) for a in issue["agents"]])
        body += f"\n\n**Suggested Agents:** {agents_str}"

    return cmd


def create_issues_dry_run():
    """Preview what issues would be created."""
    print("=" * 80)
    print("DRY RUN: Preview of issues to be created")
    print("=" * 80)

    for fr in ALL_FEATURE_REQUESTS:
        print(f"\n{'=' * 80}")
        print(f"FEATURE REQUEST #{fr['number']}: {fr['title']}")
        print(f"{'=' * 80}")
        print(f"Labels: {', '.join(fr['labels'])}")
        print(f"Sub-issues: {len(fr['sub_issues'])}")
        print(f"\nBody preview:\n{format_issue_body(fr, is_parent=True)[:500]}...")

        print(f"\n{'-' * 80}")
        print(f"SUB-ISSUES for Feature Request #{fr['number']}")
        print(f"{'-' * 80}")

        for sub in fr["sub_issues"]:
            agents_str = ", ".join(
                [AGENT_TYPES.get(a, a) for a in sub.get("agents", [])]
            )
            print(f"\n  Issue #{sub['number']}: {sub['title']}")
            print(f"    Labels: {', '.join(sub['labels'])}")
            print(f"    Agents: {agents_str}")
            print(f"    Estimate: {sub.get('estimate', 'N/A')}")
            print(f"    Description: {sub['description'][:100]}...")


def create_issues_on_github():
    """Create issues on GitHub using the GitHub CLI."""
    print("Creating issues on GitHub...")

    # Check if gh CLI is available
    try:
        subprocess.run(["gh", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: GitHub CLI (gh) is not installed or not in PATH")
        print("Please install it from: https://cli.github.com/")
        return False

    for fr in ALL_FEATURE_REQUESTS:
        print(f"\nCreating Feature Request #{fr['number']}: {fr['title']}")

        # Create parent feature request issue
        parent_issue = {
            "title": f"[Feature]: {fr['title']}",
            "body": format_issue_body(fr, is_parent=True),
            "labels": fr["labels"],
        }

        cmd = generate_issue_command(parent_issue)
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            parent_url = result.stdout.strip()
            print(f"  ✓ Created parent issue: {parent_url}")

            # Extract issue number from URL
            parent_number = parent_url.split("/")[-1]

            # Create sub-issues
            for sub in fr["sub_issues"]:
                print(f"  Creating sub-issue #{sub['number']}: {sub['title']}")
                sub_issue = {
                    "title": f"[Enhancement]: {sub['title']}",
                    "description": sub["description"],
                    "labels": sub["labels"],
                    "agents": sub.get("agents", []),
                }

                cmd = generate_issue_command(sub_issue, parent_number)
                try:
                    result = subprocess.run(
                        cmd, check=True, capture_output=True, text=True
                    )
                    sub_url = result.stdout.strip()
                    print(f"    ✓ Created: {sub_url}")
                except subprocess.CalledProcessError as e:
                    print(f"    ✗ Failed: {e.stderr}")

        except subprocess.CalledProcessError as e:
            print(f"  ✗ Failed to create parent issue: {e.stderr}")
            continue

    print("\n✓ Issue creation complete!")
    return True


def export_to_json():
    """Export issue data to JSON file."""
    output_file = "issues_data.json"
    data = {
        "feature_requests": ALL_FEATURE_REQUESTS,
        "agent_types": AGENT_TYPES,
    }

    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)

    print(f"✓ Exported issue data to {output_file}")


def export_to_markdown():
    """Export issue data to Markdown file."""
    output_file = "ISSUES_OVERVIEW.md"

    with open(output_file, "w") as f:
        f.write("# Feature Requests and Sub-Issues Overview\n\n")
        f.write(
            "This document provides an overview of all feature requests and their sub-issues.\n\n"
        )

        f.write("## Available Agent Types\n\n")
        for agent_key, agent_name in AGENT_TYPES.items():
            f.write(f"- **{agent_key}**: {agent_name}\n")
        f.write("\n---\n\n")

        for fr in ALL_FEATURE_REQUESTS:
            f.write(f"## Feature Request #{fr['number']}: {fr['title']}\n\n")
            f.write(f"**{fr['subtitle']}**\n\n")
            f.write(f"**Category:** {fr['category']}\n\n")
            f.write(f"**Priority:** {fr['priority']}\n\n")

            f.write("### Problem Statement\n\n")
            f.write(f"{fr['problem']}\n\n")

            f.write("### Proposed Solution\n\n")
            f.write(f"{fr['solution']}\n\n")

            f.write("### Alternatives Considered\n\n")
            for alt in fr["alternatives"]:
                f.write(f"- {alt}\n")
            f.write("\n")

            f.write("### Expected Impact\n\n")
            f.write(f"{fr['impact']}\n\n")

            f.write("### Technical Considerations\n\n")
            f.write(f"{fr['technical']}\n\n")

            f.write(f"### Sub-Issues ({len(fr['sub_issues'])} total)\n\n")

            for sub in fr["sub_issues"]:
                f.write(f"#### Issue #{sub['number']}: {sub['title']}\n\n")
                f.write(f"{sub['description']}\n\n")
                f.write(f"**Labels:** {', '.join(sub['labels'])}\n\n")

                if sub.get("agents"):
                    agents_str = ", ".join(
                        [AGENT_TYPES.get(a, a) for a in sub["agents"]]
                    )
                    f.write(f"**Suggested Agents:** {agents_str}\n\n")

                if sub.get("estimate"):
                    f.write(f"**Estimate:** {sub['estimate']}\n\n")

                f.write("---\n\n")

            f.write("\n")

    print(f"✓ Exported issue overview to {output_file}")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Generate GitHub issues for feature requests and sub-issues"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview issues without creating them on GitHub",
    )
    parser.add_argument(
        "--create",
        action="store_true",
        help="Create issues on GitHub using gh CLI",
    )
    parser.add_argument(
        "--export-json",
        action="store_true",
        help="Export issue data to JSON file",
    )
    parser.add_argument(
        "--export-md",
        action="store_true",
        help="Export issue overview to Markdown file",
    )

    args = parser.parse_args()

    # If no arguments provided, show help
    if not any([args.dry_run, args.create, args.export_json, args.export_md]):
        parser.print_help()
        print("\nExample usage:")
        print("  python scripts/generate_issues.py --dry-run    # Preview issues")
        print("  python scripts/generate_issues.py --create     # Create on GitHub")
        print("  python scripts/generate_issues.py --export-md  # Export to Markdown")
        return

    if args.dry_run:
        create_issues_dry_run()

    if args.create:
        create_issues_on_github()

    if args.export_json:
        export_to_json()

    if args.export_md:
        export_to_markdown()


if __name__ == "__main__":
    main()
