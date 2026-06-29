# yOS Continuity Core

**Subtitle: Context, Memory, Session & Handoff Continuity Layer**
**Version:** 1.0 (Canonical Consolidation)
**Module Status:** CORE MODULE — yOS Essential Value Proposition

---

## 1. Mission

Define once and for all how yOS preserves coherence across:
* sessions
* tools
* LLMs
* agents
* missions
* project phases
* time
* handoffs
* recovery events
* governance gates

This document consolidates:
* ADR-0027 Context Continuity Validation
* ADR-0036 Y-OS Canonical Context Architecture
* CCR Runtime v1 & v1.1 Governance Patch
* MISSION-010B Context Architecture ROI Analysis
* Handoff & Communication Protocol v0.1
* yOS Orchestration Core doctrine
* 7 Intelligences architecture
* yOS LLM & Tool Routing Matrix
* QC Debt doctrine
* L3/L4 authority model
* Context Pack boundary doctrine
* `previous_response_id` bounded session continuity
* Canonical Memory injection policy
* Mode resolution policy

---

## 2. Canonical Doctrine

1. yOS may use growing session context for local continuity inside the same active coherent work thread.
2. yOS does not treat long conversational memory as organizational truth.
3. When context crosses boundaries between LLMs, tools, agents, sessions, missions, project phases, or authority levels, continuity must be carried by artifact-backed Context Packs.
4. Fresh or formally re-contextualized sessions with mission-specific Context Packs are required for handoff, recovery, governance-sensitive work, model switching, tool switching, major phase transitions, or drift recovery.
5. Canonical Memory is injected only when required by risk, governance, architecture, full-project recovery, constitutional/canonical work, or explicit user request.
6. Short Session Context may be used manually, parametrically, programmatically, by matrix default, or through proactive Manus suggestion for bounded multi-turn continuity.
7. `previous_response_id` is an optional bounded session-continuity mechanism. It is useful for local multi-turn reasoning but must not become canonical memory.
8. All authoritative continuity must remain artifact-backed, traceable, and governed.
9. Continuity is not memory. Continuity is governed context transfer.
10. Same session while coherent. Context Pack at boundaries. Canonical Memory when authority or risk requires it. `previous_response_id` when useful. Ledger always.

---

## 3. Three Continuity Types

### 3.1 Local Session Continuity
Used inside the same coherent working thread.
**May rely on:**
* current session context
* growing conversation context
* `previous_response_id`
* short-lived execution context

**Valid when:**
* same topic, sub-mission, actor, tool/LLM
* no major phase shift
* no authority-level change
* context size remains reasonable
* no drift detected

*Must not be treated as organizational truth.*

### 3.2 Handoff Continuity
Used when passing work across boundaries (LLMs, tools, agents, sessions, missions, APIs, project phases, execution environments).
**Must rely on:**
* Context Pack
* source artifact manifest
* mission state
* active constraints
* decisions
* risks
* expected output
* handoff instructions

*This is mandatory at boundaries.*

### 3.3 Organizational Continuity
Used for truth, canon, decisions, governance, and long-term project memory.
**Must rely on:**
* Canonical Memory / Memory Backend (Mem0 / Notion / Git / Registry / manual artifact input)
* ADRs
* registries
* decision ledgers
* program state
* source artifacts
* governance reviews
* versioned reports
* Git history where applicable

*Conversation history is not organizational truth unless captured as an artifact.*

---

## 4. Relation to FCS / ELYSIUM Book

FCS is a downstream application. ELYSIUM Book uses FCS.
FCS must consume yOS Continuity Core, not own it.

FCS uses Continuity Core for:
* prose generation
* module review
* API handoff
* Claude drafting
* ChatGPT review
* QA/QC gates
* context pack refresh
* binder/module transitions
* foundation transitions
* Founder Review
* F02 start gate

**Explicit Rule:** No F02 until the relevant gate is explicitly approved.
