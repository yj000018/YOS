# CHANNEL-REGISTRY

> Y-OS / KAP — Level 1 Source Management
> A **Channel** is a platform, tool, or system that hosts one or more Sources.
> Last Updated: 2026-07-03
> **Living document — update on every new channel discovery.**

---

## Architecture

```
CHANNEL (platform/system)
  └── SOURCE (individual unit within the channel)
        └── FRAGMENT (extracted atomic knowledge unit)
              └── CLAIM (validated assertion)
                    └── THOUGHT LINE (thematic thread)
```

---

## Channel Status Vocabulary

| Status | Meaning |
|---|---|
| `ACTIVE` | Channel confirmed, connector operational |
| `CATALOGUED` | Channel identified, connector not yet built |
| `PARTIAL` | Channel accessible but not fully configured |
| `BLOCKED` | Channel identified, access not yet possible |
| `DEFERRED` | Out of scope for current phase |
| `DEPRECATED` | No longer used |

---

## Channel Scope Vocabulary

| Scope | Meaning |
|---|---|
| `yos` | yOS cognitive architecture knowledge |
| `youniverse` | Personal data, life data, behavioral data |
| `both` | Contains both yOS and personal content |

---

## Channel Phase Vocabulary

| Phase | Meaning |
|---|---|
| `phase-1` | Active in KAP Phase 1 (yOS consolidation) |
| `phase-2` | Activated in Phase 2 (YOUniverse expansion) |
| `future` | Not yet planned, connector TBD |

---

## Channel Registry

| ch_id | Channel Name | Platform/System | Scope | Phase | Status | Sources Count | Connector | Auth Method | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| CH-001 | GitHub | github.com/yj000018 | `yos` | phase-1 | `ACTIVE` | 41 repos | GitHub REST API v3 | PAT (KAP .env) | Primary code + docs channel |
| CH-002 | Obsidian | Local Mac + Git-backed | `yos` | phase-1 | `PARTIAL` | 9 vaults (2 confirmed, 7 unknown) | Filesystem + GitHub API | PAT (Git-backed) / Mac FUSE (local) | 9 vaults confirmed by user. 7 paths unknown. |
| CH-003 | Notion | notion.so | `yos` | phase-1 | `ACTIVE` | 3 workspaces (1 active) | Notion REST API v1 | Integration key (KAP .env) | Primary structured knowledge channel |
| CH-004 | Manus | manus.im | `yos` | phase-1 | `ACTIVE` | 194 sessions (in Git) | Git (already exported) | None (already in Git) | All durable outputs in yos-cognitive-os |
| CH-005 | ChatGPT | chat.openai.com | `both` | phase-1 | `PARTIAL` | ~8 sessions (2 in Git, 6 pending) | Manual export + Git | Manual | KAP GPT sessions. Parallel sessions pending export. |
| CH-006 | Mem0 | api.mem0.ai | `yos` | phase-1 | `ACTIVE` | 1 memory store (316 entries) | Mem0 REST API | API key (KAP .env) | Signal/index only. Not primary corpus. |
| CH-007 | Claude | claude.ai | `both` | phase-1 | `BLOCKED` | Unknown | Prompt extraction | Manual / API | No bulk export. Prompt-based extraction after taxonomy. |
| CH-008 | Gemini | gemini.google.com | `both` | phase-1 | `BLOCKED` | Unknown | Prompt extraction | Manual / API | Limited export. Prompt-based extraction after taxonomy. |
| CH-009 | Grok | grok.x.ai | `both` | phase-1 | `BLOCKED` | Unknown | Prompt extraction | Manual / API | No export API. Prompt-based extraction after taxonomy. |
| CH-010 | Perplexity | perplexity.ai | `both` | phase-1 | `BLOCKED` | Unknown | Prompt extraction | Manual | Research queries. Prompt-based extraction after taxonomy. |
| CH-011 | Lovable | lovable.dev | `yos` | phase-1 | `BLOCKED` | Unknown | TBD | Platform login | Apps generated via Lovable. Not inventoried. |
| CH-012 | Replit | replit.com | `yos` | phase-1 | `BLOCKED` | Unknown | TBD | Platform login | Apps deployed on Replit. Not inventoried. |
| CH-013 | Excalidraw | excalidraw.com | `both` | future | `DEFERRED` | Unknown | Webhook / export | TBD | Visual schema outputs. Future connector. |
| CH-014 | Specialized AI Tools | Various | `both` | future | `DEFERRED` | Unknown | TBD | TBD | Domain-specific AI tool outputs. Future connectors. |
| CH-015 | Google Drive | drive.google.com | `youniverse` | phase-2 | `DEFERRED` | Unknown | Google Drive API | OAuth2 | Personal/admin docs. No yOS content. Phase 2 only. |
| CH-016 | Gmail | mail.google.com | `youniverse` | phase-2 | `DEFERRED` | Unknown | Gmail API | OAuth2 | Personal communications. Phase 2 only. |
| CH-017 | Google Calendar | calendar.google.com | `youniverse` | phase-2 | `DEFERRED` | Unknown | Calendar API | OAuth2 | Behavioral data. Phase 2 only. |
| CH-018 | YouTube | youtube.com | `youniverse` | phase-2 | `DEFERRED` | Unknown | YouTube Data API | OAuth2 | Transcripts → YOUniverse. Phase 2 only. |
| CH-019 | Browser Bookmarks | Safari/Chrome | `youniverse` | phase-2 | `DEFERRED` | Unknown | Browser export | Manual | Curation external. Phase 2 only. |
| CH-020 | Browsing History | Safari/Chrome | `youniverse` | phase-2 | `DEFERRED` | Unknown | Browser export | Manual | Passive behavioral. Phase 2 only. |
| CH-021 | Voice Memos | iOS Voice Memos | `youniverse` | phase-2 | `DEFERRED` | Unknown | iOS export | Manual | Spontaneous thoughts. Phase 2 only. |

---

## Channel Summary

| Phase | Scope | Total Channels | ACTIVE | PARTIAL | BLOCKED | DEFERRED |
|---|---|---|---|---|---|---|
| phase-1 | yos/both | 12 | 4 | 2 | 6 | 0 |
| phase-2 | youniverse | 7 | 0 | 0 | 0 | 7 |
| future | both | 2 | 0 | 0 | 0 | 2 |
| **TOTAL** | | **21** | **4** | **2** | **6** | **9** |

### Phase 1 Active Channels (4)
- **CH-001 GitHub** — 41 repos, PAT confirmed ✅
- **CH-003 Notion** — 3 workspaces, API key confirmed ✅
- **CH-004 Manus** — 194 sessions in Git ✅
- **CH-006 Mem0** — 316 entries, API confirmed ✅

### Phase 1 Partial Channels (2)
- **CH-002 Obsidian** — 2/9 vaults confirmed via Git, 7 paths unknown
- **CH-005 ChatGPT** — 2/8 sessions in Git, 6 pending export

### Phase 1 Blocked Channels (6)
- **CH-007 Claude, CH-008 Gemini, CH-009 Grok, CH-010 Perplexity** — prompt extraction only, deferred until taxonomy
- **CH-011 Lovable, CH-012 Replit** — no inventory, platform login required
