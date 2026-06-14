---
id: ADR-SIMP-001
title: Simplicity Guardrail — Y-OS Permanent Constraint
status: ACCEPTED
date: 2026-06-14
deciders: [Brahma, Lakshmi, Ganesha, CEO]
governed_by: [CONSTITUTION/Y-OS_Constitution_v1.md]
tags: [simplicity, guardrail, permanent, constraint, governance]
---

# ADR-SIMP-001 — Simplicity Guardrail

## Context

Y-OS grew from 0 to 71 runtime modules across 19 missions. Each mission added value. But the cumulative effect is an architecture that:

- Only 28% of modules are used daily
- Has 26 canvas maps (3 needed)
- Has 17 dashboards (3 needed)
- Has 14 conceptual layers (5 needed)
- Requires significant cognitive load to navigate

The architecture has drifted from **personal cognitive tool** toward **experimental platform**. This ADR establishes a permanent constraint to prevent recurrence.

## Decision

**Adopt the Simplicity Guardrail as a permanent governance constraint.**

The Guardrail has equal authority to the Constitution for architectural decisions.

## The 5 Permanent Rules

### G1 — Weekly Test (MANDATORY)
Any component not needed weekly is OPTIONAL.  
Any component not needed monthly is an ARCHIVE candidate.

**Enforcement:** Monthly simplicity review. Any module unused for 30 days is flagged.

### G2 — Workload Test (MANDATORY)
Any component that does not reduce human workload is suspect.

**Enforcement:** Before any new module is added, the proposer must answer: *"How does this save time or cognitive effort weekly?"*

### G3 — Boring Infrastructure Preference (RECOMMENDED)
Prefer boring, well-understood infrastructure over clever abstractions.

**Enforcement:** Code review — if a module can be replaced by a dict + 20 lines, it should be.

### G4 — Fewer Modules Preference (MANDATORY)
When two modules do similar things, merge them.  
When a module has one use case, archive it after use.

**Enforcement:** Any new module proposal must include a "why not merge?" justification.

### G5 — No Theoretical Completeness (MANDATORY)
Y-OS is not a research project. Build for what you do, not for what you might do.

**Enforcement:** Any module that has never been used in a real session within 60 days of creation is automatically archived.

## The Complexity Budget

**Maximum active modules: 30**

| Zone | Budget |
|:---|---:|
| Core (5 cognitive modules) | 20 |
| Optional (activated as needed) | 10 |
| **Total active** | **30** |
| Experimental (/experimental/) | unlimited, not active |
| Archived (/archive/) | unlimited, not active |

**Rule:** Adding a module beyond 30 requires archiving one first.

## Consequences

### Positive
- Y-OS remains a daily-use tool, not a maintenance burden
- New contributors can understand the system in < 1 hour
- Cognitive load stays low
- Architecture stays aligned with the original vision

### Negative
- Some experimental capabilities require explicit activation
- Monthly review requires ~30 minutes

### Neutral
- All archived modules are recoverable from Git
- The Constitution remains the supreme governance document

## Governance Review

**Lakshmi — APPROVE**

| Article | Check | Status |
|:---|:---|:---|
| Art. 1 — Artifact Primacy | Guardrail is an artifact, preserved | ✅ |
| Art. 2 — Preservation | No deletion, only archival | ✅ |
| Art. 3 — Derivation Transparency | Rules are explicit and documented | ✅ |
| Art. 4 — Human Override | CEO can override any rule with justification | ✅ |
| Art. 5 — Governance Before Autonomy | ADR approved before enforcement | ✅ |

**Risk Score: 3/100 — APPROVE**

**Ganesha — ADOPT**

This is the most important ADR since the Constitution. Adopt immediately. Enforce monthly.

## Implementation

1. Commit this ADR to y-os-doctrine ✅
2. Execute 30-day simplification roadmap
3. Run monthly simplicity review (first: July 14, 2026)
4. Update complexity budget tracking in Dashboard_Executive_Cockpit.md
