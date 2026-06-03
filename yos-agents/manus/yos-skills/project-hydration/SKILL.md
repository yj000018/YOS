---
name: project-hydration
description: Load a project's living card from Notion "Manus Memory" and inject it as context at the start of a session. Use when starting a session on a known project, when the user says "load context for project X", or when yOS project context should be available. Enables memory continuity across sessions.
---

# Project Hydration

Loads a project card from Notion and injects it as session context.

## Config

- **Notion Sessions DB**: `0720db9b-5e1d-41a2-bd0c-6721fe0dab94`
- **Projects**: yOS, eia, VISUAL_REALITY, DOMUS, GEN5, ODYSSEY + any cluster-defined project

## Workflow

### Step 1 — Identify project

From user request: "Load context for yOS" → project = `yOS`
From session title or first message if project is implicit.

### Step 2 — Fetch project card from Notion

```bash
manus-mcp-cli tool call notion-search --server notion --input '{"query": "PROJECT: yOS", "filter": {"value": "page", "property": "object"}}'
```

Or query the Sessions DB filtered by project:
```bash
manus-mcp-cli tool call notion-query-database --server notion --input '{
  "data_source_id": "0720db9b-5e1d-41a2-bd0c-6721fe0dab94",
  "filter": {"property": "Project", "select": {"equals": "yOS"}},
  "sorts": [{"property": "Date", "direction": "descending"}],
  "page_size": 10
}'
```

### Step 3 — Inject context

Present the project card content as context prefix:

```
=== PROJECT CONTEXT: {project} ===
[Vision & Objective]
[Current State]
[Key Decisions]
[Open Questions]
[Next Steps]
=== END CONTEXT ===
```

Then proceed with the user's request.

## Hydration Levels

| Level | Content loaded | Use case |
|---|---|---|
| **Quick** | Executive summary + Next Steps only | Fast context refresh |
| **Standard** | Full project card | Normal session start |
| **Deep** | Project card + last 5 session cards | Complex continuation |

## Auto-trigger Signals

Hydrate automatically when:
- User mentions a known project name (yOS, eia, DOMUS, etc.)
- Session title matches a known project
- User says "continue where we left off" or "load context"
- User references a past decision or output without explaining it

## Notes

- Project cards are created/updated by `project-synthesis` skill
- If no project card exists yet → run `project-synthesis` first
- For cross-project sessions → hydrate the most relevant project only
- Hydration adds ~500-2000 tokens to context — always worth it for known projects
