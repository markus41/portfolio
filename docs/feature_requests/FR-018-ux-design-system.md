# Feature Request #18: User Experience & Design System

**Title:** Complete Design System with Accessibility and Branding

**Feature Category:** UX/Design Enhancement

**Priority:** Medium-High

**Estimated Time:** 4-5 weeks

## Problem Statement

System has inconsistent design: mixed fonts (need all sans-serif), missing NABIP color gradient, inconsistent status badges, poor empty states, no loading skeletons, missing hover states, and accessibility issues. Onboarding experience also lacking.

## Proposed Solution

Build comprehensive design system:
- Convert all fonts to sans-serif
- Apply NABIP color gradient to dashboard greeting and key elements
- Standardize all status badges
- Create helpful empty states with illustrations
- Add loading skeletons for all async content
- Implement consistent hover states throughout
- Build accessible design system (WCAG 2.1 AA)
- Add dark mode toggle
- Create animated onboarding tour
- Add accessibility controls

## Alternatives Considered

1. **Using existing UI library** - doesn't match NABIP brand
2. **No design system** - creates inconsistency
3. **Minimal accessibility** - legal/ethical issues

## Expected Impact

- **Priority:** Medium-High
- **Affects:** All users
- **Estimated time:** 4-5 weeks
- **Impact:** Increases user satisfaction by ~40%

## Technical Considerations

- Storybook component library
- Design tokens for theming
- CSS-in-JS or Tailwind configuration
- Accessibility testing suite
- Lazy loading for images
- Animation performance optimizations

## Sub-Issues

### Visual Improvements (Issues #370-377)

#### Issue #370: Add Visual Status Indicators to Campaign Cards

**Description:** Show color-coded status badges on campaign cards

**Implementation Details:**
- Gray badge for Draft status
- Blue badge for Scheduled (with date)
- Green badge for Sent (with date)
- Make status prominent and consistent

**Technical Requirements:**
- Badge component library
- Status color mapping
- Date formatting utilities

**Acceptance Criteria:**
- [ ] Draft campaigns show gray badge
- [ ] Scheduled campaigns show blue badge with date
- [ ] Sent campaigns show green badge with date
- [ ] Status badges visible and prominent
- [ ] Consistent styling across all cards
- [ ] Accessible color contrast ratios

**Recommended Agent:** UI component specialist or visual design agent

---

#### Issue #371: Add Action Menus to Chapter Cards

**Description:** Add three-dot menu with actions to chapter cards

**Implementation Details:**
- Menu button in top-right corner
- Actions: Edit, View Details, Message Leaders, Export Data, Deactivate
- Dropdown menu on click

**Technical Requirements:**
- Dropdown menu component
- Icon library
- Permission-based menu items
- Click-outside detection

**Acceptance Criteria:**
- [ ] Three-dot menu button in top-right
- [ ] Menu opens on click
- [ ] All actions listed
- [ ] Actions execute correctly
- [ ] Permission-based visibility
- [ ] Menu closes on action or click-outside
- [ ] Keyboard accessible

**Recommended Agent:** Menu component specialist or interaction design agent

---

#### Issue #372: Add Instructor Info to Course Cards

**Description:** Display instructor name and photo on course cards

**Implementation Details:**
- Show instructor photo
- Display instructor name
- Build credibility and help course selection

**Technical Requirements:**
- Image optimization
- Avatar component
- Fallback for missing photos
- Layout adjustments

**Acceptance Criteria:**
- [ ] Instructor photo displayed
- [ ] Instructor name shown
- [ ] Fallback avatar for missing photos
- [ ] Photos optimized and fast-loading
- [ ] Layout balanced and attractive
- [ ] Touch-friendly on mobile

**Recommended Agent:** Card design specialist or instructor profile agent

---

#### Issue #373: Add Hover States to All Cards

**Description:** Cards should respond to hover with visual feedback

**Implementation Details:**
- Card lifts slightly (box shadow)
- Border highlight appears
- Action buttons reveal on hover
- Interactive and responsive feel

**Technical Requirements:**
- CSS transitions
- Box shadow styling
- Button reveal animations
- Performance optimization

