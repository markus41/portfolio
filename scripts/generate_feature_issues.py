# flake8: noqa: E501
#!/usr/bin/env python3
"""
Generate GitHub issues data for Feature Requests #7-#11 and their sub-issues.

This script creates structured data for creating GitHub issues programmatically.
The output can be used with GitHub CLI (gh) or GitHub API to create the issues.
"""

import json
from typing import List, Dict, Any


class IssueGenerator:
    """Generate structured GitHub issue data."""

    def __init__(self):
        self.feature_requests = []
        self.sub_issues = []

    def create_feature_request(
        self,
        number: int,
        title: str,
        category: str,
        problem_statement: str,
        proposed_solution: str,
        alternatives: List[str],
        expected_impact: Dict[str, Any],
        priority: str,
        technical_considerations: str,
        assigned_agent: str = None,
    ) -> Dict[str, Any]:
        """Create a feature request issue."""
        labels = ["enhancement", "feature-request", priority.lower()]

        body = f"""## Feature Category
{category}

## Problem Statement
{problem_statement}

## Proposed Solution
{proposed_solution}

## Alternatives Considered
{chr(10).join(f'- {alt}' for alt in alternatives)}

## Expected Impact
- **Priority**: {expected_impact.get('priority', 'Medium')}
- **Affects**: {expected_impact.get('affects', 'N/A')}
- **Estimated Time**: {expected_impact.get('time', 'N/A')}
- **Impact**: {expected_impact.get('impact', 'N/A')}

## Technical Considerations
{technical_considerations}
"""

        if assigned_agent:
            body += f"\n## Assigned Agent\n{assigned_agent}\n"

        return {
            "number": number,
            "title": f"[Feature #{number}] {title}",
            "body": body,
            "labels": labels,
            "assigned_agent": assigned_agent,
        }

    def create_sub_issue(
        self,
        number: int,
        title: str,
        description: str,
        parent_feature: int,
        assigned_agent: str = None,
        labels: List[str] = None,
    ) -> Dict[str, Any]:
        """Create a sub-issue linked to a parent feature request."""
        default_labels = ["enhancement", "sub-issue", f"feature-{parent_feature}"]
        issue_labels = labels if labels else default_labels

        body = f"""## Description
{description}

## Parent Feature Request
This is a sub-issue of Feature Request #{parent_feature}

## Related Issues
- Part of #7 (if applicable based on parent feature)
"""

        if assigned_agent:
            body += f"\n## Assigned Agent\n{assigned_agent}\n"

        return {
            "number": number,
            "title": f"[Issue #{number}] {title}",
            "body": body,
            "labels": issue_labels,
            "parent_feature": parent_feature,
            "assigned_agent": assigned_agent,
        }


