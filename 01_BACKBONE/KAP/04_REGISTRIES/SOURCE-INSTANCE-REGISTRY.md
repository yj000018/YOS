# SOURCE-INSTANCE-REGISTRY

> Y-OS / KAP — Level 2: Source Instances
> A **Source Instance** is a concrete, identifiable unit within a Channel.
> See `SOURCE-CHANNEL-REGISTRY.md` for Level 1 (channels).
> See `KAP-SOURCE-MATRIX.md` for status matrix.
> Last Updated: 2026-07-03
> **Living document — add new instances immediately on discovery.**

---

## Instance Status Vocabulary

| Status | Meaning |
|---|---|
| `ACQUIRED` | Content in Git, available for fragment extraction |
| `CATALOGUED` | Identified and inventoried, not yet acquired |
| `DISCOVERED` | Known to exist, not yet inventoried |
| `PENDING` | Awaiting user action (export, upload, access grant) |
| `BLOCKED` | Cannot access — requires resolution |
| `DEFERRED` | Out of scope for current phase |

---

## CH-001 — Git / GitHub (41 repos)

| inst_id | ch_id | Name | URL | Visibility | Scope | Status | Priority | Notes |
|---|---|---|---|---|---|---|---|---|
| INST-GIT-001 | CH-001 | yos-cognitive-os | github.com/yj000018/yos-cognitive-os | public | yos | `ACQUIRED` | P1 | Master control plane. Active. |
| INST-GIT-002 | CH-001 | KAP | github.com/yj000018/KAP | public | yos | `ACQUIRED` | P1 | KAP module repo. Active. |
| INST-GIT-003 | CH-001 | YOS (main) | github.com/yj000018/YOS | public | yos | `CATALOGUED` | P1 | Contains Y-WORLD Obsidian vault (229+ .md), yos-agents/ |
| INST-GIT-004 | CH-001 | YOS (master) | github.com/yj000018/YOS@master | public | yos | `CATALOGUED` | P1 | Historical mission logs |
| INST-GIT-005 | CH-001 | YOS (y-os-doctrine) | github.com/yj000018/YOS@y-os-doctrine | public | yos | `CATALOGUED` | P2 | Doctrine branch |
| INST-GIT-006 | CH-001 | YOS (phase-iii) | github.com/yj000018/YOS@phase-iii | public | yos | `CATALOGUED` | P1 | Continuity Core consolidation |
| INST-GIT-007 | CH-001 | elysium-civilizational-ontology | github.com/yj000018/elysium-civilizational-ontology | public | yos | `CATALOGUED` | P2 | ELYSIUM ontology, final reports |
| INST-GIT-008 | CH-001 | elysium-book | github.com/yj000018/elysium-book | public | yos | `CATALOGUED` | P2 | ELYSIUM book manuscript |
| INST-GIT-009 | CH-001 | Y-WORLD | github.com/yj000018/Y-WORLD | private | yos | `CATALOGUED` | P1 | Y-WORLD Obsidian vault as Git repo |
| INST-GIT-010 | CH-001 | yos-bus | github.com/yj000018/yos-bus | private | yos | `CATALOGUED` | P1 | Cognitive backbone, inter-agent bus |
| INST-GIT-011 | CH-001 | yos-project | github.com/yj000018/yos-project | private | yos | `CATALOGUED` | P1 | Y-OS main project repo |
| INST-GIT-012 | CH-001 | yos-llm-pipeline | github.com/yj000018/yos-llm-pipeline | private | yos | `CATALOGUED` | P1 | LLM Knowledge Distillation Pipeline v1.2 |
| INST-GIT-013 | CH-001 | yos-skills | github.com/yj000018/yos-skills | private | yos | `CATALOGUED` | P1 | Manus Skills (memoriser, hydrater, etc.) |
| INST-GIT-014 | CH-001 | yos-continuity-protocol | github.com/yj000018/yos-continuity-protocol | private | yos | `CATALOGUED` | P1 | Continuity protocol |
| INST-GIT-015 | CH-001 | yos-governance | github.com/yj000018/yos-governance | private | yos | `CATALOGUED` | P2 | Governance docs |
| INST-GIT-016 | CH-001 | yos-voice-gateway | github.com/yj000018/yos-voice-gateway | private | yos | `CATALOGUED` | P3 | Voice gateway |
| INST-GIT-017 | CH-001 | yos-voice-vision | github.com/yj000018/yos-voice-vision | private | yos | `CATALOGUED` | P3 | Voice + vision interface |
| INST-GIT-018 | CH-001 | casa-tao-nest | github.com/yj000018/casa-tao-nest | private | yos | `CATALOGUED` | P3 | Casa Tao Nest |
| INST-GIT-019 | CH-001 | eia-awakening-petal | github.com/yj000018/eia-awakening-petal | private | yos | `CATALOGUED` | P2 | EIA Awakening Petal |
| INST-GIT-020 | CH-001 | future-news-project | github.com/yj000018/future-news-project | private | yos | `CATALOGUED` | P3 | Future News project |
| INST-GIT-021 | CH-001 | pulse-app | github.com/yj000018/pulse-app | private | yos | `CATALOGUED` | P3 | Pulse demo app |
| INST-GIT-022 | CH-001 | remotion-project | github.com/yj000018/remotion-project | private | yos | `CATALOGUED` | P3 | Remotion video engine |
| INST-GIT-023 | CH-001 | yos-scripts | github.com/yj000018/yos-scripts | public | yos | `CATALOGUED` | P2 | YOS Hub userscripts + automation |
| INST-GIT-024 | CH-001 | yos-manus-client | github.com/yj000018/yos-manus-client | public | yos | `CATALOGUED` | P2 | TamperMonkey client for manus.im |
| INST-GIT-025 | CH-001 | yos-cockpit | github.com/yj000018/yos-cockpit | public | yos | `CATALOGUED` | P2 | Cognitive Cockpit Brave extension |
| INST-GIT-026 | CH-001 | yos-userscripts | github.com/yj000018/yos-userscripts | public | yos | `CATALOGUED` | P2 | Auto-updatable userscripts |
| INST-GIT-027 | CH-001 | manus-enhancer | github.com/yj000018/manus-enhancer | public | yos | `CATALOGUED` | P2 | Manus interface enhancer |
| INST-GIT-028 | CH-001 | y-llm-exporter | github.com/yj000018/y-llm-exporter | public | yos | `CATALOGUED` | P2 | Chrome extension LLM export |
| INST-GIT-029 | CH-001 | y-menu | github.com/yj000018/y-menu | public | yos | `CATALOGUED` | P2 | Y-Menu cognitive orchestration |
| INST-GIT-030 | CH-001 | one-galaxy | github.com/yj000018/one-galaxy | public | yos | `CATALOGUED` | P3 | Galaxy Navigator 3D viz |
| INST-GIT-031 | CH-001 | civilizational-awakening | github.com/yj000018/civilizational-awakening | public | yos | `CATALOGUED` | P3 | React site |
| INST-GIT-032 | CH-001 | relevance-ai-workforce | github.com/yj000018/relevance-ai-workforce | public | yos | `CATALOGUED` | P3 | Relevance AI workforce |
| INST-GIT-033 | CH-001 | YMap | github.com/yj000018/YMap | public | yos | `CATALOGUED` | P3 | YMap |
| INST-GIT-034 | CH-001 | Y-Browser-Admin | github.com/yj000018/Y-Browser-Admin | public | yos | `CATALOGUED` | P3 | Browser admin |
| INST-GIT-035 | CH-001 | UniversalChatThemeCanon | github.com/yj000018/UniversalChatThemeCanon | public | yos | `CATALOGUED` | P3 | Universal chat theme canon |
| INST-GIT-036 | CH-001 | youniverse | github.com/yj000018/youniverse | public | youniverse | `CATALOGUED` | P2 | 3D OS Interface — Phase 2 |
| INST-GIT-037 | CH-001 | daylog | github.com/yj000018/daylog | public | youniverse | `DEFERRED` | P3 | Day log — Phase 2 |
| INST-GIT-038 | CH-001 | daylog-mvp | github.com/yj000018/daylog-mvp | public | youniverse | `DEFERRED` | P3 | Day log MVP — Phase 2 |
| INST-GIT-039 | CH-001 | desktop-tutorial | github.com/yj000018/desktop-tutorial | private | yos | `DEFERRED` | P4 | GitHub Desktop tutorial — legacy |
| INST-GIT-040 | CH-001 | yannick | github.com/yj000018/yannick | public | youniverse | `DEFERRED` | P4 | DatoCMS/Gatsby sample — legacy |
| INST-GIT-041 | CH-001 | (additional repos) | github.com/yj000018 | — | yos | `DISCOVERED` | P3 | Remaining repos from API page 2+ |