**Acceptance Criteria:**
- [ ] Cards lift on hover
- [ ] Border highlight visible
- [ ] Action buttons reveal smoothly
- [ ] Transitions perform at 60fps
- [ ] Works across browsers
- [ ] Touch devices show actions always

**Recommended Agent:** Animation specialist or hover interaction agent

---

#### Issue #374: Improve Member Not Found Page

**Description:** Replace stark error with friendly experience

**Implementation Details:**
- Friendly illustration
- Suggestions for next steps
- Search again option
- Check spelling reminder
- Browse member directory link
- Quick add member button

**Technical Requirements:**
- Illustration assets
- Suggestion logic
- Navigation links
- Form integration

**Acceptance Criteria:**
- [ ] Friendly illustration displayed
- [ ] Clear suggestions provided
- [ ] Search again option available
- [ ] Browse directory link functional
- [ ] Add member button visible (if permitted)
- [ ] Helpful, not frustrating tone

**Recommended Agent:** Error page specialist or empty state designer

---

#### Issue #375: Add Suggestions for Next Steps on Error Pages

**Description:** Provide actionable next steps on all error pages

**Implementation Details:**
- "Try: searching for similar name"
- "Browse by chapter"
- "Contact support"
- Context-specific suggestions

**Technical Requirements:**
- Error context detection
- Dynamic suggestion generation
- Link generation
- Help text system

**Acceptance Criteria:**
- [ ] All error pages have suggestions
- [ ] Suggestions context-appropriate
- [ ] Links functional
- [ ] Support contact easy to find
- [ ] Tone helpful and encouraging

**Recommended Agent:** Error handling specialist or UX copy agent

---

#### Issue #376: Add Illustrations to Error Pages

**Description:** Use friendly illustrations on error/empty states

**Implementation Details:**
- Consistent illustration style
- Match NABIP brand
- Reduce starkness of errors
- Engaging visual design

**Technical Requirements:**
- Illustration library
- SVG optimization
- Lazy loading
- Responsive sizing

**Acceptance Criteria:**
- [ ] Illustrations on all error pages
- [ ] Consistent visual style
- [ ] NABIP brand alignment
- [ ] Fast-loading SVGs
- [ ] Responsive sizing
- [ ] Accessible alt text

**Recommended Agent:** Illustration specialist or visual content agent

---

#### Issue #377: Show Recent Members on Empty States

**Description:** Provide suggestions on member not found page

**Implementation Details:**
- Show "Recently Viewed Members"
- Show "Members in Same Chapter"
- Provide path forward instead of dead end

**Technical Requirements:**
- Recently viewed tracking
- Chapter membership queries
- Dynamic content loading

**Acceptance Criteria:**
- [ ] Recently viewed members shown
- [ ] Same chapter members displayed
- [ ] Links functional
- [ ] Performance acceptable
- [ ] Privacy respecting
- [ ] Helpful for navigation

**Recommended Agent:** Empty state specialist or recommendation engine agent

---

### Data Formatting (Issues #378-382)

#### Issue #378: Standardize Number Formatting

**Description:** Use consistent number formatting throughout

**Implementation Details:**
- 1,247 members (with comma)
- $3,940 (currency with comma)
- 23.5% (percentage to 1 decimal)
- Pick one style and use everywhere

**Technical Requirements:**
- Number formatting utility
- Locale support
- Configuration management

**Acceptance Criteria:**
- [ ] All numbers use comma separators
- [ ] Currency format consistent
- [ ] Percentage format consistent
- [ ] Decimal places consistent
- [ ] Locale-aware formatting
- [ ] Applied throughout app

**Recommended Agent:** Formatting specialist or i18n agent

---

#### Issue #379: Add Trend Arrows to Percentages

**Description:** Show direction of change with color-coded arrows

**Implementation Details:**
- ↑ 23% (increase, green)
- ↓ 5% (decrease, red)
- Color code based on good/bad

**Technical Requirements:**
- Arrow icon components
- Color logic (good vs bad change)
- Accessibility considerations

**Acceptance Criteria:**
- [ ] Up arrows for increases
- [ ] Down arrows for decreases
- [ ] Green for positive changes
- [ ] Red for negative changes
- [ ] Accessible to colorblind users
- [ ] Screen reader friendly

**Recommended Agent:** Data visualization agent or icon specialist

---

#### Issue #380: Standardize Dollar Amount Formatting

