---
name: request-optimizer
description: Automatically optimize user requests to make them safer, more cost-effective, better structured, and more actionable. Use when user requests are vague or ambiguous, requests involve risky operations (deletions, bulk changes), requests could be expensive (large-scale parallel tasks, extensive research), requests need better structure (app changes, multi-step workflows), or when suggesting alternative approaches would be valuable.
---

# Request Optimizer

Automatically enhance user requests before execution to maximize safety, efficiency, cost-effectiveness, and clarity.

## When to Use This Skill

Apply request optimization when:

- **Vague or ambiguous requests** - "Make it better", "Fix this", "Update the app"
- **Risky operations** - Deletions, bulk changes, overwrites
- **Expensive operations** - Large-scale parallel tasks, extensive research, many API calls
- **Complex workflows** - Multi-step processes, app development changes
- **Underspecified requests** - Missing context, unclear objectives, undefined scope
- **Multiple valid approaches** - When suggesting alternatives would help

## Core Optimization Principles

### 1. Risk Reduction

Identify and mitigate potentially destructive operations.

**Apply when:**
- Deletion operations ("delete", "remove", "clear")
- Bulk operations ("all", "everything", "entire")
- Overwrite operations ("replace all")

**Add:**
- Backup steps before destructive operations
- Confirmation prompts with details
- Scope limitations
- Reversibility checks

**Example:**
```
Before: "Delete old files"
After: "Backup files older than 30 days to /backup/[timestamp], 
       list files to be deleted with sizes, request confirmation, 
       then delete with summary report"
```

### 2. Cost Optimization

Reduce computational and credit costs through efficient alternatives.

**Apply when:**
- Large-scale parallel operations
- Extensive research or data gathering
- Repeated API calls
- Unbounded scope

**Strategies:**
- Batch operations instead of individual calls
- Pilot approach (validate with small sample first)
- Focused scope instead of exhaustive coverage
- Suggest alternative tools or methods
- Incremental scaling

**Example:**
```
Before: "Research 500 companies"
After: "Start with 10 companies to validate approach (50 credits),
       then batch process remaining 490 (2,450 credits).
       Alternative: Use data provider API for bulk access at lower cost"
```

### 3. Auto-Execution Enablement

Transform ambiguous requests into clear, actionable tasks.

**Apply when:**
- Vague pronouns ("this", "that", "it")
- Undefined improvements ("better", "fix", "optimize")
- Missing context or objectives

**Strategies:**
- Identify specific targets (files, components, features)
- Define concrete objectives and success criteria
- Add context from conversation history
- Specify measurable outcomes

**Example:**
```
Before: "Make this better"
After: "Improve [DashboardComponent] by:
       1. Reducing load time to <2s via lazy loading
       2. Adding data export functionality
       3. Implementing responsive design for mobile"
```

### 4. Structure Enhancement

Break down complex requests into well-sequenced steps.

**Apply when:**
- Multiple objectives in one request
- Complex workflows with dependencies
- App development changes
- Interdependent operations

**Strategies:**
- Break into sequential steps
- Identify dependencies (A before B)
- Separate concerns (logic → UI → translations → styling)
- Add validation/testing steps
- Number steps for clarity

**Example:**
```
Before: "Change the login flow"
After: "Update login flow in 5 steps:
       1. Modify auth logic in auth.ts for OAuth
       2. Update LoginComponent UI with OAuth buttons
       3. Add translation strings for new UI elements
       4. Update styling to match design system
       5. Test complete flow end-to-end"
```

### 5. App Development Changes

Transform vague change requests into specific, sequenced updates.

**Apply when:**
- UI/UX changes
- Feature modifications
- Styling updates
- Component changes

**Key pattern:**
1. **Features/Logic** - Core functionality changes
2. **UI Components** - Visual and interaction updates
3. **Translations** - Update strings for modified UI
4. **Styling** - Colors, spacing, responsive design
5. **Testing** - Validate changes work correctly

