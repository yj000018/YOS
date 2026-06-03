# Request Optimization Examples

Real-world examples of request transformations across different scenarios.

## Example 1: File Operations

**Original:** "Delete all my old files"

**Issues:**
- High risk (irreversible deletion)
- Ambiguous scope ("old" is undefined)
- No safety measures

**Optimized:**
```
Create a backup of files older than 30 days to /backup/[timestamp]/. 
Then present a list of files to be deleted with their sizes and last modified dates. 
Request confirmation before proceeding with deletion.
If confirmed, delete files and provide a summary report.
```

## Example 2: Research Task

**Original:** "Research AI companies"

**Issues:**
- Expensive (unbounded scope)
- Vague objectives
- Unclear deliverable

**Optimized:**
```
Research top 10 AI companies focusing on:
1. Company overview (founding year, size, funding)
2. Primary AI products/services
3. Recent news (past 6 months)

Deliver results as a structured table with sources.
Estimated cost: ~50 credits. Proceed?
```

## Example 3: App Feature Change

**Original:** "Change the login to use Google"

**Issues:**
- Missing implementation details
- No consideration of cascade effects
- Unclear scope

**Optimized:**
```
Add Google OAuth to login flow:

Step 1: Backend Setup
- Install and configure OAuth library
- Add Google OAuth credentials to environment
- Create /auth/google/callback endpoint
- Update authentication middleware

Step 2: Frontend Updates
- Add "Sign in with Google" button to LoginComponent
- Implement OAuth redirect flow
- Handle callback and token storage

Step 3: Translations & Styling
- Add translation strings for "Sign in with Google" in all supported languages
- Update button styling to match Google brand guidelines

Step 4: Testing
- Test OAuth flow end-to-end
- Verify existing email/password login still works
- Test error handling (denied permissions, network errors)

Estimated time: 2-3 hours. Proceed?
```

## Example 4: Data Processing

**Original:** "Process all customer data"

**Issues:**
- Expensive (large-scale operation)
- No validation step
- Unclear processing logic

**Optimized:**
```
Process customer data in phases:

Phase 1: Validation (pilot with 100 records)
- Load sample of 100 customer records
- Validate data quality and processing logic
- Estimate total processing time and cost

Phase 2: Batch Processing (if validation passes)
- Process customers in batches of 1000
- Save progress after each batch (resumable)
- Generate error log for failed records

Phase 3: Summary Report
- Total records processed
- Success/failure counts
- Error analysis and recommendations

Start with Phase 1 validation?
```

## Example 5: Vague Improvement Request

**Original:** "Make the dashboard better"

**Issues:**
- No specific targets
- Undefined "better"
- Cannot auto-execute

**Optimized:**
```
I can improve the dashboard in several ways. Which aspect would you like to focus on?

Option A: Performance Optimization
- Reduce load time by implementing lazy loading
- Optimize API calls with caching
- Target: <2s initial load time

Option B: Visual Design Enhancement
- Update color scheme to match brand guidelines
- Improve spacing and typography
- Add micro-interactions for better UX

Option C: Feature Enhancement
- Add data export functionality
- Implement advanced filtering
- Add customizable widget layout

Option D: All of the above (comprehensive update)
- Estimated time: 6-8 hours
- Recommended approach: Incremental (A → B → C)

Which option would you like to pursue?
```

## Example 6: Complex Multi-Step Request

**Original:** "Update the app for the new design"

**Issues:**
- Vague scope
- No prioritization
- Missing dependencies

**Optimized:**
```
Update app to implement new design system:

Phase 1: Foundation (Required first)
- Update design tokens (colors, spacing, typography) in theme.ts
- Update global CSS variables
- Create new shared component library

Phase 2: Component Updates (Depends on Phase 1)
- Update Button, Input, Card components to use new design tokens
- Update navigation components (Header, Sidebar)
- Update form components

Phase 3: Page-Level Updates (Depends on Phase 2)
- Update Dashboard page layout
- Update Settings page
- Update Profile page

Phase 4: Translations & Assets (Parallel with Phase 3)
- Update translation strings for modified UI text
- Replace icon assets with new design system icons

Phase 5: Testing & Polish (Final)
- Visual regression testing
- Responsive design testing (mobile, tablet, desktop)
- Accessibility audit

Estimated time: 12-16 hours
Proceed with Phase 1?
```

## Example 7: Ambiguous Technical Request

**Original:** "Fix the bug"

**Issues:**
- No bug description
- Cannot identify issue
- No context

**Optimized:**
```
To fix the bug, I need more information:

1. What is the expected behavior?
2. What is the actual behavior (the bug)?
3. When does it occur (steps to reproduce)?
4. Which part of the app is affected?
5. Any error messages or logs?

Alternatively, if you can provide:
- A screenshot or screen recording
- The URL or page where it occurs
- Recent changes that might have caused it

This will help me identify and fix the issue efficiently.
```

## Example 8: Cost-Heavy Parallel Task

**Original:** "Find contact info for 500 companies"

**Issues:**
- Very expensive (500 parallel tasks)
- No validation
- Might exceed rate limits

**Optimized:**
```
Finding contact info for 500 companies is a large operation.

Recommended approach:

Phase 1: Pilot (10 companies)
- Test data quality and success rate
- Validate the extraction method
- Estimate total cost: ~50 credits
- Time: 5 minutes

Phase 2: Small Batch (50 companies) - If pilot succeeds
- Estimated cost: ~250 credits
- Time: 15 minutes

Phase 3: Full Scale (remaining 440) - If small batch succeeds
- Estimated cost: ~2,200 credits
- Time: 60 minutes

Total estimated cost: ~2,500 credits
Alternative: Use a data provider API (LinkedIn, Clearbit) for bulk access at lower cost

Proceed with Phase 1 pilot?
```