**Description:** Use consistent currency formatting

**Implementation Details:**
- Always $3,940.00 OR always $3,940
- Pick one style
- Include currency symbol
- Comma separators
- Consistent decimals

**Technical Requirements:**
- Currency formatter utility
- Configuration setting
- Locale support

**Acceptance Criteria:**
- [ ] Currency format consistent
- [ ] Decimals consistent (all or none)
- [ ] Currency symbol always present
- [ ] Comma separators used
- [ ] Locale-aware formatting

**Recommended Agent:** Currency formatting specialist

---

#### Issue #381: Use Consistent Date Formats

**Description:** Pick one date format and use throughout

**Implementation Details:**
- MM/DD/YYYY or Month DD, YYYY
- Include time when relevant
- Consistent format (12:00 PM or 12:00)

**Technical Requirements:**
- Date formatting utility
- Timezone handling
- Locale support

**Acceptance Criteria:**
- [ ] Date format consistent throughout
- [ ] Time format consistent
- [ ] Timezone displayed when relevant
- [ ] Locale-aware formatting
- [ ] Relative dates used appropriately

**Recommended Agent:** Date/time formatting specialist

---

#### Issue #382: Standardize Status Text Capitalization

**Description:** Decide on status text capitalization

**Implementation Details:**
- Either "Active" (title case)
- Or "ACTIVE" (all caps)
- Use consistently across all status badges

**Technical Requirements:**
- Status text transformation
- Component library updates

**Acceptance Criteria:**
- [ ] Status capitalization consistent
- [ ] Applied to all badges
- [ ] Applied to all status displays
- [ ] Documentation updated

**Recommended Agent:** Text formatting specialist

---

### Performance & UX (Issues #383-388)

#### Issue #383: Add Loading Skeletons

**Description:** Show placeholder shapes while data loads

**Implementation Details:**
- Replace blank space with skeletons
- Gray placeholder shapes
- Match expected content layout
- Feels faster and less broken

**Technical Requirements:**
- Skeleton component library
- Layout matching
- Animation performance

**Acceptance Criteria:**
- [ ] Skeletons for all async content
- [ ] Match actual content layout
- [ ] Smooth shimmer animation
- [ ] No layout shift on load
- [ ] Performance optimized

**Recommended Agent:** Loading state specialist or skeleton UI agent

---

#### Issue #384: Add Progress Indicators for Long Operations

**Description:** Show progress for operations > 2 seconds

**Implementation Details:**
- Progress bar or spinner
- Percentage complete
- Estimated time remaining
- For imports, reports, bulk operations

**Technical Requirements:**
- Progress tracking backend
- Progress bar component
- Time estimation algorithm

**Acceptance Criteria:**
- [ ] Progress shown for long operations
- [ ] Percentage accurate
- [ ] Time estimate reasonable
- [ ] Can cancel if appropriate
- [ ] Clear completion indicator

**Recommended Agent:** Progress tracking specialist

---

#### Issue #385: Implement Optimistic UI Updates

**Description:** Show changes immediately, revert on failure

**Implementation Details:**
- Immediately show change in UI
- Save in background
- Revert if save fails
- Makes app feel instant

**Technical Requirements:**
- Optimistic update pattern
- Rollback mechanism
- Error handling
- State management

**Acceptance Criteria:**
- [ ] Changes appear immediately
- [ ] Background save occurs
- [ ] Rollback on failure
- [ ] Error notification on failure
- [ ] User can retry
- [ ] Feels instantaneous

**Recommended Agent:** State management specialist or optimistic UI agent

---

#### Issue #386: Make Charts Animate Instead of Redrawing

**Description:** Animate transitions in chart data

**Implementation Details:**
- Animate from old values to new
- Helps users see what changed
- Smooth transitions

**Technical Requirements:**
- Chart animation library
- Transition timing
- Performance optimization

**Acceptance Criteria:**
- [ ] Charts animate on data change
- [ ] Smooth 60fps animations
- [ ] Easy to see what changed
- [ ] Can disable for accessibility
- [ ] Works across chart types

**Recommended Agent:** Chart animation specialist

---

#### Issue #387: Add Virtualization for Long Lists

**Description:** Only render items in viewport for lists > 100 items

