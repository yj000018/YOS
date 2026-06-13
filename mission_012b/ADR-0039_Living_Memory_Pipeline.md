# ADR-0039 — Living Memory Pipeline

**Status:** Proposed  
**Date:** 2026-06-13  
**Deciders:** Brahma (Architecture), Lakshmi (Governance), Ganesha (CEO)  
**Supersedes:** None  
**Related:** ADR-0036 (Context Architecture), ADR-0037 (CCR Runtime v2), ADR-0038 (Session Delta Engine)

---

## Context

Y-OS has validated across MISSIONS 001–012 that:
- Raw session history degrades execution quality (MISSION-010B: -1.0 quality, MODE-A vs MODE-B)
- Context Packs compiled from artifacts outperform raw history (MISSION-010: Mode E = 91.3)
- Session Delta replaces raw history as the continuity substrate (ADR-0038)
- CCR Runtime v2 compiles governed Context Packs (ADR-0037)

However, the **process connecting** these components — how live conversation becomes canonical organizational memory — has not been formally defined.

---

## Decision

Y-OS adopts the **Living Memory Pipeline (LMP)** as the canonical memory lifecycle doctrine.

The pipeline defines 8 sequential stages:

```
Capture → Compress → Delta → Summarize → Archive → Canonicalize → Compile → Inject
```

This pipeline replaces raw session history as the default continuity mechanism. Raw archives are retained for audit and escalation only.

---

## Rationale

| Alternative | Rejected Because |
| :--- | :--- |
| Raw session history as context | Degrades quality (-1.0), introduces noise, provider-dependent |
| No formal pipeline | Implicit practices are not auditable, not reproducible, not governable |
| Single-stage compression | Loses the distinction between ephemeral delta and canonical memory |
| Provider-native memory | Violates model independence (Constitutional Article I) |

The 8-stage pipeline is the minimum necessary to satisfy:
- Constitutional Article I (Artifact Primacy)
- Constitutional Article III (Derivation Transparency)
- Constitutional Article V (Governance Before Autonomy)

---

## Consequences

### Positive
- Memory lifecycle is explicit, auditable, and reproducible
- Context quality is governed (Lakshmi validates canonicalization)
- Provider independence is preserved (Context Packs are provider-agnostic)
- Cost efficiency: MODE-B (140.9 ROI/1k tokens) is the production default
- Escalation path exists for complex missions (Archive fallback)

### Negative / Risks
- Stage 6 (Canonicalize) adds governance latency for knowledge promotion
- Stage 5 (Archive) requires persistent storage (currently: local filesystem only)
- Implementation of all 8 stages requires CCR Runtime v2 to be fully deployed

### Mitigations
- Stages 1–4 can be implemented incrementally (Delta + Summary first)
- Archive risk is mitigated by GitHub push (pending — MISSION-012A blocker)
- Governance latency is acceptable for doctrine-level knowledge; operational knowledge is promoted via Session Delta without full Lakshmi review

---

## Implementation Phases

| Phase | Stages | Status |
| :--- | :--- | :--- |
| Phase 1 | 1–4 (Capture → Summarize) | Partially implemented (mission runners) |
| Phase 2 | 5 (Archive) | Implemented (Markdown artifacts committed to Git) |
| Phase 3 | 6 (Canonicalize) | Partially implemented (manual ADR promotion) |
| Phase 4 | 7–8 (Compile → Inject) | Implemented (CCR Runtime v1.1 + Context Router) |
| **Full LMP** | All 8 stages automated | **Target: CCR Runtime v2** |

---

## Cross-Links

| Document | Relationship |
| :--- | :--- |
| ADR-0036 Context Architecture | LMP Stage 8 (Inject) uses MODE-B/MODE-D from ADR-0036 |
| ADR-0037 CCR Runtime v2 | LMP Stage 7 (Compile) is implemented by CCR Runtime v2 |
| ADR-0038 Session Delta Engine | LMP Stage 3 (Delta) is implemented by Session Delta Engine |
| Y-OS Constitution Article I | LMP enforces Artifact Primacy at every stage |
| Y-OS Constitution Article IV | LMP preserves Human Override at every stage |

---

## Governance Verdict

**Lakshmi Risk Assessment:**  
- Constitutional compliance: ✅ All 5 Articles respected  
- Risk Score: 12/100 — **APPROVE (Pristine)**  
- No blocking reasons

**CEO Recommendation (Ganesha): ADOPT**