---

## CH-002 — ChatGPT

| inst_id | ch_id | Name | Location | Scope | Status | Priority | Notes |
|---|---|---|---|---|---|---|---|
| INST-GPT-001 | CH-002 | ChatGPT KAP Bootstrap Session Pack | yos-cognitive-os/00_Control_Plane/Session_Captures/ | yos | `ACQUIRED` | P1 | 2026-07-02. Full body in Git. |
| INST-GPT-002 | CH-002 | ChatGPT KAP Current Session Pack | yos-cognitive-os/00_Control_Plane/Session_Captures/ | yos | `ACQUIRED` | P1 | 2026-07-03. Full body in Git. |
| INST-GPT-003 | CH-002 | ChatGPT KAP Parallel Sessions (6+) | chat.openai.com — KAP GPT | yos | `PENDING` | P1 | 6 parallel sessions not yet exported. Capture Patch 2 required. |
| INST-GPT-004 | CH-002 | ChatGPT General Sessions | chat.openai.com | both | `PENDING` | P2 | Full conversations.json not provided. Unknown volume. |

---

## CH-003 — Manus

| inst_id | ch_id | Name | Location | Scope | Status | Priority | Notes |
|---|---|---|---|---|---|---|---|
| INST-MAN-001 | CH-003 | Manus Durable Gate Reports | yos-cognitive-os/ + KAP/ repos | yos | `ACQUIRED` | P1 | All gate reports, registries, models in Git. |
| INST-MAN-002 | CH-003 | Manus Historical Tasks (194 sessions) | Notion Manus Memory + Mem0 | yos | `CATALOGUED` | P2 | Non-primary corpus. Capture packs in Git. Full session content in Notion/Mem0. |