**Implementation Details:**
- Virtual scrolling
- Only render visible items
- Dramatically improves performance

**Technical Requirements:**
- Virtual scroll library
- Height calculation
- Scroll position management

**Acceptance Criteria:**
- [ ] Long lists use virtualization
- [ ] Smooth scrolling
- [ ] All items accessible
- [ ] Search/filter works
- [ ] Performance significantly improved

**Recommended Agent:** Performance optimization specialist or virtual scroll agent

---

#### Issue #388: Implement Lazy Loading for Images

**Description:** Load images only when scrolled into view

**Implementation Details:**
- Don't load until in viewport
- Speeds up initial page load
- Reduces data usage
- Use placeholder or blur while loading

**Technical Requirements:**
- Intersection Observer API
- Placeholder component
- Progressive image loading

**Acceptance Criteria:**
- [ ] Images load on scroll-in
- [ ] Placeholder shown while loading
- [ ] Smooth appearance transition
- [ ] Initial page load faster
- [ ] Works across browsers

**Recommended Agent:** Image optimization specialist or lazy loading agent

---

### Branding & Typography (Issues #389-392)

#### Issue #389: Change All Fonts to Sans-Serif

**Description:** Replace all serif fonts with sans-serif

**Implementation Details:**
- Use font stack: Inter, Helvetica, Arial, sans-serif
- Modern, clean look
- Consistent throughout

**Technical Requirements:**
- CSS font-family updates
- Font file loading
- Fallback fonts

**Acceptance Criteria:**
- [ ] All text uses sans-serif
- [ ] Font stack properly configured
- [ ] Font files loaded efficiently
- [ ] Fallbacks work correctly
- [ ] No FOIT (Flash of Invisible Text)

**Recommended Agent:** Typography specialist

---

#### Issue #390: Implement NABIP Color Gradient on Greeting

**Description:** Apply Navy-to-Teal gradient on dashboard greeting

**Implementation Details:**
- Gradient on "Good evening, markus41!"
- Navy #003366 to Teal #008B8B
- Reinforces NABIP brand colors

**Technical Requirements:**
- CSS gradient implementation
- Brand color configuration

**Acceptance Criteria:**
- [ ] Greeting has gradient
- [ ] Navy to Teal colors used
- [ ] Gradient smooth and attractive
- [ ] Text readable over gradient
- [ ] Consistent across browsers

**Recommended Agent:** Branding specialist or gradient design agent

---

#### Issue #391: Apply Consistent Font Sizing Hierarchy

**Description:** Establish and apply consistent font sizes

**Implementation Details:**
- H1=32px, H2=24px, H3=20px
- Body=16px, Small=14px
- Use throughout application

**Technical Requirements:**
- Typography scale configuration
- CSS updates
- Component library updates

**Acceptance Criteria:**
- [ ] Font scale defined
- [ ] Applied throughout app
- [ ] Visual hierarchy clear
- [ ] Responsive scaling for mobile
- [ ] Documentation updated

**Recommended Agent:** Typography hierarchy specialist

---

#### Issue #392: Ensure Proper Font Weight Variations

**Description:** Use proper font weights consistently

**Implementation Details:**
- Regular (400) for body
- Medium (500) for emphasis
- Semibold (600) for subheadings
- Bold (700) for headings

**Technical Requirements:**
- Font files with multiple weights
- CSS font-weight updates
- Weight mapping

**Acceptance Criteria:**
- [ ] All weights available
- [ ] Used consistently
- [ ] Visual hierarchy maintained
- [ ] Font files optimized
- [ ] Fallback weights defined

**Recommended Agent:** Typography weight specialist

---

### Onboarding (Issues #393-398)

#### Issue #393: Copy Getting Started Flow from AMSdemo

**Description:** Replicate onboarding tour from AMSdemo.dev

**Implementation Details:**
- Interactive tour showing key features
- Guide users through navigation
- Engaging and helpful

**Technical Requirements:**
- Onboarding library (e.g., Intro.js, Shepherd)
- Tour step definitions
- Progress tracking

**Acceptance Criteria:**
- [ ] Tour available for new users
- [ ] Covers key features
- [ ] Interactive and engaging
- [ ] Can skip or dismiss
- [ ] Progress saved

**Recommended Agent:** Onboarding specialist or tutorial flow agent

