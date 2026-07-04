# Decision Thread Examples

> Y-OS / KAP Cognitive Architecture
> Gate: DECISION-THREAD-MODEL-GATE
> Status: EXAMPLES ONLY — not real extracted Decision Threads unless explicitly noted as REGISTERED

---

## Example 1 — Architecture Decision Thread (REGISTERED)

**ID:** DT-20260703-YOS1
**Status:** REGISTERED in DECISION-THREAD-REGISTRY.md

```yaml
decision_thread_id: DT-20260703-YOS1
title: YOS contains KAP as module/process
decision_text: "YOS is the global cognitive operating system container. KAP is a module/process inside YOS, not a separate top-level system."
decision_type: architecture
domain: YOS
status: active
decision_status: active_decision
canonical_status: active_control_plane
review_status: approved_for_active_control_plane
current_validity: active
decided_by: user_directive
validated_by: guardian_architect_decision
accepted_option: "YOS as root container, KAP as module"
rejected_options:
  - option: "KAP as top-level system"
    reason: "KAP is a process/engine, not the full cognitive OS"
  - option: "Flat structure with no hierarchy"
    reason: "Does not reflect the actual scope relationship"
rationale: "KAP handles knowledge acquisition and processing. YOS is the broader cognitive OS that includes KAP plus other modules."
confidence_level: high
authority_hint: guardian_architect_decision
```

---

## Example 2 — Source Policy Decision Thread (REGISTERED)

**ID:** DT-20260703-YOS3
**Status:** REGISTERED in DECISION-THREAD-REGISTRY.md

```yaml
decision_thread_id: DT-20260703-YOS3
title: Broad acquisition is blocked until cognitive architecture is validated
decision_text: "No broad acquisition from Notion, Obsidian, ChatGPT, Manus, or other corpora until the cognitive architecture (Source Fragment, Claim, Thought Line, Decision Thread models) is validated."
decision_type: gate_policy
domain: KAP
status: active
decision_status: active_decision
canonical_status: active_control_plane
current_validity: active
accepted_option: "Architecture Before Absorption — validate models first"
rejected_options:
  - option: "Import all sources immediately"
    reason: "Without a validated model, imported data has no structure and cannot be used for synthesis"
  - option: "Import selectively without model"
    reason: "Still creates unstructured accumulation"
rationale: "Core doctrine. Importing without a validated model creates noise, not knowledge."
authority_hint: guardian_architect_decision
```

---

## Example 3 — Workflow Decision Thread (EXAMPLE ONLY)

**Status:** EXAMPLE ONLY — not registered

```yaml
decision_thread_id: DT-EXAMPLE-WF01
title: Session doctrine capture is mandatory before session close
decision_text: "Every session that produces architectural decisions, doctrines, or MPMs must have a capture pack created before the session is closed."
decision_type: workflow
domain: YOS
status: active
decision_status: active_decision
canonical_status: candidate_evidence
current_validity: active
accepted_option: "Mandatory session capture with uncaptured-items backlog"
rejected_options:
  - option: "Capture only when explicitly requested"
    reason: "Creates knowledge gaps between sessions"
  - option: "Capture everything automatically"
    reason: "Not feasible without automation infrastructure"
rationale: "Session knowledge is ephemeral. Without capture, decisions made in one session are lost to future sessions."
authority_hint: guardian_architect_decision
```

---

## Example 4 — Tooling Decision Thread (EXAMPLE ONLY)

**Status:** EXAMPLE ONLY — not registered

```yaml
decision_thread_id: DT-EXAMPLE-TOOL01
title: Obsidian is consultation-only, not canonical source
decision_text: "Obsidian vaults are used for navigation and consultation only. Canonical knowledge lives in Git/Markdown. Obsidian is not the source of truth."
decision_type: tooling
domain: Obsidian
status: active
decision_status: active_decision
canonical_status: candidate_evidence
current_validity: active
accepted_option: "Obsidian = consultation layer; Git = canonical layer"
rejected_options:
  - option: "Obsidian as canonical source"
    reason: "Obsidian is a local app with sync complexity; not durable enough for canonical status"
rationale: "Doctrine YOS-012. Obsidian is powerful for navigation but Git/Markdown provides durability."
authority_hint: guardian_architect_decision
```

---

## Example 5 — Agent Role Decision Thread (EXAMPLE ONLY)