---

## CH-004 — Obsidian / Markdown

| inst_id | ch_id | Name | Location | Scope | Status | Priority | Notes |
|---|---|---|---|---|---|---|---|
| INST-OBS-001 | CH-004 | Y-WORLD vault (in YOS repo) | github.com/yj000018/YOS → yos-vault/knowledge/Y-WORLD/ | yos | `CATALOGUED` | P1 | 229+ .md files. Accessible via GitHub API. |
| INST-OBS-002 | CH-004 | Y-WORLD vault (standalone repo) | github.com/yj000018/Y-WORLD | yos | `CATALOGUED` | P1 | May overlap with INST-OBS-001. |
| INST-OBS-003 | CH-004 | Obsidian local vaults (7 unknown) | Mac filesystem — paths unknown | yos | `BLOCKED` | P2 | User confirmed 9 total vaults. 7 paths not yet identified. Requires OBSIDIAN-VAULT-DISCOVERY-GATE. |

---

## CH-005 — Notion

| inst_id | ch_id | Name | Location | Scope | Status | Priority | Notes |
|---|---|---|---|---|---|---|---|
| INST-NOT-001 | CH-005 | Y-World workspace (primary) | notion.so — Y-World | yos | `CATALOGUED` | P1 | API accessible. Education Plus. has_more: true. Census incomplete. |
| INST-NOT-002 | CH-005 | Yannick personal workspace | notion.so — Yannick | both | `DISCOVERED` | P2 | Legacy personal workspace. May contain yOS content. |
| INST-NOT-003 | CH-005 | Namaste-Welfare workspace | notion.so — Namaste-Welfare | youniverse | `DEFERRED` | P3 | Old NGO account. Phase 2 only. |