---

#### Issue #394: Create Non-Intrusive Walkthrough Tutorial

**Description:** Guide users without blocking interface

**Implementation Details:**
- Use tooltips, arrows, highlights
- Allow continuing work while learning
- Non-blocking design

**Technical Requirements:**
- Tooltip positioning
- Highlight overlay
- State management

**Acceptance Criteria:**
- [ ] Tutorial doesn't block interface
- [ ] Tooltips positioned correctly
- [ ] Can interact while learning
- [ ] Clear visual guidance
- [ ] Easy to follow

**Recommended Agent:** Tutorial design specialist

---

#### Issue #395: Make Tutorial Dismissible

**Description:** Add "Don't show again" option

**Implementation Details:**
- Respect user choice
- Don't force on every login
- Provide restart from settings

**Technical Requirements:**
- Preference storage
- Settings integration

**Acceptance Criteria:**
- [ ] "Don't show again" checkbox
- [ ] Preference remembered
- [ ] Can restart from settings
- [ ] Clear opt-out mechanism

**Recommended Agent:** User preference specialist

---

#### Issue #396: Track Tutorial Completion Metrics

**Description:** Track which steps users complete

**Implementation Details:**
- Track step completion
- Track drop-off points
- Track completion rate
- Use data to improve

**Technical Requirements:**
- Analytics integration
- Event tracking
- Reporting dashboard

**Acceptance Criteria:**
- [ ] Step completion tracked
- [ ] Drop-off points identified
- [ ] Completion rate calculated
- [ ] Reports available
- [ ] Data actionable

**Recommended Agent:** Analytics specialist or metrics tracking agent

---

#### Issue #397: Allow Completing Tutorial Over Time

**Description:** Don't require completing in one session

**Implementation Details:**
- Save progress
- Allow resuming later
- Learn at own pace

**Technical Requirements:**
- Progress state management
- Session persistence

**Acceptance Criteria:**
- [ ] Progress saved between sessions
- [ ] Can resume where left off
- [ ] No pressure to complete immediately
- [ ] Clear indication of progress

**Recommended Agent:** Tutorial state management specialist

---

#### Issue #398: Add Progress Indicator for Onboarding

**Description:** Show "Step 3 of 7" or progress bar

**Implementation Details:**
- Clear progress indication
- Know how much remains
- Reduces abandonment

**Technical Requirements:**
- Progress component
- Step tracking

**Acceptance Criteria:**
- [ ] Progress clearly visible
- [ ] Accurate step count
- [ ] Updates in real-time
- [ ] Motivating design

**Recommended Agent:** Progress indicator specialist

---

### Quick Actions (Issues #399-404)

#### Issue #399: Include Contextual Help Tooltips

**Description:** Add question mark icons with explanations

**Implementation Details:**
- Question mark icons next to complex fields
- Tooltips with explanations
- Help in context without clutter

**Technical Requirements:**
- Tooltip component
- Help text management
- Icon library

**Acceptance Criteria:**
- [ ] Help icons next to complex fields
- [ ] Tooltips clear and helpful
- [ ] Don't clutter interface
- [ ] Accessible via keyboard
- [ ] Screen reader compatible

**Recommended Agent:** Help content specialist or tooltip agent

---

#### Issue #400: Add Floating Quick Actions Button

**Description:** FAB in bottom-right with common actions

**Implementation Details:**
- Floating action button
- Hover to show menu
- Context-based actions

**Technical Requirements:**
- FAB component
- Menu positioning
- Z-index management

**Acceptance Criteria:**
- [ ] FAB visible in bottom-right
- [ ] Doesn't obstruct content
- [ ] Menu shows on hover/click
- [ ] Actions contextual
- [ ] Mobile-friendly

**Recommended Agent:** FAB component specialist or quick actions agent

---

#### Issue #401: Create Quick Actions Menu

**Description:** Show contextual actions in FAB menu

**Implementation Details:**
- On members page: "Add Member", "Import", "Export"
- Actions relevant to current page

**Technical Requirements:**
- Context detection
- Menu item generation
- Permission checks

**Acceptance Criteria:**
- [ ] Menu shows relevant actions
- [ ] Actions functional
- [ ] Permission-based visibility
- [ ] Clear icons and labels

