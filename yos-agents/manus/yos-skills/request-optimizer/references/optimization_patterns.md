# Request Optimization Patterns

This document provides detailed patterns for transforming different types of requests.

## Pattern 1: Risk Reduction

Identify potentially destructive operations and add safety measures.

**Triggers:**
- Deletion keywords: "delete", "remove", "clear", "wipe"
- Bulk operations: "all", "everything", "entire"
- Overwrite operations: "replace all", "change everything"

**Transformation:**
```
Before: "Delete all files in the project"
After: "Create a backup of all files in /backup/[timestamp], then delete files from the project directory with confirmation before proceeding"
```

**Safety measures to add:**
- Backup before deletion
- Confirmation prompts
- Scope limitation (specific directories/files)
- Dry-run option
- Reversibility check

## Pattern 2: Cost Optimization

Reduce computational and credit costs by suggesting efficient alternatives.

**Triggers:**
- Parallel processing keywords: "for each", "all", "every"
- Large-scale operations: "comprehensive", "exhaustive", "complete"
- Redundant operations: multiple similar searches, repeated API calls

**Transformation:**
```
Before: "Research everything about 100 companies"
After: "Research 100 companies focusing on [3 specific data points]. Use batch API calls where possible. Consider starting with 10 companies to validate the approach before scaling."
```

**Cost reduction strategies:**
- Batch operations instead of individual calls
- Focused scope instead of exhaustive research
- Incremental approach (pilot → scale)
- Caching and reuse of results
- Alternative tools or methods

## Pattern 3: Auto-Execution Enablement

Transform ambiguous requests into clear, actionable tasks.

**Triggers:**
- Vague pronouns: "this", "that", "it"
- Missing context: "make it better", "fix the issue"
- Unclear scope: "update the app"

**Transformation:**
```
Before: "Make this better"
After: "Improve the [specific component] by: 1) Enhancing [aspect A] to achieve [goal], 2) Optimizing [aspect B] for [metric], 3) Refactoring [aspect C] to follow [pattern]"
```

**Clarification strategies:**
- Identify specific targets (files, components, features)
- Define concrete objectives and success criteria
- Specify measurable improvements
- Add context from recent conversation history

## Pattern 4: Structure Enhancement

Break down complex or vague requests into well-structured steps.

**Triggers:**
- Multiple objectives in one request
- Complex workflows
- Interdependent changes
- Vague action verbs: "update", "change", "modify"

**Transformation:**
```
Before: "Change the login flow"
After: "Update the login flow in 4 steps:
1. Modify authentication logic in auth.ts to support OAuth
2. Update LoginComponent UI to add OAuth buttons
3. Update translation strings for new UI elements
4. Update styling to match design system
5. Test the complete flow end-to-end"
```

**Structuring strategies:**
- Break into sequential steps
- Identify dependencies (A must complete before B)
- Separate concerns (logic → UI → translations → styling)
- Add validation/testing steps
- Number steps for clarity

## Pattern 5: App Development Changes

Transform vague change requests into specific, sequenced updates.

**Triggers:**
- UI/UX changes: "change the design", "update the layout"
- Feature modifications: "add this feature", "change how X works"
- Styling updates: "make it look better", "update colors"

**Transformation:**
```
Before: "Change the dashboard to show more data"
After: "Update dashboard feature:
1. Modify DashboardComponent to add 3 new data widgets (UserStats, RevenueChart, ActivityFeed)
2. Update dashboard API endpoint to fetch additional data
3. Add translation strings for new widget labels
4. Update dashboard.css to accommodate new layout
5. Ensure responsive design works on mobile
6. Update tests for new components"
```

**App change strategies:**
- Identify affected components/files
- Specify what changes and why
- Sequence: features → data → translations → styling → tests
- Consider cascade effects (UI changes affect translations)
- Add testing and validation steps

## Pattern 6: Variant Suggestion

When a request is immature or could be approached multiple ways, present alternatives.

**Triggers:**
- Underspecified goals: "help me with X"
- Multiple valid approaches
- Unclear priorities
- Missing key decisions

**Transformation:**
```
Before: "Help me build a website"
After: "I can help you build a website. Here are 3 approaches:

Option A: Static landing page (fast, low cost, no backend)
- Best for: Marketing, portfolios, simple content
- Timeline: 1-2 hours
- Cost: Low

Option B: Dynamic web app with database (full-featured)
- Best for: User accounts, data management, interactive features
- Timeline: 4-8 hours
- Cost: Medium

Option C: No-code solution (fastest, limited customization)
- Best for: Quick prototypes, non-technical users
- Timeline: 30 minutes
- Cost: Very low

Which approach fits your needs?"
```

**Variant suggestion strategies:**
- Present 2-4 concrete options
- Explain trade-offs (time, cost, features)
- Provide selection criteria
- Ask clarifying question to guide choice