---

## CH-006 — Mem0

| inst_id | ch_id | Name | Location | Scope | Status | Priority | Notes |
|---|---|---|---|---|---|---|---|
| INST-MEM-001 | CH-006 | Mem0 store (user_id: yannick) | api.mem0.ai | yos | `ACQUIRED` | P1 | 316 entries. Signal/index only. API confirmed. |

---

## CH-007 — Internal LLM Knowledge

| inst_id | ch_id | Name | Location | Scope | Status | Priority | Notes |
|---|---|---|---|---|---|---|---|
| INST-LLM-001 | CH-007 | Claude internal knowledge | claude.ai | both | `PENDING` | P2 | Deferred until taxonomy complete. Batch prompt extraction. |
| INST-LLM-002 | CH-007 | ChatGPT internal knowledge | chat.openai.com | both | `PENDING` | P2 | Deferred until taxonomy complete. |
| INST-LLM-003 | CH-007 | Gemini internal knowledge | gemini.google.com | both | `PENDING` | P2 | Deferred until taxonomy complete. |
| INST-LLM-004 | CH-007 | Grok internal knowledge | grok.x.ai | both | `PENDING` | P3 | Deferred until taxonomy complete. |
| INST-LLM-005 | CH-007 | Future LLMs | TBD | both | `DISCOVERED` | P3 | Open list — add on activation. |

---

## CH-008 — Other LLM Sessions

| inst_id | ch_id | Name | Location | Scope | Status | Priority | Notes |
|---|---|---|---|---|---|---|---|
| INST-SES-001 | CH-008 | Claude session history | claude.ai | both | `BLOCKED` | P2 | No export API. Manual copy or prompt extraction. |
| INST-SES-002 | CH-008 | Gemini session history | gemini.google.com | both | `BLOCKED` | P2 | Limited export. Manual or prompt extraction. |
| INST-SES-003 | CH-008 | Grok session history | grok.x.ai | both | `BLOCKED` | P3 | No export API. |
| INST-SES-004 | CH-008 | Perplexity session history | perplexity.ai | both | `BLOCKED` | P3 | Research queries. No export API. |

---

## CH-009 — Generated Sites (Manus / Lovable)

| inst_id | ch_id | Name | Location | Scope | Status | Priority | Notes |
|---|---|---|---|---|---|---|---|
| INST-SITE-001 | CH-009 | civilizational-awakening | github.com/yj000018/civilizational-awakening | yos | `CATALOGUED` | P3 | Code in Git. |
| INST-SITE-002 | CH-009 | one-galaxy | github.com/yj000018/one-galaxy | yos | `CATALOGUED` | P3 | Code in Git. |
| INST-SITE-003 | CH-009 | youniverse site | github.com/yj000018/youniverse | youniverse | `DEFERRED` | P3 | Phase 2. |
| INST-SITE-004 | CH-009 | Manus deployed sites (no Git) | manus.im — unknown URLs | yos | `BLOCKED` | P2 | URLs not inventoried. Requires MANUS-SITES-INVENTORY-GATE. |

---

## CH-010 — Generated Apps (no Git)

| inst_id | ch_id | Name | Location | Scope | Status | Priority | Notes |
|---|---|---|---|---|---|---|---|
| INST-APP-001 | CH-010 | Replit apps | replit.com | yos | `BLOCKED` | P3 | No inventory. Platform login required. |
| INST-APP-002 | CH-010 | Lovable apps (no Git) | lovable.dev | yos | `BLOCKED` | P3 | No inventory. Platform login required. |

---

## CH-013 — Generic Uploaded Files

| inst_id | ch_id | Name | Location | Scope | Status | Priority | Notes |
|---|---|---|---|---|---|---|---|
| INST-UPL-001 | CH-013 | Session upload files (this session) | /home/ubuntu/upload/ | yos | `ACQUIRED` | P1 | MPM packs, capture packs — all persisted to Git. |