**Recommended Agent:** Context-aware menu specialist

---

#### Issue #402: Make Quick Actions Contextual

**Description:** Change actions based on page and role

**Implementation Details:**
- Admins see more options
- Actions relevant to current task
- Intelligent action suggestions

**Technical Requirements:**
- Role detection
- Context analysis
- Dynamic menu generation

**Acceptance Criteria:**
- [ ] Actions change by page
- [ ] Actions respect user role
- [ ] Suggestions intelligent
- [ ] Performance acceptable

**Recommended Agent:** Contextual action specialist

---

#### Issue #403: Include Keyboard Shortcuts for Quick Actions

**Description:** Add keyboard shortcuts and display in menu

**Implementation Details:**
- "Ctrl+N" for New Member
- "Ctrl+I" for Import
- Display shortcuts in menu

**Technical Requirements:**
- Keyboard event handling
- Shortcut registration
- Shortcut documentation

**Acceptance Criteria:**
- [ ] Shortcuts functional
- [ ] Displayed in menu
- [ ] Don't conflict with browser
- [ ] Customizable if possible
- [ ] Help documentation available

**Recommended Agent:** Keyboard shortcut specialist

---

#### Issue #404: Add Recent Actions History

**Description:** Show recently used actions at top

**Implementation Details:**
- Learn user behavior
- Prioritize common actions
- Fast repeat access

**Technical Requirements:**
- Action history tracking
- Sorting algorithm
- Storage management

**Acceptance Criteria:**
- [ ] Recent actions tracked
- [ ] Displayed at menu top
- [ ] Sorted by frequency/recency
- [ ] Helpful for power users

**Recommended Agent:** User behavior tracking specialist

---

### Advanced Features (Issues #405-414)

#### Issue #405: Add Animated Onboarding Tour

**Description:** Smooth animated tour with zoom and spotlights

**Implementation Details:**
- Zoom-in on features
- Spotlight highlighting
- Progressive disclosure
- Celebration on completion

**Technical Requirements:**
- Animation library
- Spotlight component
- Celebration animation

**Acceptance Criteria:**
- [ ] Smooth animations
- [ ] Features highlighted clearly
- [ ] Progressive flow
- [ ] Completion celebration
- [ ] 60fps performance

**Recommended Agent:** Animation specialist or onboarding animator

---

#### Issue #406: Add Dark Mode Toggle

**Description:** Implement dark mode with toggle

**Implementation Details:**
- Dark backgrounds with light text
- Sufficient contrast
- Test all components

**Technical Requirements:**
- CSS color variables
- Theme switching logic
- Contrast verification

**Acceptance Criteria:**
- [ ] Dark mode functional
- [ ] Toggle in settings
- [ ] All components work in dark mode
- [ ] Contrast meets standards
- [ ] Preference persisted

**Recommended Agent:** Dark mode specialist or theming agent

---

#### Issue #407: Add Accessibility Controls

**Description:** Accessibility toolbar with options

**Implementation Details:**
- Increase font size
- Increase contrast
- Reduce motion/animations
- Screen reader optimizations

**Technical Requirements:**
- Accessibility toolbar component
- Setting application logic
- Preference storage

**Acceptance Criteria:**
- [ ] Toolbar accessible
- [ ] Font size adjustable
- [ ] Contrast adjustable
- [ ] Motion reducible
- [ ] Screen reader mode
- [ ] Preferences persist

**Recommended Agent:** Accessibility specialist or a11y agent

---

#### Issue #408: Add Language Selection

**Description:** Support multiple languages

**Implementation Details:**
- Start with English and Spanish
- Language selector in header
- Use i18n library

**Technical Requirements:**
- i18n library (e.g., i18next)
- Translation files
- Language switcher component

**Acceptance Criteria:**
- [ ] English fully supported
- [ ] Spanish fully supported
- [ ] Language switcher visible
- [ ] Translations complete
- [ ] Date/number formats localized

**Recommended Agent:** Internationalization specialist or i18n agent

---

#### Issue #409: Add Timezone Auto-Detection

**Description:** Detect and use user's timezone

**Implementation Details:**
- Auto-detect timezone
- Display times in local timezone
- Allow manual override

**Technical Requirements:**
- Timezone detection
- Date conversion logic
- Timezone selector component

