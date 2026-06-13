---
id: yos-adr-0043
title: 'ADR-0043: CCR Runtime v2 Implementation'
type: adr
status: ACCEPTED
date: '2026-06-14'
owner: Brahma
parent: '[[02_ADRs_MOC]]'
mission: MISSION-016
supersedes: '[[ADR-0037]]'
governed_by:
  - '[[Governance_Determinism]]'
  - '[[Lakshmi_Governance]]'
constrained_by:
  - '[[Artifact_Primacy]]'
  - '[[Preservation_Principle]]'
  - '[[Derivation_Transparency]]'
  - '[[Human_Override]]'
  - '[[Governance_Before_Autonomy]]'
produces:
  - '[[ccr_runtime_v2]]'
  - '[[session_delta_engine_v1]]'
  - '[[living_memory_pipeline_v1]]'
  - '[[context_compiler_v2]]'
  - '[[provider_payload_builder_v1]]'
  - '[[lakshmi_context_review_v1]]'
implements:
  - '[[CCR_Runtime]]'
  - '[[Context_Router]]'
  - '[[Living_Memory]]'
  - '[[Session_Delta]]'
depends_on:
  - '[[ADR-0037]]'
  - '[[ADR-0038]]'
  - '[[ADR-0039]]'
  - '[[ADR-0033]]'
tags:
  - '#adr'
  - '#accepted'
  - '#yos'
  - '#runtime'
  - '#ccr'
aliases:
  - ADR-0043
  - CCR Runtime v2
  - Context Router v2
source_branch: y-os-doctrine
canonical: true
---

# ADR-0043: CCR Runtime v2 Implementation

**Status:** ACCEPTED  
**Date:** 2026-06-14  
**Owner:** Brahma  
**Mission:** MISSION-016  
**Supersedes:** ADR-0037 (CCR Runtime v2 design)

---

## Context

ADR-0037 defined the CCR Runtime v2 architecture (MODE-B/D/E context routing).  
ADR-0038 defined the Session Delta Engine.  
ADR-0039 defined the Living Memory Pipeline (8 stages).  
ADR-0033 defined Governance Determinism (Lakshmi review).

MISSION-016 must implement these as executable Python modules and validate them with 3 test compilations.

**Gap before MISSION-016:**  
Y-OS could document and visualize its memory but could not automatically compile and inject context into workers from canonical memory, context packs, session deltas, or the knowledge graph.

---

## Decision

**Implement CCR Runtime v2 as 6 Python modules:**

### Module 1: `ccr_runtime_v2.py` — Context Router

Routes each worker request to the correct context mode:

| Mode | Sources | Default Workers | Trigger |
| :--- | :--- | :--- | :--- |
| **MODE-B** | Context Pack only | Hanuman, Krishna | Standard execution, build, deploy |
| **MODE-D** | Context Pack + Canonical Memory | Brahma, Ganesha, Lakshmi | Architecture, governance, ADR, strategy |
| **MODE-E** | Context Pack + Canonical Memory + Session Delta | Any | recent_delta_required=True + complex task |

**Routing rules (priority order):**
1. MODE-E if `recent_delta_required=True` AND `task_type in (complex, strategic)`
2. MODE-E if `recent_delta_required=True` AND `governance_risk > 55`
3. MODE-D if `constitutional_scope=True`
4. MODE-D if `task_type in (strategic, constitutional, governance)`
5. MODE-D if `capability in MODE_D_CAPABILITIES` (architecture, governance, adr, design...)
6. MODE-D if worker default is D AND capability not in MODE_B_CAPABILITIES
7. MODE-B (default)

**Hard constraint:** Raw session history is NEVER injected. `raw_session_history_tokens` is always 0.

### Module 2: `session_delta_engine_v1.py` — Session Delta Engine

Generates structured deltas with 7 fields:
- `recent_decisions`, `unresolved_questions`, `open_loops`
- `state_changes`, `user_preferences`, `temporary_context`, `next_actions`

Supports: append, compress (merge N deltas), summarize, emit `.md`, emit `.json`.

### Module 3: `living_memory_pipeline_v1.py` — 8-Stage LMP

Each stage creates a Markdown artifact:

| Stage | Input | Output Artifact |
| :--- | :--- | :--- |
| 1. capture | raw_inputs[] | `lmp_capture_*.md` |
| 2. compress | capture | `lmp_compress_*.md` (60-80% reduction) |
| 3. delta | compress | `lmp_delta_*.md` (session_delta) |
| 4. summarize | delta | `lmp_summarize_*.md` (session_summary) |
| 5. archive | summary | `lmp_archive_*.md` (archive_reference) |
| 6. canonicalize | archive | `lmp_canonicalize_*.md` (canonical_memory) |
| 7. compile | canonical | `lmp_compile_*.md` (context_pack) |
| 8. inject | compile | `lmp_inject_*.md` (injection_package) |