---

## Instance Summary

| Channel | Total Instances | ACQUIRED | CATALOGUED | PENDING | BLOCKED | DEFERRED |
|---|---|---|---|---|---|---|
| CH-001 Git | 41 | 2 | 35 | 0 | 0 | 4 |
| CH-002 ChatGPT | 4 | 2 | 0 | 2 | 0 | 0 |
| CH-003 Manus | 2 | 1 | 1 | 0 | 0 | 0 |
| CH-004 Obsidian | 3 | 0 | 2 | 0 | 1 | 0 |
| CH-005 Notion | 3 | 0 | 1 | 0 | 0 | 2 |
| CH-006 Mem0 | 1 | 1 | 0 | 0 | 0 | 0 |
| CH-007 LLM Internal | 5 | 0 | 0 | 4 | 0 | 1 |
| CH-008 Other LLM | 4 | 0 | 0 | 0 | 4 | 0 |
| CH-009 Sites | 4 | 0 | 2 | 0 | 1 | 1 |
| CH-010 Apps | 2 | 0 | 0 | 0 | 2 | 0 |
| CH-013 Uploads | 1 | 1 | 0 | 0 | 0 | 0 |
| **TOTAL** | **70** | **7** | **41** | **6** | **8** | **8** |

---

## OBSIDIAN-MARKDOWN-METADATA-DRY-RUN-GATE — Instance Updates (2026-07-03)

### INST-OBS-002 — Y-WORLD Vault (Git-backed) — Updated

| Field | Value |
|---|---|
| source_instance_id | INST-OBS-002 |
| channel_id | CH-004 |
| name | Y-WORLD — World Operating System (standalone Git repo) |
| source_type | git_backed_obsidian_vault |
| location | github.com/yj000018/Y-WORLD (private) |
| access_status | `ACCESSIBLE` — GitHub API read-only confirmed |
| metadata_status | `COMPLETED` — 235 notes, 21 folders, 74 wikilinks, 17 with frontmatter |
| content_status | `BLOCKED` — no body content ingested |
| pipeline_status | `METADATA_DRY_RUN_COMPLETE` |
| next_safe_gate | OBSIDIAN-LIMITED-CONTENT-PILOT-GATE |
| notes | Case C (Git-backed). Scan via GitHub API recursive tree. 5 files with spaces in names had minor urllib encoding issue. Attachments not tracked in Git tree. 1 duplicate title: "Untitled". |

### INST-OBS-LOCAL — Local Mac Vaults — SUPERSEDED

> **SUPERSEDED** by OBSIDIAN-LOCAL-VAULT-DISCOVERY-GATE (2026-07-03). See individual vault instances below.

| Field | Value |
|---|---|
| source_instance_id | INST-OBS-LOCAL |
| channel_id | CH-004 |
| name | Local Obsidian Vaults — Mac filesystem |
| source_type | local_obsidian_vault |
| access_status | `SUPERSEDED` — replaced by 5 individual vault instances |
| pipeline_status | `DISCOVERY_COMPLETE` |
| notes | Mac connected 2026-07-03. 5 vaults discovered. See INST-OBS-LUDIVINE through INST-OBS-TESTING below. |


---

## Notion Source Instances (added: NOTION-METADATA-INVENTORY-GATE)

| Instance ID | Name | Workspace ROOT | L2 Children | Status | Scope |
|---|---|---|---|---|---|
| INST-NOTION-YOS | Y-OS ROOT | `- Y-OS ROOT -` | 16 | `METADATA_DRY_RUN_COMPLETE` | yos |
| INST-NOTION-YWORLD | Y-World ROOT | `- Y-World ROOT -` | 20 | `METADATA_DRY_RUN_COMPLETE` | both |
| INST-NOTION-YANNICK | Yannick ROOT | `- Yannick ROOT -` | 7 | `METADATA_DRY_RUN_COMPLETE` | yos |
| INST-NOTION-ELYSIUM | ELYSIUM ROOT | `- ELYSIUM ROOT -` | 7 | `METADATA_DRY_RUN_COMPLETE` | youniverse |
| INST-NOTION-KOSMOS | KOSMOS ROOT | `- KOSMOS ROOT -` | 0 | `METADATA_DRY_RUN_COMPLETE_EMPTY` | youniverse |
| INST-NOTION-BLOCKED | Blocked / Inaccessible | — | — | `BLOCKED` | — |

