# LLM Extraction Methods — Reference Table
*LLM Memory Pipeline (LMP) v2 — Last updated: 2026-04-09*

This table tracks the extraction method for each LLM, its current status, and known alternatives.
Update this table each time a new method is validated or a new LLM is added.

---

## Status Legend

| Symbol | Meaning |
|---|---|
| ✅ | Operational — tested and working |
| 🟡 | Partial — works with manual step |
| 🔴 | Blocked — no method available yet |
| ⏳ | Pending — not yet tested |

---

## Extraction Methods by LLM

| LLM | Primary Method | Status | Notes | Adapter |
|---|---|---|---|---|
| **Manus** | Native API — gRPC-web (`ListSessions` + `getSessionV2`) | ✅ Operational | JWT token from browser. Pagination via `offset`. 325 sessions archived. Token valid ~6mo. | `01_collect_sessions.py` |
| **ChatGPT** | Export ZIP — `chat.openai.com → Settings → Data Controls → Export data` | 🟡 Manual trigger | ZIP contains `conversations.json`. Web only, not iOS. Delivery by email within 24h. | `adapters/chatgpt_adapter.py` ✅ Built |
| **Gemini** | Google Takeout — `takeout.google.com → Gemini Apps Activity` | 🟡 Manual trigger | JSON export. Web only. Includes all conversations with timestamps. | `adapters/gemini_adapter.py` ✅ Built |
| **Grok** | Browser automation — Playwright scrape `grok.com` (authenticated) | ⏳ Pending login | No native export. No API for conversation history. `api.x.ai` is generation-only. | `adapters/grok_playwright.py` ✅ Built |
| **Claude.ai** | API intercept — Bearer token from DevTools + direct API call | ⏳ Pending token | No export API. Token from DevTools → `claude.ai/api/organizations/{org_id}/chat_conversations` | `adapters/claude_playwright.py` ✅ Built |
| **Perplexity** | Browser automation — Playwright scrape `perplexity.ai` | ⏳ Low priority | Search-based, lower synthesis value. Library feature stores threads. | `adapters/perplexity_playwright.py` ✅ Built |
| **Mistral (Le Chat)** | Browser automation — Playwright scrape `chat.mistral.ai` | ⏳ Not tested | No export API known. | Not built |
| **Copilot (Microsoft)** | Browser automation or Edge extension | ⏳ Not tested | Conversations may sync to Microsoft account. | Not built |

---

## Pipeline Adapters — Implementation Status

| LLM | Adapter Script | Status | Location |
|---|---|---|---|
| Manus | `01_collect_sessions.py` | ✅ Operational | `/home/ubuntu/manus_pipeline/` |
| ChatGPT | `chatgpt_adapter.py` | ✅ Built | `/home/ubuntu/manus_pipeline/adapters/` |
| Gemini | `gemini_adapter.py` | ✅ Built | `/home/ubuntu/manus_pipeline/adapters/` |
| Grok | `grok_playwright.py` | ✅ Built | `/home/ubuntu/manus_pipeline/adapters/` |
| Claude.ai | `claude_playwright.py` | ✅ Built | `/home/ubuntu/manus_pipeline/adapters/` |
| Perplexity | `perplexity_playwright.py` | ✅ Built | `/home/ubuntu/manus_pipeline/adapters/` |

---

## Unified Entry Point (LMP v2)

```bash
cd /home/ubuntu/manus_pipeline

# Status of all LLMs
python lmp_run.py --status

# Run any LLM
python lmp_run.py --llm manus
python lmp_run.py --llm chatgpt --input /path/to/conversations.json
python lmp_run.py --llm gemini --input /path/to/takeout_folder/
python lmp_run.py --llm grok --playwright
python lmp_run.py --llm claude --playwright

# Print extraction instructions
python lmp_run.py --instructions chatgpt

# Cross-LLM clustering (after all LLMs processed)
python lmp_run.py --cluster-all
```

---

## Unified Pipeline Flow (All LLMs)

```
LLM-SPECIFIC EXTRACTION
  (API / ZIP export / Playwright / Browser extension)
         ↓
NORMALIZATION → unified_session format
  {uid, title, date, source_llm, messages: [{role, content, ts}]}
         ↓
SYNTHESIS → Claude Sonnet (session-synthesis)
  → structured card JSON
         ↓
CLUSTERING → Claude Sonnet (project-synthesis)
  → project assignment + taxonomy
         ↓
ARCHIVING → Notion "Manus Memory — Sessions"
  → structured page + collapsed verbatim
         ↓
PROJECT CARDS → Notion "Manus Memory — Projects"
  → living project synthesis (updated incrementally)
```

---

## Browser Extensions — Known Tools

| Extension | Supported LLMs | Method | Notes |
|---|---|---|---|
| **ChatGPT Exporter** | ChatGPT | DOM scraping → JSON/MD/HTML | Chrome/Firefox. Works on web app. |
| **SaveMyConversations** | ChatGPT, Claude, Gemini | DOM scraping | Multi-LLM support. |
| **HistoryExport** | ChatGPT | API-based | Requires OpenAI session token. |
| **Claude Exporter** | Claude.ai | DOM scraping | Chrome only. |

---

## Next Actions (Priority Order)

1. **ChatGPT** — trigger export on `chat.openai.com` → send ZIP → run `python lmp_run.py --llm chatgpt --input conversations.json`
2. **Gemini** — trigger Google Takeout → send ZIP → run `python lmp_run.py --llm gemini --input takeout_folder/`
3. **Grok** — login to grok.com in sandbox browser → run `python lmp_run.py --llm grok --playwright`
4. **Claude.ai** — open claude.ai → DevTools → copy Bearer token + org_id → run `python adapters/claude_playwright.py --token <T> --org-id <O>`
5. **Cross-LLM clustering** — after all LLMs: `python lmp_run.py --cluster-all`

---

*This document is part of the LLM Memory Pipeline (LMP) — skill: `memory-pipeline`*