**Example:**
```
Before: "Update the dashboard"
After: "Update dashboard in 4 phases:
       Phase 1: Add 3 new data widgets to DashboardComponent
       Phase 2: Update API to fetch additional data
       Phase 3: Add translation strings for new widgets
       Phase 4: Update styling for new layout + responsive design"
```

### 6. Variant Suggestion

When requests are underspecified or multiple approaches exist, present options.

**Apply when:**
- Underspecified goals
- Multiple valid approaches
- Unclear priorities
- Missing key decisions

**Structure:**
- Present 2-4 concrete options
- Explain trade-offs (time, cost, features)
- Provide selection criteria
- Ask clarifying question

**Example:**
```
Before: "Help me build a website"
After: "3 approaches for your website:

       Option A: Static landing page
       - Best for: Marketing, portfolios
       - Time: 1-2 hours | Cost: Low

       Option B: Dynamic web app with database
       - Best for: User accounts, data management
       - Time: 4-8 hours | Cost: Medium

       Option C: No-code solution
       - Best for: Quick prototypes
       - Time: 30 min | Cost: Very low

       Which fits your needs?"
```

## Optimization Workflow

### Step 1: Analyze the Request

Identify optimization opportunities:

- **Risk indicators** - Deletion, bulk operations, overwrites
- **Cost indicators** - Large scale, parallel tasks, extensive research
- **Ambiguity indicators** - Vague pronouns, undefined goals, missing context
- **Complexity indicators** - Multiple objectives, dependencies, app changes
- **Maturity indicators** - Underspecified, multiple approaches possible

### Step 2: Select Optimization Patterns

Choose applicable patterns from the 6 core principles above. Multiple patterns can apply to a single request.

### Step 3: Transform the Request

Rewrite the request applying selected patterns:

- Add safety measures for risky operations
- Suggest cost-effective alternatives
- Clarify ambiguous elements
- Structure complex workflows
- Sequence app development changes properly
- Present variants when appropriate

### Step 4: Present the Optimized Request

Format the optimized request clearly:

- Use numbered steps for sequences
- Use phases for large workflows
- Include estimates (time, cost) when relevant
- Add confirmation questions for expensive operations
- Explain trade-offs for variants

## Advanced Patterns

### Cascade Awareness for App Changes

UI changes trigger cascading updates:

```
UI Component Change
  ↓
Translation Strings (new UI text needs translation)
  ↓
Styling Updates (new components need styling)
  ↓
Responsive Design (ensure mobile compatibility)
  ↓
Testing (validate all changes)
```

Always consider cascade effects when optimizing app change requests.

### Pilot-Scale Pattern for Expensive Operations

For large-scale operations, use incremental validation:

```
1. Pilot (small sample) - Validate approach
2. Small batch - Confirm scalability
3. Full scale - Execute with confidence
```

Include cost estimates at each phase.

### Dependency Sequencing

When operations have dependencies, sequence them correctly:

```
✗ Wrong: "Update UI and translations simultaneously"
✓ Right: "1. Update UI components, 2. Add translations for new UI text"
```

UI must exist before it can be translated.

## Reference Documents

For detailed patterns and examples, see:

- **[optimization_patterns.md](references/optimization_patterns.md)** - Detailed transformation patterns for each of the 6 core principles
- **[examples.md](references/examples.md)** - Real-world examples of request optimizations across different scenarios

Load these references when you need specific guidance on how to apply a pattern or want to see more examples.

## Key Principles

- **Safety first** - Always add safety measures for risky operations
- **Cost awareness** - Suggest efficient alternatives for expensive operations
- **Clarity over brevity** - Better to be explicit than ambiguous
- **Structure over chaos** - Break down complex requests into clear steps
- **Validate before scale** - Use pilot approach for large operations
- **Consider cascades** - Especially for app development changes
