# KAP Knowledge Adapter Census
**Gate:** MPM-20260705-YOS-KAP-KNOWLEDGE-ADAPTER-CENSUS-AND-PROBE-GATE  
**Version:** 1.0.0  
**Date:** 2026-07-05  
**Status:** COMPLETE

---

## 1. Census Summary

| Metric | Value |
|---|---|
| Total adapters catalogued | 19 |
| Production-ready | 2 |
| Production-candidate | 3 |
| Candidate | 1 |
| Probe-required | 8 |
| Unsupported (Class C) | 5 |

---

## 2. Adapter Classification

### Class A — API Adapters (8 adapters)

| Adapter | Provider | Status | Auth | Key Gap |
|---|---|---|---|---|
| `openai-api-conversation` | OpenAI | production_candidate | API key ✅ (proxy) | No ChatGPT App history |
| `anthropic-api-conversation` | Anthropic | probe_required | API key ❌ | No key in env |
| `gemini-api-conversation` | Google Gemini | probe_required | API key ❌ | No key in env |
| `xai-api-research` | xAI / Grok | probe_required | API key ❌ | No key in env |
| `perplexity-api-research` | Perplexity | probe_required | API key ❌ | No key in env |
| `manus-api-adapter` | Manus API | production_candidate | API key ❌ (must generate) | No key generated |
| `notion-api-adapter` | Notion | production_candidate | OAuth2/token ❌ | No token in env |
| `mem0-memory-adapter` | Mem0 | probe_required | API key ❌ | No key in env |

### Class B — Workspace/Repository Adapters (6 adapters)

| Adapter | Provider | Status | Auth | Key Gap |
|---|---|---|---|---|
| `manus-workspace-adapter` | Manus FS | **production_ready** | None (native) | None |
| `git-repository-adapter` | Git / GitHub | **production_ready** | PAT ✅ | GitHub connector not enabled |
| `google-drive-file-adapter` | Google Drive | candidate | OAuth2 ⚠️ | gws auth incomplete |
| `claude-code-workspace` | Claude Code | probe_required | CLI ❌ | Not installed |
| `codex-workspace` | OpenAI Codex | probe_required | CLI ❌ | Not installed |
| `gemini-cli-workspace` | Gemini CLI | probe_required | CLI ❌ | Not installed |

### Class C — Consumer UI Adapters (5 adapters)

| Adapter | Provider | Status | Notes |
|---|---|---|---|
| `chatgpt-app-consumer` | ChatGPT App | unsupported | Manual export only |
| `claude-ai-consumer` | Claude.ai | unsupported | Manual export only |
| `gemini-app-consumer` | Gemini App | unsupported | Manual export only |
| `grok-app-consumer` | Grok App | unsupported | Manual export only |
| `perplexity-app-consumer` | Perplexity App | unsupported | Manual export only |

---

## 3. Capability Matrix Summary

| Capability | Proven | Candidate | Unsupported |
|---|---|---|---|
| Historical backfill | git | manus-workspace, manus-api, notion, gdrive, mem0 | All Class C + openai-api |
| Continuous capture | git | manus-workspace, manus-api, openai-api, notion, gdrive | All Class C |
| Checkpoint | git, manus-workspace | manus-api, notion, gdrive | All Class C + openai-api |
| Finalization | git | manus-workspace, manus-api, notion | All Class C + openai-api |
| Health check | git, manus-workspace, openai-api | manus-api | All Class C |

---

## 4. Recommended Production Stack

```
PRIMARY WORKSPACE:   manus-workspace-adapter  (/home/ubuntu/yos-bus-runtime)
PRIMARY TRANSPORT:   git-repository-adapter   (yos-monorepo)
PRIMARY RELAY:       manus-api-adapter        (task.sendMessage — needs API key)
PRIMARY MEMORY:      notion-api-adapter       (needs token)
PRIMARY LLM:         openai-api-conversation  (Manus proxy — active)
RESEARCH:            perplexity-api-research  (needs API key)
```

---

## 5. Critical Gaps

| Gap | Priority | Workaround |
|---|---|---|
| GAP-001: ChatGPT App history inaccessible | HIGH | Manual JSON export |
| GAP-002: Manus API key not configured | HIGH | Generate in Manus settings |
| GAP-003: Notion token not configured | MEDIUM | Create integration token |
| GAP-004: Google Drive auth incomplete | MEDIUM | gws auth login |
| GAP-005: No Anthropic/Gemini/xAI/Perplexity keys | LOW | Configure per provider |

---

## 6. Probe Queue (ordered by priority)

1. `manus-api-adapter` — generate API key → test task.list + sendMessage
2. `notion-api-adapter` — configure token → test page.create + search
3. `google-drive-file-adapter` — complete gws auth → test files.list
4. `mem0-memory-adapter` — configure API key → test memory.search
5. `anthropic-api-conversation` — configure key → test health
6. `perplexity-api-research` — configure key → test research query
7. `gemini-api-conversation` — configure key → test health
8. `xai-api-research` — configure key → test health

---

## 7. Phase A Documentation Sources

| Source | Status | Notes |
|---|---|---|
| Manus API docs (`/home/ubuntu/skills/manus-api/docs/`) | COMPLETE | openapi_v2.json, all endpoints |
| OpenAI API (Manus proxy) | COMPLETE | 10 models available |
| Git/GitHub | COMPLETE | v2.43.0, PAT active |
| gws CLI | COMPLETE | v0.22.3, auth incomplete |
| Manus workspace filesystem | COMPLETE | /home/ubuntu persists |
| Manus tools (`manus-*`) | COMPLETE | 12 tools available |
| KAP existing protocols | COMPLETE | 5 protocols read |
| AGENTS registry | COMPLETE | 6 agents, 8 capabilities |
| YARP spec | COMPLETE | v1.1.0 |
| BUS connectivity matrix | COMPLETE | 18 mechanisms |

---

## 8. Phase B Probe Results

| Probe | Result |
|---|---|
| Manus workspace write/read/delete | PASS |
| OpenAI proxy health | PASS (10 models) |
| Git delta (2026-07-05) | PASS (2 commits) |
| Manus API (unauthenticated) | HTTP 401 (expected) |
| Google Drive API | 401 (auth incomplete) |
| gws drive list | Error (auth required) |
| Anthropic CLI | Not installed |
| Gemini CLI | Not installed |
| Codex CLI | Not installed |
| mem0 Python package | Not installed |
| notion_client Python package | Not installed |