**Status:** EXAMPLE ONLY — not registered

```yaml
decision_thread_id: DT-EXAMPLE-AGENT01
title: Manus is executor, not architectural authority
decision_text: "Manus executes tasks and persists outputs. Manus does not make architectural decisions. Architectural authority belongs to the Guardian Architect (ChatGPT) and the user."
decision_type: agent_role
domain: Agents
status: active
decision_status: active_decision
canonical_status: candidate_evidence
current_validity: active
accepted_option: "Manus = executor; ChatGPT Guardian = architect"
rejected_options:
  - option: "Manus as co-architect"
    reason: "Creates ambiguity about who has final architectural authority"
rationale: "Doctrine YOS-019. Clear role separation prevents conflicting architectural decisions."
authority_hint: guardian_architect_decision
```

---

## Example 6 — Rejected Option Decision Thread (EXAMPLE ONLY)

**Status:** EXAMPLE ONLY — not registered

```yaml
decision_thread_id: DT-EXAMPLE-REJ01
title: Notion canonical merge was rejected as active pipeline
decision_text: "Notion was considered as the canonical knowledge store but was rejected in favor of Git/Markdown."
decision_type: source_policy
domain: Notion
status: rejected
decision_status: rejected_decision
canonical_status: historical_source
current_validity: rejected
accepted_option: "Git/Markdown as canonical store"
rejected_options:
  - option: "Notion as canonical store"
    reason: "Notion has API limits, sync complexity, and is not durable enough for canonical status"
rationale: "Decision DEC-BOOT-009 — Notion is frozen legacy / future migration target."
superseded_by: DT-20260703-YOS2
authority_hint: guardian_architect_decision
```

---

## Example 7 — Superseded Decision Thread (EXAMPLE ONLY)

**Status:** EXAMPLE ONLY — not registered

```yaml
decision_thread_id: DT-EXAMPLE-SUP01
title: KAP was initially conceived as a standalone repo
decision_text: "KAP was initially conceived as a standalone top-level repository, not as a module inside YOS."
decision_type: repo_architecture
domain: KAP
status: superseded
decision_status: superseded_decision
canonical_status: historical_source
current_validity: superseded
superseded_by: DT-20260703-YOS1
rationale: "Initial conception before YOS architecture was defined."
review_notes: "Superseded by DT-20260703-YOS1 — YOS as root container, KAP as module."
authority_hint: guardian_architect_decision
```

---

## Example 8 — Partial Supersession Decision Thread (EXAMPLE ONLY)

**Status:** EXAMPLE ONLY — not registered

```yaml
decision_thread_id: DT-EXAMPLE-PSUP01
title: Notion pipeline was partially superseded by controlled pipeline policy
decision_text: "The original Notion pipeline (ChatGPT2Notion) was partially superseded. The import path is deprecated but the Notion workspace remains as a reference source."
decision_type: pipeline
domain: Notion
status: partially_superseded
decision_status: historical_decision
canonical_status: historical_source
current_validity: partially_superseded
partially_superseded_by: [DT-EXAMPLE-PIPE01]
rationale: "ChatGPT2Notion deprecated (DEC-BOOT-010) but Notion content remains accessible as source."
review_notes: "The active part: Notion as reference source. The superseded part: ChatGPT2Notion as active pipeline."
authority_hint: guardian_architect_decision
```

---

## Example 9 — Implementation Evidence Decision Thread (EXAMPLE ONLY)

**Status:** EXAMPLE ONLY — not registered

```yaml
decision_thread_id: DT-EXAMPLE-IMPL01
title: yos-cognitive-os is the root YOS control plane repository
decision_text: "The repository yj000018/yos-cognitive-os is the root control plane for YOS. All strategic doctrine, registries, and gate reports are persisted here."
decision_type: repo_architecture
domain: YOS
status: active
decision_status: active_decision
canonical_status: implementation_evidence
current_validity: active
implementation_evidence_ids: [SF-005, SF-006]
commit_ids: [3ef6529, 1e29c8c, ff199ef, 63f18a3, b1ffa83]
gate_evidence_ids: [YOS-CONTROL-PLANE-BOOTSTRAP-GATE-REPORT]
accepted_option: "yos-cognitive-os as root YOS repo"
rationale: "REPO-001 decision. Root repo must be at YOS level, not KAP level."
maturity_hint: implementation_evidence
authority_hint: git_commit_evidence
```
