# SOURCE-CHANNEL-REGISTRY

> Y-OS / KAP — L0: Source Channels
> A **Source Channel** is an access family / connector class.
> Examples: Git, Obsidian, Notion, ChatGPT, Manus.
> **PATCHED:** SOURCE-TAXONOMY-ALIGNMENT-PATCH 2026-07-03
> Last Updated: 2026-07-03
> **Living document — add new channels immediately on discovery.**

---

## Four-Level Taxonomy

```
L0 Source Channel     (this file)
  └── L1 Source Instance  (SOURCE-INSTANCE-REGISTRY.md)
        └── L2 Source Object  (SOURCE-OBJECT-REGISTRY.md)
              └── L3 Source Fragment  (SOURCE-FRAGMENT-REGISTRY.md)
                    └── Claim → Thought Line → Decision Thread
```

---

## Channel Status Vocabulary

| Status | Meaning |
|---|---|
| `ACTIVE` | Channel confirmed, connector operational |
| `PARTIAL` | Accessible but incomplete |
| `BLOCKED` | Identified, access not yet possible |
| `DEFERRED_FOR_LATER_KAP_YOUNIVERSE_EXTENSION` | Out of scope for Phase 1 — catalogued for future YOUniverse extension |
| `DEPRECATED` | No longer used |

## Channel Scope

| Scope | Meaning |
|---|---|
| `yos` | yOS cognitive architecture knowledge |
| `youniverse` | Personal data, life data, behavioral data |
| `both` | Contains both yOS and personal content |

## Special Roles

| Role | Channels | Meaning |
|---|---|---|
| `SIGNAL_ONLY` | CH-006 Mem0 | Not a corpus — routing/semantic index only. No claim extraction without durable source artifact. |
| `HEURISTIC_CONTEXT_ONLY` | CH-007 LLM Internal | Not canonical evidence. Never used for claims without source-linked artifacts. |
| `PROVENANCE_CENSUS_ONLY` | CH-009, CH-010 | Sites/Apps — only provenance/URL/code/repo census. No content acquisition. No claims. |

---

## Channel Registry

| ch_id | Channel Name | Connector Class | Scope | Phase | Status | Role | Known Instances | Auth | Notes |
|---|---|---|---|---|---|---|---|---|---|
| CH-001 | Git / GitHub | GitHub REST API v3 | `yos` | phase-1 | `ACTIVE` | — | 41 repos | PAT (KAP .env) | Primary code + docs channel. PAT confirmed. |
| CH-002 | ChatGPT | Manual export + Git | `both` | phase-1 | `PARTIAL` | — | 2 in Git, 6+ pending | Manual | KAP GPT sessions. Parallel sessions pending. |
| CH-003 | Manus | Git (already exported) | `yos` | phase-1 | `ACTIVE` | — | 2 (194 sessions in Git) | None (in Git) | All durable outputs in yos-cognitive-os. |
| CH-004 | Obsidian / Markdown | GitHub API + Mac filesystem | `yos` | phase-1 | `PARTIAL` | — | 2 Git, 7 local unknown | PAT (Git) | 9 vaults total. 7 paths unknown. |
| CH-005 | Notion | Notion REST API v1 | `yos` | phase-1 | `PARTIAL` | — | 3 workspaces (1 active) | Integration key | Census incomplete. |
| CH-006 | Mem0 | Mem0 REST API | `yos` | phase-1 | `ACTIVE` | `SIGNAL_ONLY` | 1 store (316 entries) | API key | **Not a corpus.** Signal/index only. No claim extraction without durable artifact. |
| CH-007 | Internal LLM Knowledge | Structured prompt batch | `both` | phase-1 | `PARTIAL` | `HEURISTIC_CONTEXT_ONLY` | All active LLMs | N/A | **Not canonical evidence.** Never used for claims without source-linked artifacts. Gate renamed: LLM-HEURISTIC-CONTEXT-USAGE-POLICY. |
| CH-008 | Other LLM Sessions | Manual export / prompt | `both` | phase-1 | `BLOCKED` | — | 4 platforms | Manual | No export API. |
| CH-009 | Generated Sites (Manus/Lovable) | GitHub API + HTTP | `yos` | phase-1 | `PARTIAL` | `PROVENANCE_CENSUS_ONLY` | 3 Git, unknown deployed | PAT (Git) | Provenance/URL/code census only. No content acquisition. |
| CH-010 | Generated Apps (no Git) | TBD | `yos` | phase-1 | `BLOCKED` | `PROVENANCE_CENSUS_ONLY` | Unknown | Platform login | Provenance/code recovery only. No content acquisition. |
| CH-011 | General Web | HTTP / scraper | `both` | — | `DEFERRED_FOR_LATER_KAP_YOUNIVERSE_EXTENSION` | — | N/A | None | Out of scope Phase 1. |
| CH-012 | Google Drive | Google Drive API | `youniverse` | phase-2 | `DEFERRED_FOR_LATER_KAP_YOUNIVERSE_EXTENSION` | — | Unknown | OAuth2 | Personal docs. Phase 2 only. |
| CH-013 | Generic Uploaded Files | Manus upload | `both` | — | `DEFERRED_FOR_LATER_KAP_YOUNIVERSE_EXTENSION` | — | Session-by-session | N/A | **Not ACQUIRED in Phase 1 scope.** Files must be persisted to Git to become canonical. |
| CH-014 | Unknown / Unidentified Legacy | TBD | `both` | — | `DEFERRED_FOR_LATER_KAP_YOUNIVERSE_EXTENSION` | — | Unknown | TBD | Discovery audit required before any activation. |

---

## Channel Summary

| Phase-1 Status | Count | Channels |
|---|---|---|
| `ACTIVE` | 3 | CH-001 Git, CH-003 Manus, CH-006 Mem0 (SIGNAL_ONLY) |
| `PARTIAL` | 5 | CH-002 ChatGPT, CH-004 Obsidian, CH-005 Notion, CH-007 LLM Internal (HEURISTIC_ONLY), CH-009 Sites |
| `BLOCKED` | 2 | CH-008 Other LLM, CH-010 Apps |
| `DEFERRED_FOR_LATER_KAP_YOUNIVERSE_EXTENSION` | 4 | CH-011 Web, CH-012 GDrive, CH-013 Uploads, CH-014 Legacy |