### Module 4: `context_compiler_v2.py` — Context Compiler

Compiles a `ContextPack` artifact from:
- Worker identity (built-in)
- Mission context
- Relevant ADRs (title + status snippets)
- Relevant concepts (title snippets)
- Relevant missions (references)
- Canonical Memory (MODE-D/E only)
- Session Delta (MODE-E only)
- Parent artifacts

Output fields: `content`, `source_manifest`, `omitted_context`, `missing_context`, `compression_mode`, `lineage`, `token_estimate`, `raw_session_history_tokens=0`.

### Module 5: `provider_payload_builder_v1.py` — Provider Payload Builder

Converts a Context Pack into provider-ready payloads for:
- **OpenAI** (`gpt-4o` / `gpt-4o-mini` based on worker)
- **Anthropic** (`claude-opus-4-5` / `claude-haiku-3-5` / `claude-sonnet-4-5`)
- **Manus Runtime** (internal format)

Does NOT call providers. Compilation only.

### Module 6: `lakshmi_context_review_v1.py` — Governance Hook

Evaluates every Context Pack against 5 Constitutional Articles:

| Article | Check |
| :--- | :--- |
| I — Artifact Primacy | Source manifest not empty |
| II — Preservation | raw_session_history_tokens = 0 |
| III — Derivation Transparency | Lineage recorded |
| IV — Human Override | Missing context disclosed |
| V — Governance Before Autonomy | MODE-D/E has lineage |

**PASS criteria:** verdict in (APPROVE, APPROVE_WITH_WARNING) AND score ≤ 55 AND blocking = 0.

---

## Test Results

| Test | Worker | Capability | Expected | Selected | Correct | Gov | Score | Raw |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A | Brahma | architecture | MODE-D | **MODE-D** | ✅ | APPROVE | 3 | 0 |
| B | Hanuman | build | MODE-B | **MODE-B** | ✅ | APPROVE | 3 | 0 |
| C | Saraswati | learning | MODE-E | **MODE-E** | ✅ | APPROVE | 3 | 0 |

**All modes correct. All governance passed. Raw session history = 0.**

---

## Consequences

### Positive

- Y-OS can now automatically compile and inject the right context for worker execution
- No raw session history is ever injected (hard constraint enforced in code)
- Context Packs are artifacts (Markdown + JSON) — fully traceable
- Living Memory Pipeline produces 8 artifacts per run
- Lakshmi governance hook validates every Context Pack before injection
- Provider-ready payloads for OpenAI, Anthropic, Manus Runtime

### Negative / Limitations

- Token estimates are rough (4 chars ≈ 1 token) — improve with tiktoken in v3
- Canonical Memory is passed as string — future: load from corpus dynamically
- Provider payloads are not yet executed — MISSION-017 will add live execution
- MODE-F (constitutional amendments) not yet defined

### Risks

- Token budget overflow if canonical memory is very large — mitigated by truncation
- Inferred relationships in KGC v2 may produce incorrect concept links — mitigated by `inferred: true` flag

---

## Governance

**Lakshmi Review:** APPROVE — Risk Score 12/100  
**Ganesha CEO Recommendation:** ADOPT  
**Constitutional Compliance:** All 5 Articles satisfied

---

## Implementation Files

```
runtime/
  ccr_runtime_v2.py
  session_delta_engine_v1.py
  living_memory_pipeline_v1.py
  context_compiler_v2.py
  provider_payload_builder_v1.py
  lakshmi_context_review_v1.py

mission_016/
  run_tests_016.py
  context_packs/         (3 Context Packs × .md + .json)
  session_deltas/        (3 Session Deltas)
  compiled_payloads/     (9 payloads: 3 tests × 3 providers)
  governance_reviews/    (3 Governance Reviews)
  traces/                (LMP traces + artifacts)
  reports/               (test_results_MISSION-016.json)
```

---

## Semantic Links

- **supersedes:** [[ADR-0037]]
- **implements:** [[CCR_Runtime]], [[Context_Router]], [[Living_Memory]], [[Session_Delta]]
- **depends_on:** [[ADR-0037]], [[ADR-0038]], [[ADR-0039]], [[ADR-0033]]
- **governed_by:** [[Governance_Determinism]], [[Lakshmi_Governance]]
- **constrained_by:** [[Artifact_Primacy]], [[Preservation_Principle]], [[Derivation_Transparency]], [[Human_Override]], [[Governance_Before_Autonomy]]
