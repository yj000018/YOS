---
name: session-synthesis
description: Generate a structured session card (fiche synthèse) for a single Manus session and archive it to Notion "Manus Memory — Sessions". Use when the user asks to synthesize, archive, or summarize a specific session, or at the end of a session to capture its essence. Part of the LLM Memory Pipeline (LMP).
---

# Session Synthesis

Generates a structured session card from a Manus session verbatim and archives it to Notion.

## Config

- **Notion Data Source ID**: `0720db9b-5e1d-41a2-bd0c-6721fe0dab94` (🗃️ Manus Memory — Sessions)
- **Cards dir**: `/home/ubuntu/manus_pipeline/session_cards/`
- **Export dir**: `/home/ubuntu/manus_pipeline/sessions_export/`
- **Model**: Claude Sonnet (`claude-sonnet-4-5`) via `ANTHROPIC_API_KEY`
- **Manus JWT**: refresh from browser if expired, store in `/home/ubuntu/manus_pipeline/.manus_token`

## Workflow

### Step 1 — Identify session UID

From Manus URL: `https://manus.im/app/<uid>` or from `all_sessions.json`.

### Step 2 — Collect verbatim

Run `scripts/collect_session.py` with the UID. Handles multi-segment sessions automatically.

### Step 3 — Generate card via Claude

Run `scripts/generate_card.py` with the UID. Output: `session_cards/<uid>_card.json`.

### Step 4 — Archive to Notion

Run `scripts/archive_to_notion.py`. Deduplication is automatic via `archived_uids.json`.

## Card Schema

```json
{
  "title": "Session title",
  "date": "YYYY-MM-DD",
  "depth_score": "landmark|substantial|standard|minor",
  "length_category": "xl|long|medium|short",
  "language": "fr|en|mixed",
  "project_hint": "yOS|eia|VISUAL_REALITY|DOMUS|GEN5|ODYSSEY|UNKNOWN",
  "themes": ["theme1"],
  "subthemes": ["subtheme1"],
  "executive_summary": "3-5 dense sentences",
  "context_and_intent": "Why this session was started",
  "what_was_done": "Actions taken",
  "outputs_produced": [{"type": "script|skill|page|config", "name": "...", "description": "..."}],
  "key_decisions": ["decision1"],
  "lessons_learned": {"worked_well": [], "failed_or_suboptimal": [], "discoveries": []},
  "challenges_and_blockers": ["challenge1"],
  "open_questions": ["question1"],
  "next_steps": ["step1"]
}
```

## Depth Score Guide

| Score | Criteria |
|---|---|
| `landmark` | Major architectural decision, new system built, paradigm shift |
| `substantial` | Significant progress, multiple outputs, complex problem solved |
| `standard` | Normal working session, moderate output |
| `minor` | Short session, test, quick task, trivial content |

## Notion Page Structure

- **Always open**: Executive Summary, Next Steps
- **Collapsed**: Context & Intent, What Was Done, Outputs, Key Decisions, Lessons Learned, Challenges, Open Questions
- **Properties**: Title, Date, Project, Depth, Length, Language, Themes, Subthemes, UID, Archived

## Notes

- Sessions with <50 words → marked `trivial`, skipped (no Claude call)
- Deduplication: check `archived_uids.json` before archiving
- Cost: ~$0.01-0.05/session with Claude Sonnet
