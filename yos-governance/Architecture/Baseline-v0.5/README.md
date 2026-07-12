# Y-OS Architecture Baseline v0.5

**Status:** Working canon derived from the completed internal ChatGPT memory consolidation round.  
**Purpose:** Provide a stable, explicit reading grid for the next evidence waves: GitHub, Markdown/Obsidian, Notion, Manus, then other LLMs and ARCH transcript reconciliation.  
**Authority level:** Provisional. This baseline guides investigation; it does not freeze the final Y-OS architecture.

## Governing rule

> Consolidate the existing Y-OS before inventing the next Y-OS.

No new top-level module may be introduced unless a documented gap remains after source reconciliation.

## Included documents

1. [`00-Executive-Baseline.md`](00-Executive-Baseline.md) — mission, principles, five-plane architecture, canonical formulas.
2. [`01-Architecture-Planes-and-Flows.md`](01-Architecture-Planes-and-Flows.md) — detailed architecture, flows, boundaries, feedback and growth.
3. [`02-Module-Registry.md`](02-Module-Registry.md) — exhaustive provisional registry of recovered modules, aliases, responsibilities and open questions.
4. [`03-Concept-Lineage-and-Supersession.md`](03-Concept-Lineage-and-Supersession.md) — naming history, merges, splits, rejected and superseded concepts.
5. [`04-Decisions-Open-Questions-and-ADRs.md`](04-Decisions-Open-Questions-and-ADRs.md) — accepted decisions, unresolved decisions and ADR queue.
6. [`05-Implementation-Evidence-Matrix.md`](05-Implementation-Evidence-Matrix.md) — reported implementation status and verification requirements.
7. [`06-Source-of-Truth-and-Storage-Model.md`](06-Source-of-Truth-and-Storage-Model.md) — roles of Git, Obsidian, Notion, Supabase, ARCH and KAP.
8. [`07-Consolidation-Execution-Roadmap.md`](07-Consolidation-Execution-Roadmap.md) — next source waves, multi-agent workstreams, gates and deliverables.
9. [`08-Canonical-Glossary.md`](08-Canonical-Glossary.md) — normalized terms and status labels.

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
Applications, agents, tools, workflows and embodied systems
```

## Status vocabulary

- **CANON-PROVISIONAL** — strongly supported by repeated internal evidence; pending external verification.
- **IMPLEMENTED-CLAIMED** — implementation was reported but has not yet been verified against artifacts.
- **IMPLEMENTED-VERIFIED** — code/runtime evidence inspected directly.
- **PROPOSED** — explicit architecture proposal not yet canonized.
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

> ART chooses who or what acts, with which agents, tools, APIs, MCPs, runtimes and effectors.

> ARCH preserves evidence. KAP structures validated knowledge. Git preserves durable artifacts and implementation history.

> No major work in a native LLM interface without a measurable functional advantage and a recoverable path through ARCH.

## Next gate

This baseline must now be tested against evidence. The next work is not redesign; it is verification, reconciliation and correction.