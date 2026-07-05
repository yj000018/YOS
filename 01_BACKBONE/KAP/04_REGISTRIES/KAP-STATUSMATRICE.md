# KAP Statusmatrice

> Y-OS / KAP Cognitive Architecture
> Gate: CONTRADICTION-SUPERSESSION-POLICY-GATE
> Last Updated: 2026-07-03
> Status: ACTIVE

---

## In-Scope Source Families (Phase 1 — yOS Core)

| Source Family | Scope Tag | Acquisition Status | Pipeline Status | Notes |
|---|---|---|---|---|
| **Git / YOS repo** | `yos` | ✅ ACTIVE | ✅ ACTIVE | yj000018/yos-cognitive-os + yj000018/KAP. Canonical authority. |
| **ChatGPT captures (Git)** | `yos` | ✅ ACTIVE | ✅ ACTIVE | Capture packs persisted verbatim in 00_Control_Plane/Session_Captures/. CAPTURE-PATCH-2 pending. |
| **Manus durable outputs (Git)** | `yos` | ✅ ACTIVE | ✅ ACTIVE | Gate reports, registries, schemas committed to Git. |
| **Obsidian / Markdown** | `yos` | 📍 DISCOVERED | ⏳ GATED | 9 vaults. Metadata-only scan blocked until OBSIDIAN-PIPELINE-VALIDATION-GATE. |
| **Notion** | `yos` | 🔄 IN_PROGRESS | ⏳ GATED | 1300+ pages. Metadata-only intake blocked until NOTION-PIPELINE-CONTROLLED-EXECUTION-GATE. |
| **Mem0** | `yos` | ✅ ACQUIRED | 🔄 SIGNAL_ONLY | Memory/index signal only. Not a primary corpus. |
| **Internal LLM knowledge** | `both` | ⏳ DEFERRED | ⏳ DEFERRED | Extractable via structured prompts after taxonomy is known. Gate: LLM-INTERNAL-MEMORY-EXTRACTION-GATE. |
| **Sessions autres LLM** | `both` | ⏳ PLANNED | ⏳ PLANNED | Claude, Gemini, Grok, Perplexity + future LLMs. Requires explicit export/capture. |
| **Sites générés Manus / Lovable** | `yos` | ⏳ PLANNED | ⏳ PLANNED | Provenance capture required before intake. |
| **Apps générées Manus / Replit / Lovable non documentées Git** | `yos` | ⏳ PLANNED | ⏳ PLANNED | Requires documentation/provenance before intake. |

---

## Out-of-Scope / Deferred Sources

> Status: `DEFERRED_FOR_LATER_KAP_YOUNIVERSE_EXTENSION`
> These sources will be activated in Phase 2 (YOUniverse extension). Not active in current yOS Phase 1.

| Source Family | Scope Tag | Deferred Status | Notes |
|---|---|---|---|
| **Web général** | `youniverse` | DEFERRED | General web browsing/scraping. No active pipeline. |
| **Google Drive** | `youniverse` | DEFERRED | Personal/admin docs. No yOS content. Phase 2 only. |
| **Uploaded files génériques** | `youniverse` | DEFERRED | Generic uploads without provenance. Not safe for intake. |
| **Unknown / legacy non identifié** | `youniverse` | DEFERRED | Unidentified legacy sources. Require identification before any intake. |
| **YouTube / vidéos** | `youniverse` | DEFERRED | Transcripts → YOUniverse. Phase 2 only. |
| **Calendar** | `youniverse` | DEFERRED | Behavioral data. Phase 2 only. |
| **Email** | `youniverse` | DEFERRED | Personal communications. Phase 2 only. |
| **Bookmarks / Browsing History** | `youniverse` | DEFERRED | Passive behavioral data. Phase 2 only. |
| **Voice Memos** | `youniverse` | DEFERRED | Spontaneous thoughts. Phase 2 only. |

---

## Gate Sequence (Phase 1 — Active)

| Gate | Status | Commit |
|---|---|---|
| EVOLUTIONARY-KNOWLEDGE-MERGE-ARCHITECTURE-GATE | ✅ PASS | KAP repo |
| YOS-CONTROL-PLANE-BOOTSTRAP-GATE | ✅ PASS | `3ef6529` |
| SESSION-DOCTRINE-CAPTURE-GATE | ✅ PASS (with gaps) | `1e29c8c` |
| FULL-BODY-CAPTURE-PATCH | ✅ PASS | `e912532` |
| MPM-COUNT-RECONCILIATION-PATCH | ✅ PASS | `3e1ba10` |
| SOURCE-FRAGMENT-MODEL-GATE | ✅ PASS | `ff199ef` |
| SOURCE-FRAGMENT-MODEL-CONSISTENCY-PATCH | ✅ PASS | `ce3f720` |
| CLAIM-MODEL-GATE | ✅ PASS | `63f18a3` |
| THOUGHT-LINE-MODEL-GATE | ✅ PASS | `b1ffa83` |
| DECISION-THREAD-MODEL-GATE | ✅ PASS | `6c6cd60` |
| DECISION-THREAD-REQUIRED-FIELDS-PATCH | ✅ PASS | `48d5632` |
| CONTRADICTION-SUPERSESSION-POLICY-GATE | 🔄 IN_PROGRESS | — |

---

## Next Gates (Planned)

| Gate | Priority | Dependency |
|---|---|---|
| SOURCE-FRAGMENT-ID-NORMALIZATION-PATCH | HIGH | After CONTRADICTION-SUPERSESSION-POLICY-GATE |
| OBSIDIAN-PIPELINE-VALIDATION-GATE | HIGH | Before Obsidian intake |
| NOTION-PIPELINE-CONTROLLED-EXECUTION-GATE | HIGH | Before Notion intake |
| GITHUB-SOURCE-ACQUISITION-GATE | MEDIUM | 36 repos |
| CAPTURE-PATCH-2 | MEDIUM | Remaining ChatGPT parallel sessions |
| LLM-INTERNAL-MEMORY-EXTRACTION-GATE | LOW | After full taxonomy known |
