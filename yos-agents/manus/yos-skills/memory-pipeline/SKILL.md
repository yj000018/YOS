---
name: memory-pipeline
description: Run the full LLM Memory Pipeline (LMP) to collect, synthesize, cluster, and archive all Manus (and other LLM) conversation sessions into Notion "Manus Memory". Use when the user asks to run the full pipeline, process all sessions, do a bulk archive, or perform a periodic memory update. Orchestrates session-synthesis and project-synthesis at scale.
---

# LLM Memory Pipeline (LMP) v2

Full multi-LLM pipeline — bulk processing of sessions from Manus, ChatGPT, Gemini, Grok, Claude.ai, Perplexity into Notion "Manus Memory — Sessions".

## Current State (snapshot: 2026-04-09)

| LLM | Sessions | Status | Notion |
|---|---|---|---|
| Manus | 325 | ✅ Complete | 325/325 archived |
| ChatGPT | — | 🟡 Awaiting ZIP export | — |
| Gemini | — | 🟡 Awaiting Takeout | — |
| Grok | — | ⏳ Playwright pending | — |
| Claude.ai | — | ⏳ Token intercept pending | — |
| Perplexity | — | ⏳ Low priority | — |

**Verbatim update**: 278 pages updated with collapsed verbatim sections (32 not found, 2 empty).

**Projects identified**: 7 (yOS 183, eia 41, VISUAL_REALITY 22, DOMUS 25, ONE 21, GEN5 13, ODYSSEY 8)

## Config

- **Pipeline dir**: `/home/ubuntu/manus_pipeline/`
- **Unified entry point**: `lmp_run.py` (v2)
- **Adapters dir**: `adapters/` (chatgpt, gemini, grok, claude, perplexity)
- **State files**: `archived_uids.json`, `state/cross_llm_assignments.json`
- **Notion DB**: `0720db9b-5e1d-41a2-bd0c-6721fe0dab94`
- **Model**: Claude Sonnet (`claude-sonnet-4-5`) via `ANTHROPIC_API_KEY`
- **Cost**: ~$0.02/session avg → ~$7 per full run of 350 sessions

## Unified Entry Point (LMP v2)

```bash
cd /home/ubuntu/manus_pipeline

# Status overview
python lmp_run.py --status

# Run Manus pipeline (automatic)
python lmp_run.py --llm manus

# Run ChatGPT (requires ZIP export first)
python lmp_run.py --llm chatgpt --input /path/to/conversations.json

# Run Gemini (requires Takeout folder)
python lmp_run.py --llm gemini --input /path/to/takeout_folder/

# Run Grok (requires browser login)
python lmp_run.py --llm grok --playwright

# Run Claude.ai (requires token from DevTools)
python lmp_run.py --llm claude --playwright

# Cross-LLM clustering (after all LLMs processed)
python lmp_run.py --cluster-all

# Print extraction instructions for any LLM
python lmp_run.py --instructions chatgpt
```

## Full Pipeline — Phase by Phase

```bash
# Phase 1: Collect sessions (Manus API, pagination-aware)
python 01_collect_sessions.py

# Phase 2: Generate session cards (Claude Sonnet)
python 02_generate_cards.py

# Phase 3: Archive to Notion
python 03_archive_to_notion.py

# Phase 4: Add verbatim sections to existing pages
python 04_update_verbatim.py

# Phase 5: Cluster sessions into projects
python 05_clustering.py

# Phase 6: Cross-LLM clustering (after all LLMs)
python 06_cross_llm_cluster.py

# Phase 7: Archive project cards
python 07_archive_project_cards.py
```

Or run all phases at once:
```bash
nohup python run_full_pipeline.py > /tmp/pipeline.log 2>&1 &
tail -f /tmp/pipeline.log
```

## Per-LLM Extraction Methods

### Manus (✅ Automatic)
- Method: Native gRPC-web API
- Token: JWT from browser DevTools → `/home/ubuntu/manus_pipeline/.manus_token`
- Token expiry: ~6 months. Refresh when 401.
- Command: `python lmp_run.py --llm manus`

### ChatGPT (🟡 Manual step required)
1. Go to https://chat.openai.com
2. Settings → Data Controls → Export data
3. Wait for email with download link (up to 24h)
4. Download ZIP, extract `conversations.json`
5. Run: `python lmp_run.py --llm chatgpt --input /path/to/conversations.json`

### Gemini (🟡 Manual step required)
1. Go to https://takeout.google.com
2. Deselect all → select "Gemini Apps Activity"
3. Export → Download ZIP → Extract
4. Run: `python lmp_run.py --llm gemini --input /path/to/extracted_folder/`

### Grok (⏳ Playwright)
1. Login to grok.com in sandbox browser
2. Run: `python lmp_run.py --llm grok --playwright`
- Adapter: `adapters/grok_playwright.py`

### Claude.ai (⏳ API Intercept)
1. Open claude.ai in sandbox browser
2. DevTools → Network → copy Bearer token + org_id
3. Run: `python adapters/claude_playwright.py --token <TOKEN> --org-id <ORG_ID>`

### Perplexity (⏳ Low priority)
- Similar to Claude.ai — API intercept or Playwright
- Adapter: `adapters/perplexity_playwright.py`

## Retry Failed Sessions

If some sessions fail archiving (Notion rate limit):
```bash
cd /home/ubuntu/manus_pipeline
python retry_failed.py
```
Edit `FAILED_UIDS` list in `retry_failed.py` to target specific sessions.

## Cross-LLM Clustering

After all LLMs are processed:
```bash
python 06_cross_llm_cluster.py --all-llms
python 06_cross_llm_cluster.py --update-notion
```

Results saved to `state/cross_llm_assignments.json`.

## Cost Optimization

- **Prompt caching**: System prompt is identical across sessions → automatic caching by Anthropic
- **Skip trivial**: Sessions <50 words are auto-skipped
- **Batch API**: Set `USE_BATCH=true` for 50% cost reduction (async, ~24h delay)
- **Scope filtering**: Use `--scope since:DATE` or `--scope project:NAME` for incremental runs

## Monitoring

```bash
# Check archive progress
grep -c "✅" /home/ubuntu/manus_pipeline/archive_notion.log

# Check verbatim update
tail -10 /home/ubuntu/manus_pipeline/verbatim_update.log

# Check clustering
tail -10 /home/ubuntu/manus_pipeline/clustering.log

# Full pipeline log
tail -20 /home/ubuntu/manus_pipeline/run_full.log
```

## Notion Structure

- **Database**: "Manus Memory — Sessions" (`0720db9b-5e1d-41a2-bd0c-6721fe0dab94`)
- **Properties**: Title, Project (Select), Depth (Select), Length (Select), Language (Select), Themes, Subthemes, UID, Archived, Date
- **Page structure**: Executive Summary → Context & Intent → What Was Done → Outputs → Key Decisions → Lessons Learned → Challenges → Open Questions → Next Steps → [Verbatim collapsed]
- **Project cards**: Living synthesis pages per project, updated incrementally

## Session Card Format (unified_session)

All adapters normalize to this format before synthesis:
```json
{
  "uid": "unique_id",
  "title": "Session title",
  "date": "YYYY-MM-DD",
  "source_llm": "manus|chatgpt|gemini|grok|claude|perplexity",
  "created_at": "ISO timestamp",
  "updated_at": "ISO timestamp",
  "message_count": 42,
  "word_count": 5000,
  "messages": [
    {"role": "USER", "content": "...", "timestamp": ""},
    {"role": "ASSISTANT", "content": "...", "timestamp": ""}
  ]
}
```
