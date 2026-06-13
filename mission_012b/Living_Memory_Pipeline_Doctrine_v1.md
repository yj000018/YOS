# Living Memory Pipeline Doctrine v1

**Document ID:** LMP-001  
**Version:** 1.0  
**Status:** Proposed → ADR-0039  
**Date:** 2026-06-13  
**Author:** Y-OS Organizational Intelligence (Brahma + Saraswati)

---

## Purpose

This doctrine defines the canonical Y-OS memory lifecycle: how live conversation and execution events are transformed into durable, governed, reusable organizational context.

The Living Memory Pipeline (LMP) replaces raw session history as the default continuity mechanism. Raw archives remain available only as escalation and fallback references.

> **Core Principle:** The goal is not to remember everything in-context. The goal is to transform conversation into governed, compressed, reusable organizational memory.

---

## The Pipeline

```
Live Interaction
      ↓
  1. CAPTURE        ← Raw events, decisions, artifacts, state changes
      ↓
  2. COMPRESS       ← Remove noise, preserve signal
      ↓
  3. DELTA          ← Extract only meaningful changes since last state
      ↓
  4. SUMMARIZE      ← Update rolling session summary
      ↓
  5. ARCHIVE        ← Persist full raw record (Markdown, audit-only)
      ↓
  6. CANONICALIZE   ← Promote validated knowledge to canonical memory
      ↓
  7. COMPILE        ← CCR builds task-specific Context Packs
      ↓
  8. INJECT         ← Context Router delivers pack to target worker/model
      ↓
Governed Execution
```

---

## Stage Definitions

| Stage | Name | Input | Process | Output | Owner |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | **Capture** | Live conversation, tool calls, artifact events, state changes | Record all events as structured entries | Raw Event Stream | Y-ORC / Session Logger |
| 2 | **Compress** | Raw Event Stream | Remove duplicates, filler, retries, noise. Preserve decisions, artifacts, errors, outcomes | Compressed Event Log | CCR |
| 3 | **Delta** | Compressed Event Log + Previous State | Extract only changes since last checkpoint | Session Delta (YAML) | Session Delta Engine |
| 4 | **Summarize** | Session Delta | Continuously update rolling summary: what happened, what was decided, what is pending | Rolling Summary | CCR / Saraswati |
| 5 | **Archive** | Full raw record | Write complete Markdown artifact to persistent storage | Archive Artifact (`.md`) | Artifact Writer |
| 6 | **Canonicalize** | Rolling Summary + Archive | Promote validated, stable knowledge to canonical memory: Constitution, ADRs, Registry, doctrine | Canonical Memory Update | Governance (Lakshmi) |
| 7 | **Compile** | Canonical Memory + Session Delta + Artifact Lineage + Mission State | CCR builds a task-scoped, compressed, governed Context Pack | Context Pack (YAML + MD) | CCR Runtime v2 |
| 8 | **Inject** | Context Pack + Target Worker/Model | Context Router selects MODE-B or MODE-D, injects pack into execution context | Governed Execution Context | Context Router |

---

## Runtime Flow

### Standard Execution (MODE-B — Production Default)

```
Session Events
    → Capture → Compress → Delta → Summarize
                                        ↓
                              Archive (background)
                                        ↓
                              Canonicalize (if validated)
                                        ↓
                              CCR Compile (Context Pack)
                                        ↓
                              Context Router → MODE-B
                                        ↓
                              Worker Execution
```

### Constitutional/Governance Work (MODE-D)

```
Same pipeline as above, PLUS:
    → Canonical Memory (Constitution + ADRs + Registry)
    → Injected alongside Context Pack
    → Context Router → MODE-D
```

### Escalation / Fallback

```
If Context Pack is insufficient:
    → Context Router escalates to Archive
    → Raw Markdown archive injected (one-time, flagged)
    → Lakshmi notified
    → Escalation logged in execution trace
```

---

## Governance Rules

### G1 — Archive is not default context
Raw archives are never injected by default. They are accessible only via explicit escalation request from a worker or operator.

### G2 — Canonicalization requires governance approval
Promotion from Rolling Summary to Canonical Memory requires Lakshmi validation (Risk Score ≤ 55, Verdict ∈ {APPROVE, APPROVE_WITH_WARNING}).

### G3 — Context Packs are artifacts
Every Context Pack produced by CCR is registered as an artifact in the Registry with full lineage (source_artifact_ids, compiler_version, compression_level).

### G4 — Session Delta is ephemeral
Session Deltas are scoped to a single mission. They are purged after Archive is written and Canonicalization is complete.

### G5 — Inject is observable
Every injection event is logged in the execution trace with: context_pack_id, mode, worker, timestamp, token_count.

### G6 — Human Override at every stage
A human operator may halt the pipeline at any stage, override a compression decision, or force escalation to archive. This right is non-removable (Constitutional Article IV).

---

## What This Pipeline Replaces

| Old Approach | New Approach | Reason |
| :--- | :--- | :--- |
| Raw session history injected | Session Delta (YAML) | History introduces noise (MISSION-010B: -1.0 quality) |
| Conversation as memory | Artifacts as memory | Constitutional Article I: Artifact Primacy |
| Ad-hoc context selection | CCR Compile (governed) | Reproducibility, auditability |
| Provider-specific memory | Provider-independent Context Packs | Constitutional Article I + model independence |
| Infinite context window | Compressed, scoped Context Pack | Cost efficiency (MISSION-010B: MODE-B = 140.9 ROI/1k) |

---

## Relationship to Existing Architecture

```
Constitution (Article I — Artifact Primacy)
    ↓
Living Memory Pipeline Doctrine (this document)
    ↓
Session Delta Engine v1 (ADR-0038)
    ↓
CCR Runtime v2 (ADR-0037)
    ↓
Context Architecture (ADR-0036)
    ↓
Context Pack Standard v2.1 (CCR v1.1 — ADR-0030)
```

The LMP is the **process layer** that connects the Session Delta Engine (ADR-0038) to the CCR Runtime (ADR-0037) and the Context Architecture (ADR-0036).

---

## Final Validation Question

> **Can this pipeline define the canonical Y-OS memory lifecycle from live interaction to runtime context injection?**

**YES.**

The 8-stage pipeline covers the complete lifecycle:
- **Capture → Compress → Delta → Summarize** = live-to-structured transformation
- **Archive** = durability and audit compliance
- **Canonicalize** = knowledge promotion with governance gate
- **Compile** = task-scoped, governed context assembly
- **Inject** = governed delivery to execution layer

Every stage has a defined owner, input, output, and governance rule. The pipeline is observable, interruptible, and constitutionally compliant.

---

## CEO Recommendation (Ganesha)

**ADOPT.**

The Living Memory Pipeline Doctrine formalizes what Y-OS has been doing empirically across MISSIONS 001–012. It transforms an implicit practice into an explicit, governed, auditable process. This is the missing connective tissue between the Session Delta Engine (ADR-0038) and the CCR Runtime (ADR-0037).

**Immediate actions:**
1. Register as ADR-0039
2. Cross-link with ADR-0036, ADR-0037, ADR-0038
3. Add Stage 6 (Canonicalize) governance check to all future mission runners
4. Update CCR Runtime v2 implementation spec to include explicit pipeline stage logging
