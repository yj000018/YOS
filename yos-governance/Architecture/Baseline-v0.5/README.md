# Y-OS Architecture Baseline v0.5

**Status:** Working canon derived from the completed internal ChatGPT memory consolidation round.
**Purpose:** Provide a stable, explicit reading grid for the next evidence waves: GitHub, Manus, Markdown/Obsidian, Notion, other LLMs, then ARCH transcript reconciliation.
**Authority level:** Provisional. This baseline guides investigation; it does not freeze the final Y-OS architecture.

## Governing rule

> Consolidate the existing Y-OS before inventing the next Y-OS.

No new top-level module may be introduced unless a documented gap remains after source reconciliation.

## Included documents

1. [`00-Executive-Baseline.md`](00-Executive-Baseline.md) — executive synthesis, mission, five-plane model, and canonical distinctions.
2. [`01-Vision-Principles-and-Scope.md`](01-Vision-Principles-and-Scope.md) — mission, strategic hierarchy, governing principles, scope, and non-goals.
3. [`02-Five-Plane-Architecture.md`](02-Five-Plane-Architecture.md) — Experience, Control, Cognitive, Knowledge, and Growth planes.
4. [`03-Module-Registry.md`](03-Module-Registry.md) — comprehensive provisional registry of modules, aliases, responsibilities, dependencies, and open questions.
5. [`04-Boundary-Contracts.md`](04-Boundary-Contracts.md) — ownership and interface contracts across modules and planes.
6. [`05-Concept-Lineage-and-Supersession.md`](05-Concept-Lineage-and-Supersession.md) — naming history, splits, merges, rejected concepts, supersession, and historical lineage.
7. [`06-Historical-Decisions-and-ADRs.md`](06-Historical-Decisions-and-ADRs.md) — recovered decisions and ADR-oriented history.
8. [`07-Implementation-Evidence-Matrix.md`](07-Implementation-Evidence-Matrix.md) — reported implementation state, confidence, and verification requirements.
9. [`08-Open-Questions-and-ADR-Queue.md`](08-Open-Questions-and-ADR-Queue.md) — unresolved architecture questions and prioritized ADR queue.
10. [`09-Growth-Plane.md`](09-Growth-Plane.md) — feedback, evaluation, learning, capability lifecycle, promotion, rollback, and controlled evolution.
11. [`10-Source-Wave-Roadmap.md`](10-Source-Wave-Roadmap.md) — GitHub, Manus, Markdown/Obsidian, Notion, other LLM, and ARCH evidence waves.
12. [`11-Source-of-Truth-Matrix.md`](11-Source-of-Truth-Matrix.md) — declared roles of Git, ARCH, KAP, Obsidian, Notion, Y-REG, Y-Nexus, and runtime stores.
13. [`12-Glossary-and-Acronyms.md`](12-Glossary-and-Acronyms.md) — normalized terminology, acronyms, aliases, and unresolved names.
14. [`13-Canon-Promotion-Rules.md`](13-Canon-Promotion-Rules.md) — evidence hierarchy, promotion ladders, contradiction handling, supersession, and no-invention rules.

## Recommended reading order

```text
00 Executive Baseline
→ 01 Vision and Principles
→ 02 Five-Plane Architecture
→ 03 Module Registry
→ 04 Boundary Contracts
→ 05 Concept Lineage
→ 06 Historical Decisions
→ 07 Implementation Evidence
→ 08 Open Questions / ADR Queue
→ 09 Growth Plane
→ 10 Source-Wave Roadmap
→ 11 Source-of-Truth Matrix
→ 12 Glossary
→ 13 Canon Promotion Rules
```

## Current baseline hierarchy

```text
KOSMOS
  ↓ philosophical foundation
Theory of Cognition
  ↓ functional translation
Y-OS
  ├── Experience Plane
  ├── Control Plane
  ├── Cognitive Plane
  ├── Knowledge Plane
  └── Growth Plane
        ↓
Applications, agents, tools, workflows, environments, and embodied systems
```

## Status vocabulary

- **CANON** — formally accepted architecture.
- **WORKING_CANON** — current best architecture used provisionally.
- **IMPLEMENTATION_CLAIM** — implementation was reported but not yet verified.
- **IMPLEMENTED** — code or executable configuration was inspected.
- **RUNNABLE** — implementation can execute in a defined environment.
- **DEPLOYED** — installed or available in an intended environment.
- **OPERATIONAL** — recent successful execution is evidenced.
- **PROPOSED** — explicit proposal not yet canonized.
- **OPEN** — unresolved.
- **SUPERSEDED** — replaced but historically preserved.
- **HISTORICAL** — important prior state.
- **REJECTED** — explicitly declined.
- **CONFLICTING** — incompatible definitions remain.
- **UNVERIFIED** — insufficient evidence.

## Canonical operating formulas

> Manus directs the program.

> Codex builds by default.

> Claude Code challenges or takes work where it is superior.

> CRT chooses who thinks and how.

> ART chooses who or what acts, with which agents, tools, APIs, MCPs, runtimes, and effectors.

> ARCH preserves evidence. KAP structures validated knowledge. Git preserves durable artifacts and implementation history.

> No major work in a native LLM interface without a measurable functional advantage and a recoverable path through ARCH.

## Phase-completion declaration

The internal ChatGPT consolidation round is complete to the limit of currently retrievable internal memory.

The remaining gaps are evidence and raw-transcript gaps, not unfinished ChatGPT-memory search gaps.

## Next gate

This baseline must now be tested against GitHub evidence. The next work is not redesign; it is repository census, verification, reconciliation, correction, and promotion or downgrading of claims according to `13-Canon-Promotion-Rules.md`.