def generate_all_issues():
    """Generate all feature requests and sub-issues."""
    gen = IssueGenerator()

    # Feature Request #7: Member Management System Enhancement
    fr7 = gen.create_feature_request(
        number=7,
        title="Advanced Member Management with Editable Grid and Custom Fields",
        category="Member Management Enhancement",
        problem_statement="Member management lacks critical features: no editable grid, limited custom fields, modal-only editing, no bulk import progress, basic filtering, and no duplicate detection. Admins spend excessive time on manual data management.",
        proposed_solution="Implement editable grid like chapters page, add unlimited custom fields, enable inline editing, add bulk import with progress tracking, implement advanced filtering with saved filters, add auto member merge/duplicate detection.",
        alternatives=[
            "Keeping modal-only editing (creates friction)",
            "Limited custom fields (doesn't meet needs)",
            "Manual duplicate detection (too time-consuming)",
        ],
        expected_impact={
            "priority": "Medium-high priority",
            "affects": "National and chapter admins",
            "time": "4-5 weeks",
            "impact": "Reduces member management time by ~70%",
        },
        priority="Medium",
        technical_considerations="Virtual scrolling for large lists, debouncing for inline edits, background jobs for bulk import, fuzzy matching for duplicates, database indexing for custom fields.",
        assigned_agent="Backend/Frontend Integration Agent - handles complex CRUD operations with UI components",
    )

    # Feature Request #8: Campaign & Email Marketing Platform
    fr8 = gen.create_feature_request(
        number=8,
        title="Full-Featured Email Campaign Management with A/B Testing",
        category="Marketing/Communications Enhancement",
        problem_statement="Campaign management is severely limited: creation doesn't work, no templates, no A/B testing, no send time optimization, basic editor, missing analytics. Segment query shows raw text instead of visual builder. No preview before sending.",
        proposed_solution="Fix campaign creation, add templates library, implement A/B testing for subject/content/timing, add AI send time optimization, build drag-and-drop email editor, add campaign cloning, create visual segment builder, add comprehensive analytics with click maps.",
        alternatives=[
            "Integrating Mailchimp/SendGrid UI (loses customization)",
            "Basic email only (doesn't meet marketing needs)",
            "Text-only editor (limits design)",
        ],
        expected_impact={
            "priority": "Medium priority",
            "affects": "Marketing team, admins",
            "time": "5-6 weeks",
            "impact": "Increases email engagement by ~40%",
        },
        priority="Medium",
        technical_considerations="Email service provider (SendGrid, AWS SES), template storage, email rendering preview, segment query engine, pixel/link tracking, A/B test calculations.",
        assigned_agent="Marketing Automation Agent - specializes in email campaigns and analytics",
    )

    # Feature Request #9: Learning Management System (LMS)
    fr9 = gen.create_feature_request(
        number=9,
        title="Complete LMS with Course Builder, Tracking, and Certifications",
        category="Education/LMS Enhancement",
        problem_statement="LMS is broken: course creation doesn't work, no preview, no enrollment tracking, no progress visualization, no certificates, no learning paths with prerequisites. Members cannot access professional development.",
        proposed_solution="Fix course creation, implement SCORM-compatible course builder, add preview, build enrollment tracking with capacity management, create progress visualization, add auto certificate generation, implement learning paths with prerequisites, add quiz engine.",
        alternatives=[
            "Integrating Moodle/Canvas (complexity)",
            "Basic course listing (doesn't meet CE needs)",
            "Video-only platform (lacks interactivity)",
        ],
        expected_impact={
            "priority": "Medium-high priority",
            "affects": "All members",
            "time": "6-8 weeks",
            "impact": "Increases course completion by ~50%",
        },
        priority="Medium",
        technical_considerations="SCORM player, video streaming with CDN, quiz engine, PDF certificate generation with signatures, CE credit tracking, prerequisite logic.",
        assigned_agent="Learning Management Agent - specializes in educational content and certification workflows",
    )

    # Feature Request #10: Advanced Reporting System
    fr10 = gen.create_feature_request(
        number=10,
        title="Custom Report Builder with Visual Designer and Scheduling",
        category="Reporting/Analytics Enhancement",
        problem_statement="Reporting is broken: 'Run Report' doesn't execute, reports don't display properly on web, no interactive preview, no in-browser parameter editing, no scheduling, no sharing. Builder shows columns but no data types or preview.",
        proposed_solution="Fix report execution, create visual report builder, add interactive preview with drill-down, enable in-browser parameter editing, implement scheduled email delivery, add sharing with permissions, build template library, enable custom graph creation.",
        alternatives=[
            "Using Tableau/Power BI (expensive, complex)",
            "Static reports only (no ad-hoc analysis)",
            "Excel export only (loses interactivity)",
        ],
        expected_impact={
            "priority": "Medium priority",
            "affects": "All admin users",
            "time": "5-6 weeks",
            "impact": "Reduces report creation time by ~80%",
        },
        priority="Medium",
        technical_considerations="Query builder with SQL generation, report caching, background job queue for large reports, real-time data refresh, JSON report definitions, column-level permissions.",
        assigned_agent="Analytics & Reporting Agent - specializes in data visualization and report generation",
    )

    # Feature Request #11: Event Management System
    fr11 = gen.create_feature_request(
        number=11,
        title="Comprehensive Event Management with Registration and Analytics",
        category="Event Management Enhancement",
        problem_statement="Event management is broken and incomplete: creation workflow doesn't work, no session selection for multi-track events, no meal preferences, no hotel management, no companion registration, no virtual event support, no post-event surveys. Event cards lack status indicators and venue info.",
        proposed_solution="Fix creation workflow, add session selection for tracks, implement meal/dietary preferences, add hotel room block management, enable guest registration, integrate virtual event streaming, add automated post-event surveys, implement CPE credit tracking, create photo galleries, build sponsor portal.",
        alternatives=[
            "Using Eventbrite/Cvent (loses customization)",
            "Basic registration only (doesn't meet complex needs)",
            "Separate virtual platform (fragments UX)",
        ],
        expected_impact={
            "priority": "Medium-high priority",
            "affects": "All members, event coordinators",
            "time": "6-8 weeks",
            "impact": "Increases event registration by ~35%",
        },
        priority="Medium",
        technical_considerations="Payment gateway integration, session capacity management, calendar integration (iCal), QR code check-in, email reminder automation, mobile app integration.",
        assigned_agent="Event Management Agent - specializes in event logistics and registration workflows",
    )

    gen.feature_requests = [fr7, fr8, fr9, fr10, fr11]

    # Sub-issues for Feature Request #7 (Member Management)
    member_mgmt_issues = [
        (
            130,
            "Implement Editable Grid for Members",
            "Convert member table to editable grid similar to chapters page. Allow clicking into any cell to edit directly inline without opening modals. Auto-save changes on blur or Enter key.",
            "Frontend Data Grid Agent",
        ),
        (
            131,
            "Add Unlimited Custom Columns",
            "Allow admins to create custom fields for member data beyond standard fields. Support field types like text, number, date, dropdown, checkbox, multi-select, file upload.",
            "Backend Schema Agent",
        ),
        (
            132,
            "Enable Inline Editing Without Modals",
            "Make all member data editable directly in the table view. Click a cell to edit, tab to next field, auto-save changes, show validation errors inline without popup interruptions.",
            "Frontend Form Agent",
        ),
        (
            133,
            "Add Bulk Import with Progress Tracking",
            "Build CSV/Excel import feature with drag-and-drop upload, column mapping interface, validation preview, progress bar during import, error report for failed rows, and rollback option.",
            "Data Import Agent",
        ),
        (
            134,
            "Implement Advanced Filtering with Saved Filters",
            "Create advanced filter builder with multiple conditions, AND/OR logic, and save filter combinations with names like 'California Active Members' for quick re-use.",
            "Query Builder Agent",
        ),
        (
            135,
            "Add Member Merge and Duplicate Detection",
            "Automatically detect potential duplicate members based on email, name similarity, phone number. Suggest merges and provide merge interface to combine duplicate records.",
            "Data Quality Agent",
        ),
        (
            136,
            "Enable Inline Editing in Member Detail Modal",
            "Make member detail modal editable instead of read-only. Allow clicking any field to edit, show save/cancel buttons, validate before saving, and show success feedback.",
            "Frontend Form Agent",
        ),
        (
            137,
            "Add Engagement Score Breakdown",
            "Instead of just showing numeric engagement score, provide breakdown showing how it's calculated (event attendance 30%, course completions 25%, email opens 20%, etc.) with details.",
            "Analytics Display Agent",
        ),
        (
            138,
            "Standardize Status Badges",
            "Fix inconsistent status badge colors and styles. Use green for Active, red for Inactive, yellow for Pending, gray for Lapsed. Apply consistently across all views.",
            "UI Components Agent",
        ),
        (
            139,
            "Fix Add Member Button",
            "Ensure Add Member button actually opens the new member form modal. This overlaps with Issue #1 but specific to the member management page.",
            "Frontend Bug Fix Agent",
        ),
        (
            140,
            "Add Bulk Selection Checkboxes",
            "Add checkbox column to member table for selecting multiple members. Include 'Select All' checkbox in header and show bulk action toolbar when items selected.",
            "Frontend Data Grid Agent",
        ),
        (
            141,
            "Add Quick Filters Above Table",
            "Provide filter chips above table for common filters like 'Active Members', 'Pending Renewals', 'California', 'Joined This Year' that apply with single click.",
            "Frontend Filter Agent",
        ),
        (
            142,
            "Add Column Resize Handles",
            "Make table columns resizable by dragging column borders. Save column widths per user so table appearance persists across sessions.",
            "Frontend Data Grid Agent",
        ),
        (
            143,
            "Implement Sticky Header When Scrolling",
            "Make table header stick to top of viewport when scrolling down long member lists so column labels remain visible for context.",
            "Frontend CSS Agent",
        ),
        (
            144,
            "Add Row Hover Highlights",
            "Highlight entire row on hover to make it easier to visually track across columns. Use subtle background color change.",
            "Frontend CSS Agent",
        ),
        (
            145,
            "Show Column Sorting Indicators",
            "When column is sorted, show up/down arrow in column header. Allow clicking column header to sort ascending, click again for descending, click again to remove sort.",
            "Frontend Data Grid Agent",
        ),
        (
            146,
            "Improve Pagination Display",
            "Show 'Showing 1-50 of 1,247 members' instead of just page numbers. Makes it clear where you are in the total dataset and how many results exist.",
            "Frontend Pagination Agent",
        ),
        (
            147,
            "Add Table Density Options",
            "Provide compact, comfortable, and spacious view options that adjust row height and padding. Compact fits more rows on screen, spacious is easier to read.",
            "Frontend Layout Agent",
        ),
        (
            148,
            "Add Self-Service Password Reset",
            "Build password reset flow where members can reset their own password via email link without contacting admin. Send reset email, validate token, allow setting new password.",
            "Authentication Agent",
        ),
        (
            149,
            "Implement Two-Factor Authentication",
            "Add optional 2FA for members using authenticator apps (Google Authenticator, Authy). Show QR code for setup, validate codes on login, provide backup codes.",
            "Security Agent",
        ),
        (
            150,
            "Add Member Profile Photo Upload",
            "Allow members to upload profile photo with cropping tool to ensure proper aspect ratio and size. Display photos throughout system (member directory, comments, etc.).",
            "File Upload Agent",
        ),
        (
            151,
            "Create Digital Membership Card with QR Code",
            "Generate digital membership card with member info and QR code that can be scanned for event check-in or identity verification. Allow downloading to Apple/Google Wallet.",
            "QR Code Generator Agent",
        ),
        (
            152,
            "Enable Download of Tax Documents/Receipts",
            "Provide member portal section where members can download receipts for dues payments, event registrations, donations for tax purposes. Include year-end summary.",
            "PDF Generation Agent",
        ),
        (
            153,
            "Build Personal Dashboard with Widgets",
            "Create member-facing dashboard showing upcoming events, course progress, renewal date, engagement stats. Allow customizing which widgets appear.",
            "Dashboard Builder Agent",
        ),
        (
            154,
            "Add Referral Tracking System",
            "Implement referral program where members can generate referral links, track who they referred, earn rewards for successful referrals, and see referral leaderboard.",
            "Referral Tracking Agent",
        ),
        (
            155,
            "Implement Member-to-Member Messaging",
            "Add internal messaging system where members can send messages to other members. Include inbox, sent messages, message threading, and notifications.",
            "Messaging System Agent",
        ),
        (
            156,
            "Add Personal Calendar Integration",
            "Allow members to sync their NABIP events with personal calendar (Google Calendar, Outlook, Apple Calendar). Provide iCal feed URL or OAuth integration.",
            "Calendar Integration Agent",
        ),
        (
            157,
            "Create Mobile App QR Code Login",
            "Generate QR code that members can scan with mobile device to quickly log into member portal without typing credentials. Short-lived QR codes for security.",
            "Authentication Agent",
        ),
        (
            158,
            "Add Membership Calculator/Comparison Tool",
            "Build tool showing different membership tiers, benefits, and pricing. Allow comparing tiers side-by-side to help prospects choose appropriate membership level.",
            "Comparison Tool Agent",
        ),
        (
            159,
            "Create Member Referral Rewards Program",
            "Track member referrals and automatically apply rewards (discounts, points, recognition). Show referral dashboard with stats and reward balance.",
            "Rewards System Agent",
        ),
        (
            160,
            "Build Tiered Benefits Visualization",
            "Create visual comparison of benefits across membership tiers (Individual, Agency, Corporate). Use checkmarks, highlighted features, and tier badges.",
            "UI Visualization Agent",
        ),
        (
            161,
            "Implement Automatic Tier Upgrades",
            "When member meets criteria for higher tier (e.g. certain # of employees), automatically suggest or apply upgrade. Send notification with upgrade benefits.",
            "Business Rules Agent",
        ),
        (
            162,
            "Add Membership Pause/Hold Options",
            "Allow members to temporarily pause membership for life events (medical leave, sabbatical) without losing member # or tenure. Set resume date.",
            "Membership Lifecycle Agent",
        ),
        (
            163,
            "Enable Transfer Membership Between Individuals",
            "Provide workflow for transferring membership from one person to another (like when employee leaves company). Transfer history and benefits eligibility.",
            "Membership Transfer Agent",
        ),
        (
            164,
            "Support Household/Family Memberships",
            "Allow linking multiple individual memberships into family/household account. Share benefits, single renewal date, family discount pricing, linked profiles.",
            "Membership Grouping Agent",
        ),
    ]

    # Sub-issues for Feature Request #8 (Campaign & Email Marketing)
    campaign_issues = [
        (
            165,
            "Fix Campaign Creation Workflow",
            "Repair the completely broken campaign creation process. Ensure form loads, all fields work, rich text editor functions, and campaigns actually save/send.",
            "Frontend Bug Fix Agent",
        ),
        (
            166,
            "Add Campaign Templates Library",
            "Build library of pre-designed email templates organized by category (Newsletter, Event Announcement, Welcome Series). Allow previewing and using templates as starting point.",
            "Email Template Agent",
        ),
        (
            167,
            "Implement A/B Testing Capabilities",
            "Add A/B testing for subject lines, email content, and send times. Set up test with winner criteria (open rate, click rate), test percentage, and automatic winner selection.",
            "A/B Testing Agent",
        ),
        (
            168,
            "Add Send Time Optimization",
            "Use AI to analyze when each member typically opens emails and schedule delivery for optimal time. Provide 'Optimize Send Time' option when scheduling campaigns.",
            "ML Optimization Agent",
        ),
        (
            169,
            "Build Visual Email Editor",
            "Create drag-and-drop email builder with blocks for text, images, buttons, social links, dividers. Include pre-built layouts, mobile preview, and HTML code editor for power users.",
            "Email Editor Agent",
        ),
        (
            170,
            "Add Campaign Cloning",
            "Provide 'Clone Campaign' button that duplicates existing campaign with all settings and content. Useful for recurring newsletters or similar campaigns.",
            "Campaign Management Agent",
        ),
        (
            171,
            "Display Actual Schedule Date",
            "Instead of showing vague 'scheduled' status, display exact date and time campaign will send. Make it prominent so admins can verify before campaign goes out.",
            "Frontend Display Agent",
        ),
        (
            172,
            "Add Test Recipient Configuration",
            "For 'Send Test' button, add interface to specify test email addresses. Allow saving test list (team members) for quick future tests.",
            "Email Testing Agent",
        ),
        (
            173,
            "Implement Rich Text Editor",
            "Replace basic campaign editor with full rich text editor supporting bold, italics, links, images, lists, alignment, and basic formatting like Notion or Google Docs.",
            "Rich Text Editor Agent",
        ),
        (
            174,
            "Add Campaign Preview",
            "Before sending, show preview of exactly how email will appear in inbox. Preview desktop and mobile views, test on different email clients (Gmail, Outlook, Apple Mail).",
            "Email Preview Agent",
        ),
        (
            175,
            "Build Visual Segment Query Builder",
            "Replace 'status:active' text field with visual query builder. Allow selecting field from dropdown, choosing operator (equals, contains, greater than), entering value with autocomplete.",
            "Query Builder Agent",
        ),
        (
            176,
            "Add Campaign Metrics/Analytics",
            "After sending, display comprehensive analytics: sends, deliveries, opens, clicks, unsubscribes, bounces, complaints. Show open rate and click rate over time graphs.",
            "Analytics Display Agent",
        ),
        (
            177,
            "Add Helpful Placeholders to Campaign Fields",
            "Include descriptive placeholder text in form fields like 'Enter subject line (60 characters max)' or 'Select segment or create new' to guide users.",
            "Frontend UX Agent",
        ),
        (
            178,
            "Include Character Count for Subject Lines",
            "Display character count for subject line with warning when approaching limits that cause truncation in email clients (typically 60 chars).",
            "Frontend Validation Agent",
        ),
        (
            179,
            "Replace Not Scheduled with Date Picker",
            "Instead of showing 'Not scheduled' text, show actual date/time picker control where admins can select when campaign should send or save as draft.",
            "Frontend Form Agent",
        ),
        (
            180,
            "Add Autocomplete to Segment Query",
            "When typing segment queries, provide autocomplete suggestions for fields, operators, and values based on available data and common queries.",
            "Autocomplete Agent",
        ),
        (
            181,
            "Implement Inline Validation Messages",
            "Show validation errors directly below form fields as user types, not just on submit. Use red text and icons to indicate errors like 'Email address is required'.",
            "Frontend Validation Agent",
        ),
        (
            182,
            "Create Announcement Banner System",
            "Build system for displaying urgent announcements at top of pages. Support different banner types (info, warning, success), dismissible options, and link to more details.",
            "Notification System Agent",
        ),
        (
            183,
            "Build Internal Messaging/Chat",
            "Add real-time chat system for admin-to-admin and member-to-member communication. Include typing indicators, read receipts, file sharing, and message search.",
            "Chat System Agent",
        ),
        (
            184,
            "Add Discussion Forums/Communities",
            "Create forum system with categories, threads, replies, upvoting, best answer marking, and moderation tools for community discussions.",
            "Forum System Agent",
        ),
        (
            185,
            "Implement Comment System on Resources",
            "Allow members to comment on documents, courses, blog posts. Include threading, @mentions, notifications, and moderation tools.",
            "Comment System Agent",
        ),
        (
            186,
            "Create Member Polls and Surveys",
            "Build poll/survey tool for gathering member feedback. Include question types (multiple choice, rating, free text), logic branching, and response analytics.",
            "Survey Builder Agent",
        ),
        (
            187,
            "Add Newsletter Subscription Management",
            "Let members choose which newsletters they receive. Create preference center with checkboxes for different newsletter types and frequency options.",
            "Subscription Management Agent",
        ),
        (
            188,
            "Build Communication Preferences Center",
            "Central dashboard where members control all communication preferences: emails, push notifications, SMS, frequency limits, topics of interest.",
            "Preferences Management Agent",
        ),
    ]

    # Sub-issues for Feature Request #9 (Learning Management System)
    lms_issues = [
        (
            189,
            "Fix Course Creation Completely",
            "Repair broken course creation functionality. Ensure form loads, file uploads work, modules can be added, and courses actually publish to catalog.",
            "Frontend Bug Fix Agent",
        ),
        (
            190,
            "Implement Course Preview",
            "Build preview interface showing course outline, sample lessons, instructor info, and what learners will experience. Include preview of first video or lesson.",
            "Course Preview Agent",
        ),
        (
            191,
            "Add Course Enrollment Tracking",
            "Track who enrolls in courses, when they enroll, completion status, quiz scores, and time spent. Provide enrollment reports and exports.",
            "Enrollment Tracking Agent",
        ),
        (
            192,
            "Build Progress Visualization",
            "Show progress bars for course completion, module completion, quiz completion. Use segmented progress bars showing which modules are done vs remaining.",
            "Progress Visualization Agent",
        ),
        (
            193,
            "Add Automated Certificate Generation",
            "When learner completes course, auto-generate PDF certificate with their name, course title, completion date, CE credits earned, and digital signature.",
            "Certificate Generator Agent",
        ),
        (
            194,
            "Create Learning Paths with Prerequisites",
            "Allow grouping courses into learning paths (beginner → intermediate → advanced). Enforce prerequisites so users must complete Course A before accessing Course B.",
            "Learning Path Agent",
        ),
        (
            195,
            "Display Course Capacity Limits",
            "Show enrollment limits on course cards like '23/50 enrolled' or 'FULL - Waitlist Available'. Prevent over-enrollment and manage waitlists.",
            "Capacity Management Agent",
        ),
        (
            196,
            "Show Segmented Progress Bars",
            "Instead of single solid progress bar, show segmented bar with each segment representing a module. Visual indication of which modules complete and which remain.",
            "UI Visualization Agent",
        ),
        (
            197,
            "Add Individual Progress Tracking",
            "In Learning Stats section, show each member's personal progress across all courses, not just aggregates. Include completion rate, courses in progress, courses completed.",
            "Progress Analytics Agent",
        ),
        (
            198,
            "Implement Category Filtering",
            "Make course categories like 'Medicare & Medicaid' actually filter the course list when clicked. Add filter pills and clear all filters option.",
            "Frontend Filter Agent",
        ),
        (
            199,
            "Show Module Breakdown in Duration",
            "Instead of just '12 hours', show breakdown like '12 hours total: Module 1 (3hrs), Module 2 (4hrs), Module 3 (5hrs)' so learners know time commitment per section.",
            "Course Details Agent",
        ),
        (
            200,
            "Add Prerequisite Checking Before Enroll",
            "When clicking 'Enroll Now', check if user has completed prerequisites. If not, show message listing required courses and provide links to enroll in those first.",
            "Prerequisite Checker Agent",
        ),
        (
            201,
            "Create Course Builder with SCORM Support",
            "Build course authoring tool supporting SCORM 1.2 and 2004. Allow importing SCORM packages and creating SCORM-compliant courses for compatibility with other LMS systems.",
            "SCORM Integration Agent",
        ),
        (
            202,
            "Build Quiz and Assessment Engine",
            "Create quiz builder with question types: multiple choice, true/false, multiple select, fill-in-blank, essay. Include passing scores, retake limits, randomization.",
            "Assessment Engine Agent",
        ),
        (
            203,
            "Implement Certificate Designer",
            "Visual designer for creating certificate templates. Include placeholders for name, course, date, CE credits. Support logos, signatures, backgrounds.",
            "Certificate Design Agent",
        ),
        (
            204,
            "Add Credit Tracking Across Providers",
            "Track CE credits earned from NABIP courses plus external providers. Maintain transcript showing all credits with course names, dates, providers, credit amounts.",
            "Credit Tracking Agent",
        ),
        (
            205,
            "Create Transcript Generation",
            "Generate official transcript PDF showing all courses completed, dates, scores, credits earned. Include NABIP logo and digital verification code.",
            "Transcript Generator Agent",
        ),
        (
            206,
            "Build Course Recommendations Engine",
            "Use AI/ML to recommend courses based on member's role, previous completions, peers in similar roles, and trending courses in their state/chapter.",
            "Recommendation Engine Agent",
        ),
        (
            207,
            "Integrate Live Webinar Platform",
            "Connect Zoom or Teams for live webinar courses. Auto-create meeting, send join links, track attendance, record sessions, and award CE credits based on attendance.",
            "Webinar Integration Agent",
        ),
    ]

    # Sub-issues for Feature Request #10 (Advanced Reporting System)
    reporting_issues = [
        (
            208,
            "Fix Run Report Execution Completely",
            "Repair the broken report execution engine so reports actually run when clicking 'Run Report' button. Fix backend processing, query generation, and result delivery.",
            "Backend Bug Fix Agent",
        ),
        (
            209,
            "Improve Report Web Viewing",
            "Make reports display properly in web browser with responsive layout. Support desktop and mobile viewing with appropriate column wrapping and horizontal scrolling.",
            "Frontend Display Agent",
        ),
        (
            210,
            "Add Interactive Report Preview",
            "Show live preview of report results with filtering, sorting, and search. Allow interacting with data before deciding to download or schedule.",
            "Interactive Report Agent",
        ),
        (
            211,
            "Enable In-Browser Parameter Editing",
            "Let users modify report parameters (date ranges, filters, grouping) directly in browser and see updated results without re-running entire report.",
            "Parameter Editor Agent",
        ),
        (
            212,
            "Add Scheduled Report Delivery",
            "Allow scheduling reports to run automatically (daily, weekly, monthly) and email results to distribution list. Include options for format (PDF, Excel, CSV).",
            "Report Scheduler Agent",
        ),
        (
            213,
            "Implement Report Sharing with Permissions",
            "Add sharing controls to give specific users or groups access to reports. Set permissions like view-only, can-edit, can-share. Track who has access.",
            "Permissions Management Agent",
        ),
        (
            214,
            "Add Data Type Indicators to Columns",
            "In report builder, show icon or label indicating each column's data type (text, number, date, currency) to help users understand and format data correctly.",
            "Report Builder UI Agent",
        ),
        (
            215,
            "Make Web View Different from Details",
            "The 'Web View' tab should show formatted report in browser, while 'Details' tab shows report configuration. Currently they show the same thing.",
            "Frontend Layout Agent",
        ),
        (
            216,
            "Add Format Preview for Exports",
            "Before downloading, show preview of how export will look in each format (CSV plain text, Excel with formatting, PDF with charts and layout).",
            "Export Preview Agent",
        ),
        (
            217,
            "Show Run History Not Just Last Run",
            "Instead of 'Last run: Never', show complete run history with timestamps, who ran it, parameters used, and links to download previous results.",
            "Report History Agent",
        ),
        (
            218,
            "Add Actual Data Preview",
            "Show preview of actual data the report will return based on current date, not just sample data. Limited to first 100 rows but real query results.",
            "Data Preview Agent",
        ),
        (
            219,
            "Add Sharing Options to Visibility",
            "Report visibility setting should include sharing options like 'Private', 'Shared with team', 'Shared with chapter admins', 'Public to all admins'.",
            "Visibility Settings Agent",
        ),
        (
            220,
            "Create In-Depth Report Templates",
            "Build library of pre-configured reports for common needs: Member Roster, Financial Summary, Event Attendance, Chapter Performance, Renewal Forecast.",
            "Report Templates Agent",
        ),
        (
            221,
            "Add Custom Visual Builder",
            "Create drag-and-drop interface for building report visualizations. Place charts, tables, metrics, filters on canvas and arrange layout visually.",
            "Visual Builder Agent",
        ),
        (
            222,
            "Allow Selecting Data Sources",
            "Let users choose which data to visualize: members, events, financials, courses, campaigns. Support joining multiple data sources in single report.",
            "Data Source Agent",
        ),
        (
            223,
            "Provide 3+ Chart Type Options",
            "For each dataset, offer chart type choices: bar, line, pie, area, scatter, etc. Allow switching between chart types to find best visualization.",
            "Chart Options Agent",
        ),
        (
            224,
            "Enable Custom Graph Creation",
            "Integrate Chart.js or similar library allowing users to create fully custom graphs with their data. Include customization of colors, labels, axes, legends.",
            "Chart Integration Agent",
        ),
        (
            225,
            "Add Report Drill-Down Capabilities",
            "Make report elements clickable to drill into details. Clicking bar in chart shows underlying data, clicking summary number shows transaction list.",
            "Drill-Down Agent",
        ),
        (
            226,
            "Include Export with Formatting Preserved",
            "When exporting to Excel or PDF, maintain all formatting: colors, fonts, chart styles, cell borders, column widths from the web version.",
            "Export Formatting Agent",
        ),
    ]

    # Sub-issues for Feature Request #11 (Event Management System)
    event_issues = [
        (
            227,
            "Fix Event Creation Workflow",
            "Repair completely broken event creation. Ensure form loads, all fields work including date/time pickers, location fields, virtual event settings, pricing, and publishing.",
            "Frontend Bug Fix Agent",
        ),
        (
            228,
            "Show Venue/Location Info Prominently",
            "On event cards and listings, display venue name and city prominently so users can quickly see where event is happening. Include map link.",
            "Frontend Display Agent",
        ),
        (
            229,
            "Add Color Legend for Event Types/Status",
            "Create legend showing what different colors mean for event types (conference=blue, webinar=green, training=orange) and status (upcoming, in-progress, past, cancelled).",
            "UI Components Agent",
        ),
        (
            230,
            "Implement Consistent Event Color Coding",
            "Apply color coding consistently across all event displays: calendar, list view, cards, detail pages. Use same color scheme throughout.",
            "UI Standardization Agent",
        ),
        (
            231,
            "Add Tooltip Explanations for Colors",
            "When hovering over colored event elements, show tooltip explaining what the color means like 'Green = Webinar' or 'Red = Cancelled'.",
            "Frontend UX Agent",
        ),
        (
            232,
            "Include Legend in Event List Header",
            "Display color legend at top of event list page so users can reference what colors mean without having to hover or remember.",
            "Frontend Layout Agent",
        ),
        (
            233,
            "Add Session Selection for Multi-Track Events",
            "For conferences with multiple concurrent sessions, allow attendees to build personal schedule by selecting which sessions to attend in each time slot.",
            "Session Scheduler Agent",
        ),
        (
            234,
            "Implement Meal Preferences and Dietary Restrictions",
            "During registration, collect meal preferences (vegetarian, vegan, gluten-free, kosher, halal, allergies) for catering planning and name badge printing.",
            "Registration Form Agent",
        ),
        (
            235,
            "Add Hotel Room Block Management",
            "Manage hotel room blocks for multi-day events. Track room reservations, show rooms available vs booked, provide hotel booking link, and send reminders to book before deadline.",
            "Hotel Management Agent",
        ),
        (
            236,
            "Enable Companion/Guest Registration",
            "Allow primary registrant to register guests/companions with them. Collect guest info, charge companion fee if applicable, and include guests in attendee count.",
            "Guest Registration Agent",
        ),
        (
            237,
            "Integrate Event Mobile App",
            "Provide mobile app for events with schedule, speaker bios, venue maps, attendee networking, live polling, Q&A, and push notifications for session changes.",
            "Mobile App Integration Agent",
        ),
        (
            238,
            "Add Virtual Event Streaming Integration",
            "Integrate Zoom, Teams, or Webex for virtual/hybrid events. Auto-create meetings, send join links, track virtual attendance separately from in-person, and record sessions.",
            "Virtual Event Agent",
        ),
        (
            239,
            "Implement Post-Event Survey Automation",
            "Automatically send survey to attendees after event ends. Include questions about satisfaction, session quality, speakers, venue, and likelihood to recommend.",
            "Survey Automation Agent",
        ),
        (
            240,
            "Add CPE Credit Tracking and Certificates",
            "Track CPE credits earned at events, automatically generate certificates of attendance showing credits earned, and submit credits to state boards if integrated.",
            "CPE Tracking Agent",
        ),
        (
            241,
            "Create Event Photo Galleries",
            "Upload event photos to gallery, allow attendees to view and download, enable tagging people in photos, and integrate with social media sharing.",
            "Photo Gallery Agent",
        ),
        (
            242,
            "Build Sponsor/Exhibitor Management Portal",
            "Give sponsors access to portal for managing booth details, uploading logos, viewing lead list, sending messages to attendees, and downloading attendee lists (if permitted).",
            "Sponsor Portal Agent",
        ),
        (
            243,
            "Add Event Conversion Funnel",
            "Track and visualize conversion funnel showing how many people viewed event page, started registration, completed registration, and actually attended. Identify drop-off points.",
            "Analytics Funnel Agent",
        ),
    ]

    # Generate all sub-issues
    for issue_num, title, desc, agent in member_mgmt_issues:
        gen.sub_issues.append(gen.create_sub_issue(issue_num, title, desc, 7, agent))

    for issue_num, title, desc, agent in campaign_issues:
        gen.sub_issues.append(gen.create_sub_issue(issue_num, title, desc, 8, agent))

    for issue_num, title, desc, agent in lms_issues:
        gen.sub_issues.append(gen.create_sub_issue(issue_num, title, desc, 9, agent))

    for issue_num, title, desc, agent in reporting_issues:
        gen.sub_issues.append(gen.create_sub_issue(issue_num, title, desc, 10, agent))

    for issue_num, title, desc, agent in event_issues:
        gen.sub_issues.append(gen.create_sub_issue(issue_num, title, desc, 11, agent))

    return gen


