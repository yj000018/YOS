# Continuity Enforcement Protocol

This protocol defines the automatic enforcement rules for the yOS Continuity Core.

## 1. Boundary Enforcement
If work crosses an LLM, tool, agent, session, mission, or phase boundary, a Context Pack is **required**.
* **If missing:** `enforcement_level = blocking`

## 2. Canonical Memory Enforcement
If a task is governance-heavy, architecture-level, full-project recovery, canonical, constitutional, or a Founder/Chief Architect gate:
* `canonical_memory_mode` must be `required` or `auto_if_high_risk`.
* **If absent:** `enforcement_level = warning` or `blocking` (depending on risk).

## 3. Session Drift Enforcement
If a session grows too long, the topic pivots, the sub-theme shifts, or the contradiction risk increases:
* Manus must suggest session rotation or a Context Pack refresh.
* User confirmation may be required depending on matrix policy.

## 4. `previous_response_id` Enforcement
`previous_response_id` may be used **only** when:
* `session_continuity_mode` allows it.
* The task is bounded.
* No canonical memory dependency is being replaced by it.
* No handoff boundary requires a Context Pack instead.

**If used, log:**
* `previous_response_id_used: true`
* purpose
* expected scope
* reset condition

## 5. Source Artifact Manifest Enforcement
Every governed Context Pack must include a `source_artifact_manifest`.
* **If missing for governed or gate-critical work:** `hard_stop`.

## 6. Output Lineage Enforcement
Every output artifact produced from a Context Pack must reference:
* `context_pack_id`
* source artifacts (where applicable)
* `mission_id`
* execution mode
* model/tool used

* **If missing for gate-critical work:** `blocking` or `hard_stop`.

## 7. Silent Fallback Enforcement
**No silent fallback.** Any model, tool, or context mode fallback must log:
* requested mode
* executed mode
* reason
* authority
* validation status

## 8. QC Debt Enforcement
* Legacy missing metadata may be QC debt.
* Gate-critical missing metadata is a `blocker`.
* New output missing mandatory metadata is an `error`.
* Promoted unverified output is a `hard_stop`.

## 9. Constraint Acknowledgment Protocol (CAP) Enforcement
As a rule of handoff validation, the receiving LLM must declaratively acknowledge the active constraints.
* **If acknowledgment is missing or incomplete:** `enforcement_level = blocking`.

## 10. Integrity and Staleness Enforcement
* **Checksum Verification:** The `pack_checksum` must be verified by the runtime or script. This verification is authoritative.
* **Staleness:** Pack age is evaluated against the `staleness_policy` defined for the specific `task_class`. If the maximum age is exceeded, the corresponding `staleness_action` (`advisory`, `warning`, `blocking`, or `hard_stop`) is enforced.