**Acceptance Criteria:**
- [ ] Timezone auto-detected
- [ ] Times displayed in local timezone
- [ ] Manual override available
- [ ] Conversions accurate
- [ ] Clear timezone indicators

**Recommended Agent:** Timezone specialist or temporal data agent

---

#### Issue #410: Add Session Timeout Warnings

**Description:** Warn before session expires

**Implementation Details:**
- "Your session will expire in 2 minutes"
- Click to stay logged in
- Prevent losing unsaved work

**Technical Requirements:**
- Session monitoring
- Warning modal
- Session extension API

**Acceptance Criteria:**
- [ ] Warning shows before timeout
- [ ] Can extend session
- [ ] Unsaved work preserved
- [ ] Clear timing indication
- [ ] Auto-save if possible

**Recommended Agent:** Session management specialist

---

#### Issue #411: Ensure Breadcrumb Navigation Throughout

**Description:** Breadcrumbs on every page deeper than 2 levels

**Implementation Details:**
- Keep users oriented
- Quick navigation to parent sections

**Technical Requirements:**
- Breadcrumb component
- Route tracking
- Dynamic generation

**Acceptance Criteria:**
- [ ] Breadcrumbs on deep pages
- [ ] Accurate path representation
- [ ] Clickable navigation
- [ ] Mobile-friendly
- [ ] Accessible

**Recommended Agent:** Navigation specialist or breadcrumb agent

---

#### Issue #412: Add Quick Feedback Widget

**Description:** "Was this helpful?" widget on pages

**Implementation Details:**
- Small feedback widget
- Quick issue reporting
- Don't leave page

**Technical Requirements:**
- Feedback widget component
- Feedback submission API
- Analytics integration

**Acceptance Criteria:**
- [ ] Widget visible but unobtrusive
- [ ] Yes/No feedback captured
- [ ] Optional comments
- [ ] Thank you confirmation
- [ ] Data collected for analysis

**Recommended Agent:** Feedback widget specialist

---

#### Issue #413: Integrate Live Chat Support

**Description:** Embed live chat widget

**Implementation Details:**
- Intercom or Drift integration
- Real-time help
- Show online/offline status

**Technical Requirements:**
- Chat widget integration
- Support team training
- Analytics integration

**Acceptance Criteria:**
- [ ] Chat widget embedded
- [ ] Online/offline status shown
- [ ] Messages delivered reliably
- [ ] Support team responsive
- [ ] Mobile-friendly

**Recommended Agent:** Live chat integration specialist

---

#### Issue #414: Add Contextual Help Videos

**Description:** Short tutorial videos on complex pages

**Implementation Details:**
- 30-90 second videos
- Show how to use features
- Skippable with transcripts

**Technical Requirements:**
- Video hosting
- Video player component
- Transcript generation

**Acceptance Criteria:**
- [ ] Videos on complex pages
- [ ] Clear and concise
- [ ] Skippable
- [ ] Transcripts available
- [ ] Fast loading

**Recommended Agent:** Video content specialist or tutorial video agent

---

## Implementation Priority

1. **Critical Foundation:**
   - Issues #378-382: Data Formatting
   - Issues #389-392: Branding & Typography
   - Issue #383: Loading Skeletons

2. **High Priority Visual:**
   - Issues #370-373: Card Improvements
   - Issues #374-377: Error Page Improvements
   - Issues #384-388: Performance & UX

3. **Medium Priority Onboarding:**
   - Issues #393-398: Onboarding System
   - Issues #399-404: Quick Actions

4. **Advanced Features:**
   - Issues #405-414: Advanced UX Features

## Testing Strategy

- Visual regression testing
- Accessibility testing (WCAG 2.1 AA)
- Cross-browser testing
- Mobile device testing
- Performance testing
- User acceptance testing
- A/B testing for design changes

## Documentation Requirements

- Design system documentation
- Component library (Storybook)
- Accessibility guidelines
- Brand guidelines
- Animation guidelines
- User onboarding materials

## Success Metrics

- User satisfaction increase by 40%
- Accessibility score above 95
- Design consistency score above 90
- Onboarding completion rate above 70%
- Support ticket reduction by 30%
- Task completion time reduction by 25%
- Mobile satisfaction score above 4.5/5