def main():
    """Generate and output all issues."""
    generator = generate_all_issues()

    output = {
        "feature_requests": generator.feature_requests,
        "sub_issues": generator.sub_issues,
        "summary": {
            "total_feature_requests": len(generator.feature_requests),
            "total_sub_issues": len(generator.sub_issues),
            "feature_request_numbers": [
                fr["number"] for fr in generator.feature_requests
            ],
            "sub_issue_range": f"{generator.sub_issues[0]['number']}-{generator.sub_issues[-1]['number']}",
        },
    }

    # Write to JSON file
    with open("github_issues.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"✅ Generated {len(generator.feature_requests)} feature requests")
    print(f"✅ Generated {len(generator.sub_issues)} sub-issues")
    print(f"✅ Output written to github_issues.json")

    # Also create a markdown summary
    with open("github_issues_summary.md", "w") as f:
        f.write("# GitHub Issues Summary\n\n")
        f.write("## Feature Requests\n\n")
        for fr in generator.feature_requests:
            f.write(f"### {fr['title']}\n")
            f.write(f"- **Number**: #{fr['number']}\n")
            f.write(f"- **Labels**: {', '.join(fr['labels'])}\n")
            f.write(f"- **Assigned Agent**: {fr['assigned_agent']}\n\n")

        f.write("\n## Sub-Issues Summary\n\n")
        f.write(f"Total sub-issues: {len(generator.sub_issues)}\n\n")

        # Group by parent feature
        by_parent = {}
        for issue in generator.sub_issues:
            parent = issue["parent_feature"]
            if parent not in by_parent:
                by_parent[parent] = []
            by_parent[parent].append(issue)

        for parent in sorted(by_parent.keys()):
            f.write(
                f"\n### Feature Request #{parent} ({len(by_parent[parent])} sub-issues)\n\n"
            )
            for issue in by_parent[parent]:
                f.write(f"- **#{issue['number']}**: {issue['title']}\n")
                f.write(f"  - Agent: {issue['assigned_agent']}\n")

    print("✅ Summary written to github_issues_summary.md")


if __name__ == "__main__":
    main()
