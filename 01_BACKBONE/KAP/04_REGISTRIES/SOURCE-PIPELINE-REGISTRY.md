# SOURCE-PIPELINE-REGISTRY

> Y-OS / KAP — Pipeline Status Registry
> Tracks available pipelines per channel and source instance.
> See `KAP-SOURCE-MATRIX.md` for full status matrix.
> Last Updated: 2026-07-03
> **No acquisition. No ingestion. No synthesis. No mutation.**

---

## Pipeline Types

| Pipeline | Description |
|---|---|
| `METADATA-ONLY` | Scan repo/workspace structure, file names, dates — no content read |
| `CONTENT-PILOT` | Read a small sample of content (5–10 files) to validate extraction |
| `EXTRACTION-PILOT` | Extract fragments from a controlled sample |
| `FULL-EXTRACTION` | Full fragment extraction across all instances |

## Pipeline Status Vocabulary

| Status | Meaning |
|---|---|
| `READY` | Pipeline can run immediately |
| `PENDING-GATE` | Requires a gate to pass first |
| `BLOCKED` | Cannot run — blocker must be resolved |
| `COMPLETE` | Pipeline has run successfully |
| `NOT-APPLICABLE` | Pipeline type not relevant for this source |

---

## CH-001 — Git / GitHub

| Source | Metadata-Only | Content Pilot | Extraction Pilot | Full Extraction | Mutation Risk | Blockers | Next Gate |
|---|---|---|---|---|---|---|---|
| INST-GIT-001/002 (ACQUIRED) | `COMPLETE` | `COMPLETE` | `PENDING-GATE` | `PENDING-GATE` | None | None | THOUGHT-LINE-SEEDING-GATE |
| INST-GIT-003→035 (CATALOGUED) | `READY` | `PENDING-GATE` | `PENDING-GATE` | `PENDING-GATE` | None | None | GITHUB-SOURCE-ACQUISITION-GATE |
| INST-GIT-036→041 (DEFERRED) | `NOT-APPLICABLE` | `NOT-APPLICABLE` | `NOT-APPLICABLE` | `NOT-APPLICABLE` | None | Out of scope | — |

**Connector:** GitHub REST API v3 — PAT confirmed working
**Metadata endpoint:** `GET /repos/{owner}/{repo}` + `/git/trees/{sha}?recursive=1`
**Content endpoint:** `GET /repos/{owner}/{repo}/contents/{path}`
**Rate limit:** 5000 req/hr (authenticated)

---

## CH-002 — ChatGPT

| Source | Metadata-Only | Content Pilot | Extraction Pilot | Full Extraction | Mutation Risk | Blockers | Next Gate |
|---|---|---|---|---|---|---|---|
| INST-GPT-001/002 (ACQUIRED) | `COMPLETE` | `COMPLETE` | `PENDING-GATE` | `PENDING-GATE` | None | None | THOUGHT-LINE-SEEDING-GATE |
| INST-GPT-003/004 (PENDING) | `BLOCKED` | `BLOCKED` | `BLOCKED` | `BLOCKED` | None | User must export sessions | CAPTURE-PATCH-2 |

**Connector:** Manual export → Git persistence
**Export method:** ChatGPT Settings → Data Controls → Export → conversations.json

---

## CH-003 — Manus

| Source | Metadata-Only | Content Pilot | Extraction Pilot | Full Extraction | Mutation Risk | Blockers | Next Gate |
|---|---|---|---|---|---|---|---|
| INST-MAN-001 (ACQUIRED) | `COMPLETE` | `COMPLETE` | `PENDING-GATE` | `PENDING-GATE` | None | None | THOUGHT-LINE-SEEDING-GATE |
| INST-MAN-002 Historical (194) | `COMPLETE` | `PENDING-GATE` | `PENDING-GATE` | `PENDING-GATE` | None | Non-primary corpus | MANUS-HISTORICAL-ACQUISITION-GATE |

**Connector:** Git (already exported) + Notion API (for historical)

---

## CH-004 — Obsidian / Markdown

| Source | Metadata-Only | Content Pilot | Extraction Pilot | Full Extraction | Mutation Risk | Blockers | Next Gate |
|---|---|---|---|---|---|---|---|
| INST-OBS-001/002 (Git-backed) | `READY` | `PENDING-GATE` | `PENDING-GATE` | `PENDING-GATE` | None | None | OBSIDIAN-PIPELINE-VALIDATION-GATE |
| INST-OBS-003 Local vaults (7) | `BLOCKED` | `BLOCKED` | `BLOCKED` | `BLOCKED` | None | Vault paths unknown | OBSIDIAN-VAULT-DISCOVERY-GATE |

**Connector (Git-backed):** GitHub API tree endpoint — `GET /repos/{owner}/{repo}/git/trees/{sha}?recursive=1`
**Connector (local):** Mac filesystem via FUSE mount or user-provided export
**Note:** Never modify Obsidian vault files. Read-only access only.

