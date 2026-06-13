# CCR Runtime v1.1 — Governance Patch

**Status:** ACCEPTED WITH GOVERNANCE PATCH  
**Supersedes:** CCR Runtime v1 (MISSION-005)  
**Date:** 2026-06-13  
**Mission:** MISSION-005B  
**Patches:** 1-6 (Artifact Primacy, Source Artifact Manifest, Operational Lineage, Human Override, Schema v2.1, Governance Hook)

---

## Patch Summary

| Patch | Title | Resolves |
| :---: | :--- | :--- |
| 1 | Strengthen Artifact Primacy | Lakshmi: Artifact Primacy incomplete |
| 2 | Source Artifact Manifest | Lakshmi: Lineage traceability missing |
| 3 | Operational Lineage Preservation | Lakshmi: Lineage Preservation incomplete |
| 4 | Human Override Protocol | Lakshmi: Human Override undefined |
| 5 | Context Pack Schema v2.1 | Lakshmi: Schema lacks governance fields |
| 6 | Governance Hook v1 | Lakshmi: Hook interface undefined |

---

## Patch 1 — Artifact Primacy (Constitutional Rule)

### Canonical Rule

> **Artifacts are the source of context truth.**

CCR **may**:
- Retrieve artifacts from the Registry
- Traverse lineage graphs
- Select relevant context from artifacts
- Compress context within token budgets
- Generate Context Packs from artifact content

CCR **may NOT**:
- Invent context not present in registered artifacts
- Silently rewrite source artifact meaning
- Treat conversation history as source of truth
- Treat model memory as source of truth
- Treat provider output as canonical unless registered as an artifact

### Enforcement

Every Context Pack must include a **Source Artifact Manifest** (Patch 2).  
Any CCR output that cannot be traced to a registered artifact is a **constitutional violation**.  
Lakshmi must flag any Context Pack with missing source artifact references.

---

## Patch 2 — Source Artifact Manifest

Every Context Pack must include a `source_artifact_manifest` block:

```yaml
source_artifact_manifest:
  source_artifact_ids:
    - "ART-M005-8A4718"
    - "ART-M005-80F9D8"
    - "ART-M005-DCD41E"
  source_artifact_types:
    - "CEO Directive"
    - "Strategy Brief"
    - "Architecture Package"
  source_artifact_versions:
    - "v1"
    - "v1"
    - "v1"
  parent_artifact_id: "ART-M005-DCD41E"
  mission_id: "MISSION-005"
  lineage_depth: 3
  compiler_version: "CCR-v1.1"
  compression_level: "COMPRESSED"
  omitted_context_summary: "Governance Review (ART-M005-F4EA52) omitted — not relevant to build task"
  missing_context_disclosure: "None — all required artifacts present"
```

### Rules

1. `source_artifact_ids` must reference only registered artifacts.
2. `omitted_context_summary` must be explicit — never empty if artifacts were omitted.
3. `missing_context_disclosure` must state "None" explicitly if nothing is missing.
4. `lineage_depth` must match the actual traversal depth used.

---

## Patch 3 — Operational Lineage Preservation

### Canonical Lineage Rules

1. **Every Context Pack is itself an artifact.** It must be registered in the Registry with a unique ID.
2. **Every Context Pack has parent artifacts.** The `parent_artifact_id` field is mandatory.
3. **Every Context Pack records source artifacts.** Via the Source Artifact Manifest (Patch 2).
4. **Every Context Pack records what was omitted.** Via `omitted_context_summary`.
5. **Every output artifact must reference the Context Pack used.** Field: `context_pack_id`.
6. **Context Pack lineage must be visible to Lakshmi.** Via the Governance Hook (Patch 6).

### Updated Architecture Flow

```
Artifacts (Registry)
    ↓
CCR (Retriever → Traverser → Selector → Compressor → Generator)
    ↓
Context Pack Artifact (registered in Registry, with lineage)
    ↓
Worker (receives Context Pack)
    ↓
Output Artifact (references context_pack_id)
    ↓
Registry (updated with lineage: Output → Context Pack → Source Artifacts)
```

### Lineage Integrity Rule

If a Context Pack cannot be traced back to at least one registered artifact, the Context Pack is **invalid** and must not be delivered to a worker.

---

## Patch 4 — Human Override Protocol

### Override Authorities

**CEO may:**
- Force FULL compression level (override CCR token budget)
- Force MINIMAL compression level
- Reject a Context Pack and request recompilation
- Require inclusion of specific artifact IDs
- Suspend CCR execution for a mission

**Lakshmi may:**
- Flag a Context Pack as HIGH_RISK
- Request governance review before execution
- Recommend recompilation with different parameters
- **Block execution** if a constitutional violation is detected

**Brahma may:**
- Require inclusion of specific ADR artifacts
- Require specific lineage depth
- Require architectural artifact coverage

### Override Event Logging

Every human override event must be logged as an artifact:

```yaml
artifact_type: "Human Override Event"
override_authority: "CEO | Lakshmi | Brahma"
override_action: "REJECT_CONTEXT_PACK | FORCE_FULL | BLOCK_EXECUTION | ..."
target_context_pack_id: "CP-XXXX"
reason: "..."
timestamp: "ISO-8601"
```

Override events are immutable. They cannot be deleted or modified.

---

## Patch 5 — Context Pack Schema v2.1

Full Y-OS-native schema replacing v2.0:

```yaml
# Context Pack Schema v2.1 — Y-OS Native
context_pack_id: "CP-{mission_id}-{uuid6}"
schema_version: "2.1"
compiler_version: "CCR-v1.1"
freshness_timestamp: "ISO-8601"

# Identity
mission_id: "MISSION-XXX"
target_worker: "Krishna | Brahma | Ganesha | Hanuman | Lakshmi | Saraswati"
target_capability: "strategy | architecture | plan | build | governance | learning | reporting"
target_provider: "anthropic | openai | gemini | manus_runtime | local"
target_model: "claude-opus-4-5 | gpt-4o | ..."

# Lineage
parent_artifact_id: "ART-XXX"
source_artifact_manifest:
  source_artifact_ids: []
  source_artifact_types: []
  source_artifact_versions: []
  lineage_depth: 0
  omitted_context_summary: ""
  missing_context_disclosure: ""

# Mission Context
mission_objective: ""
current_state: ""
relevant_decisions: []
relevant_adrs: []
relevant_laws: []
relevant_doctrine: []

# Operational State
open_loops: []
active_constraints: []
known_risks: []
missing_context: []

# Worker Instructions
expected_output_artifact: ""
success_criteria: []
output_format: ""

# Compression
token_budget: 2000
compression_level: "FULL | COMPRESSED | MINIMAL"

# Governance
human_override_status: "NONE | CEO_OVERRIDE | LAKSHMI_FLAG | BRAHMA_REQUIREMENT"
lakshmi_risk_score: 0  # 0-100, 0=no risk, 100=block
lakshmi_verdict: "APPROVE | APPROVE_WITH_WARNING | RECOMPILE_REQUIRED | BLOCK_EXECUTION"
```

---

## Patch 6 — Governance Hook v1

### Interface

Lakshmi evaluates every Context Pack before it is delivered to a worker.

**Input:** Context Pack (Schema v2.1)  
**Output:** Context Pack Governance Review

### Evaluation Dimensions

| Dimension | Description | Risk Threshold |
| :--- | :--- | :--- |
| Context Completeness | Are all required artifacts present? | Missing required artifact → HIGH |
| Source Artifact Coverage | Are source artifact IDs valid and registered? | Unregistered source → BLOCK |
| Missing Context Risk | Is missing_context_disclosure complete? | Empty disclosure → MEDIUM |
| Omitted Context Risk | Is omitted_context_summary honest? | Silent omission → HIGH |
| Constitutional Compliance | Does the pack violate any constitutional rule? | Any violation → BLOCK |
| Token Compression Risk | Is compression level appropriate for task? | MINIMAL for complex task → MEDIUM |
| Stale Context Risk | Is freshness_timestamp within acceptable range? | >24h for volatile missions → MEDIUM |
| Lineage Integrity | Can all source artifacts be traced in Registry? | Broken lineage → BLOCK |

### Verdicts

| Verdict | Meaning | Action |
| :--- | :--- | :--- |
| `APPROVE` | No issues detected | Deliver to worker |
| `APPROVE_WITH_WARNING` | Minor risks, acceptable | Deliver with warning logged |
| `RECOMPILE_REQUIRED` | Significant gaps, fixable | Return to CCR for recompilation |
| `BLOCK_EXECUTION` | Constitutional violation | Stop execution, alert CEO |

### Governance Review Artifact

Every Governance Hook evaluation produces a `Context Pack Governance Review` artifact:

```yaml
artifact_type: "Context Pack Governance Review"
context_pack_id: "CP-XXX"
evaluator: "Lakshmi"
timestamp: "ISO-8601"
dimensions_evaluated: 8
risk_scores:
  context_completeness: 0
  source_artifact_coverage: 0
  missing_context_risk: 0
  omitted_context_risk: 0
  constitutional_compliance: 0
  token_compression_risk: 0
  stale_context_risk: 0
  lineage_integrity: 0
overall_risk_score: 0
verdict: "APPROVE"
warnings: []
blocking_reasons: []
```

---

## Governance Compliance Status (Post-Patch)

| Principle | Pre-Patch | Post-Patch |
| :--- | :--- | :--- |
| Artifact Primacy | PARTIAL | ✅ COMPLIANT |
| Capability Independence | COMPLIANT | ✅ COMPLIANT |
| Lineage Preservation | PARTIAL | ✅ COMPLIANT |
| Context Continuity | COMPLIANT | ✅ COMPLIANT |
| Human Override | NON-COMPLIANT | ✅ COMPLIANT |

**All 5 constitutional principles: COMPLIANT.**

---

*Generated by MISSION-005B — CCR Governance Patch*