**Scan date:** 2026-07-03
**Scan method:** ROOT-anchored L1+L2 metadata-only (Notion API read-only)
**Total objects registered:** 55 (5 L1 ROOT + 50 L2 children)

---

## GitHub Source Instances (added: GITHUB-SOURCE-METADATA-PILOT-GATE)

| Instance ID | Full Name | Default Branch | Archived | Workflows | Status | Scope |
|---|---|---|---|---|---|---|
| INST-GITHUB-YOS | yj000018/yos-cognitive-os | main | No | 0 | `METADATA_PILOT_COMPLETE` | yos |
| INST-GITHUB-YWORLD | yj000018/Y-WORLD | main | Yes (GitHub flag) | 1 (compile-graph.yml) | `METADATA_PILOT_COMPLETE_ARCHIVED_FLAG` | both |
| INST-GITHUB-CANDIDATE | yj000018/* (10 repos) | — | No | — | `CANDIDATE_NOT_SCANNED` | mixed |
| INST-GITHUB-BLOCKED | Blocked / Inaccessible | — | — | — | `BLOCKED` | — |

**Scan date:** 2026-07-03
**Scan method:** GitHub API read-only — repo metadata + L1+L2 tree metadata only
**Total repos discovered:** 23 (2 scanned + 10 candidates + 11 archived)
**Note:** Y-WORLD archived flag on GitHub is likely a legacy/incorrect flag — active workflow and recent commits present.

---

## Obsidian Local Vault Instances (added: OBSIDIAN-LOCAL-VAULT-DISCOVERY-GATE)

**Discovery date:** 2026-07-03
**Discovery method:** `find -name .obsidian -type d` via Manus desktop bridge (macOS)
**Content extracted:** NONE
**Source mutated:** NONE
**Paths:** Redacted in public files — aliases used

| Instance ID | Name | Alias | Sync | MD Files | Status | KAP Role |
|---|---|---|---|---|---|---|
| INST-OBS-LUDIVINE | LUDIVINE_OBSIDIAN_VAULT | `LOCAL://LUDI/LUDIVINE_VAULT` | Local only | 1842 | `DISCOVERED_NOT_AUTHORIZED_PENDING_SCOPE_DECISION` | Principal local vault candidate |
| INST-OBS-LUDIVINE-BACKUP | LUDIVINE_OBS_BACKUP | `LOCAL://LUDI/LUDIVINE_BACKUP` | Local only | 1418 | `BACKUP_EXCLUDE_BY_DEFAULT` | Backup duplicate |
| INST-OBS-YWORLD-ICLOUD | Y-World (iCloud) | `ICLOUD://obsidian/Y-World` | iCloud | 17 | `DISCOVERED_LOW_PRIORITY` | Small experimental vault |
| INST-OBS-TEST | Test (iCloud) | `ICLOUD://obsidian/Test` | iCloud | ~8 | `EXCLUDE_BY_DEFAULT` | Test vault |
| INST-OBS-TESTING | testing (local) | `LOCAL://TESTS/testing` | Local only | ~5 | `EXCLUDE_BY_DEFAULT` | Test vault |

**Key findings:**
- LUDIVINE is the only substantial local Obsidian vault (1842 md). It is a creative/intellectual project vault, NOT a Y-OS system vault.
- The real Y-World content is on GitHub (INST-GITHUB-YWORLD), not in the iCloud Obsidian vault (only 17 md files).
- Guardian must authorize LUDIVINE before any content access or dry-run execution.
- No next gate started. Paused pending Guardian review.