---

## CH-005 — Notion

| Source | Metadata-Only | Content Pilot | Extraction Pilot | Full Extraction | Mutation Risk | Blockers | Next Gate |
|---|---|---|---|---|---|---|---|
| INST-NOT-001 Y-World | `READY` | `PENDING-GATE` | `PENDING-GATE` | `PENDING-GATE` | None | Census incomplete | NOTION-PIPELINE-CONTROLLED-EXECUTION-GATE |
| INST-NOT-002 Personal | `BLOCKED` | `BLOCKED` | `BLOCKED` | `BLOCKED` | None | Login required | NOTION-PIPELINE-CONTROLLED-EXECUTION-GATE |

**Connector:** Notion REST API v1 — Integration key confirmed
**Metadata endpoint:** `POST /search` with `page_size=100`, `filter: {object: page}`
**Content endpoint:** `GET /blocks/{id}/children`
**Rate limit:** 3 req/sec

---

## CH-006 — Mem0

| Source | Metadata-Only | Content Pilot | Extraction Pilot | Full Extraction | Mutation Risk | Blockers | Next Gate |
|---|---|---|---|---|---|---|---|
| INST-MEM-001 (ACQUIRED) | `COMPLETE` | `NOT-APPLICABLE` | `NOT-APPLICABLE` | `NOT-APPLICABLE` | None | Signal/index only | — |

**Note:** Mem0 is a semantic routing layer, not a primary corpus. No extraction pipeline needed.

---

## CH-007 — Internal LLM Knowledge

| Source | Metadata-Only | Content Pilot | Extraction Pilot | Full Extraction | Mutation Risk | Blockers | Next Gate |
|---|---|---|---|---|---|---|---|
| INST-LLM-001→005 All LLMs | `NOT-APPLICABLE` | `PENDING-GATE` | `PENDING-GATE` | `PENDING-GATE` | None | Taxonomy not complete | LLM-INTERNAL-MEMORY-EXTRACTION-GATE |

**Connector:** Structured prompt batch
**Prompt template:** `"For each of the following projects/themes, synthesize everything you know: [LIST]. Format: structured Markdown per topic."`
**Trigger:** After THOUGHT-LINE-SEEDING-GATE completes full taxonomy

---

## CH-008 — Other LLM Sessions

| Source | Metadata-Only | Content Pilot | Extraction Pilot | Full Extraction | Mutation Risk | Blockers | Next Gate |
|---|---|---|---|---|---|---|---|
| INST-SES-001→004 | `BLOCKED` | `BLOCKED` | `BLOCKED` | `BLOCKED` | None | No export API | CAPTURE-PATCH-2 |

**Resolution:** Manual export or structured prompt extraction per platform

---

## CH-009 — Generated Sites

| Source | Metadata-Only | Content Pilot | Extraction Pilot | Full Extraction | Mutation Risk | Blockers | Next Gate |
|---|---|---|---|---|---|---|---|
| INST-SITE-001/002 (Git) | `READY` | `PENDING-GATE` | `PENDING-GATE` | `PENDING-GATE` | None | None | GITHUB-SOURCE-ACQUISITION-GATE |
| INST-SITE-004 Deployed | `BLOCKED` | `BLOCKED` | `BLOCKED` | `BLOCKED` | None | URLs unknown | MANUS-SITES-INVENTORY-GATE |

---

## CH-010 — Generated Apps (no Git)

| Source | Metadata-Only | Content Pilot | Extraction Pilot | Full Extraction | Mutation Risk | Blockers | Next Gate |
|---|---|---|---|---|---|---|---|
| INST-APP-001/002 | `BLOCKED` | `BLOCKED` | `BLOCKED` | `BLOCKED` | None | No inventory | REPLIT-LOVABLE-INVENTORY-GATE |

---

## Pipeline Readiness Summary

| Channel | Metadata-Only Ready | Content Pilot Ready | Blockers |
|---|---|---|---|
| CH-001 Git | ✅ 39 repos | ⏳ Pending gate | None |
| CH-002 ChatGPT | ✅ 2 packs | ⏳ Pending gate | 6 sessions pending user export |
| CH-003 Manus | ✅ Complete | ⏳ Pending gate | None |
| CH-004 Obsidian | ✅ 2 Git vaults | ❌ 7 local blocked | Vault paths unknown |
| CH-005 Notion | ✅ Y-World | ⏳ Pending gate | Census incomplete |
| CH-006 Mem0 | ✅ Complete | N/A | None |
| CH-007 LLM Internal | N/A | ⏳ Deferred | Taxonomy not complete |
| CH-008 Other LLM | ❌ Blocked | ❌ Blocked | No export API |
| CH-009 Sites | ✅ 2 Git | ❌ Deployed blocked | URLs unknown |
| CH-010 Apps | ❌ Blocked | ❌ Blocked | No inventory |
