---
name: project-synthesis
description: Generate or update a living project card in Notion "Manus Memory — Projects" by synthesizing all session cards belonging to a project. Use when the user asks to synthesize a project, create a project overview, or update a project's status from its sessions. Part of the LLM Memory Pipeline (LMP).
---

# Project Synthesis

Aggregates all session cards for a project into a living project card in Notion.

## Config

- **Notion Sessions DB**: `0720db9b-5e1d-41a2-bd0c-6721fe0dab94`
- **Cards dir**: `/home/ubuntu/manus_pipeline/session_cards/`
- **Model**: Claude Sonnet (`claude-sonnet-4-5`) via `ANTHROPIC_API_KEY`
- **Projects**: yOS, eia, VISUAL_REALITY, DOMUS, GEN5, ODYSSEY (+ clusters from clustering phase)

## Workflow

### Step 1 — Gather session cards for the project

```python
import json
from pathlib import Path

project = "yOS"  # or any project name
cards_dir = Path("/home/ubuntu/manus_pipeline/session_cards")
project_cards = []
for f in cards_dir.glob("*_card.json"):
    card = json.load(open(f))
    if card.get("project_hint") == project or project in card.get("themes", []):
        project_cards.append(card)
```

### Step 2 — Generate project card via Claude

Send all session cards (executive summaries + key decisions + next steps) to Claude with this prompt:

```
You are synthesizing a living project card for the project "{project}".
Below are {N} session cards from this project, ordered by date.

For each section, synthesize across ALL sessions:
1. PROJECT VISION & OBJECTIVE — What is this project trying to achieve?
2. CURRENT STATE — Where does the project stand today?
3. KEY DECISIONS TAKEN — Chronological list of major decisions
4. ARCHITECTURE / STACK — Technical stack if applicable
5. CUMULATIVE OUTPUTS — All outputs produced across sessions
6. RECURRING PATTERNS — What approaches work repeatedly?
7. RECURRING BLOCKERS — What keeps coming up as obstacles?
8. OPEN QUESTIONS — Unresolved questions across the project
9. NEXT STEPS — Concrete actions identified but not yet executed
10. LINKED SESSIONS — List of session UIDs with one-line summary each

Be dense, factual, no filler. This card will be used as context injection for future sessions.
```

### Step 3 — Archive to Notion

Create a page in the parent Notion page for the project (or in Manus Memory hub).

## Project Card Structure in Notion

```
⭐ PROJECT: {name}
Last updated: {date}

## Vision & Objective [open]
## Current State [open]
## Key Decisions (chronological) [collapsed]
## Architecture / Stack [collapsed]
## Cumulative Outputs [collapsed]
## Recurring Patterns [collapsed]
## Recurring Blockers [collapsed]
## Open Questions [collapsed]
## Next Steps [open]
## Linked Sessions [collapsed]
```

## Notes

- Run after every 5+ new sessions on a project
- The project card is the primary source for `project-hydration`
- If sessions span multiple projects, create one card per project
