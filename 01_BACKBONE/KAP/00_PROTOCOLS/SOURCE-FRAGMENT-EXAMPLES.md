# Source Fragment Examples

> Y-OS / KAP Cognitive Architecture
> Gate: SOURCE-FRAGMENT-MODEL-GATE
> Status: ILLUSTRATIVE — examples are representative, not real source data unless explicitly noted

---

## Example 1 — ChatGPT Session Capture Pack

```json
{
  "fragment_id": "FRAG-20260703-CP01",
  "fragment_title": "CURRENT-CHATGPT-YOS-KAP-SESSION-CAPTURE (2026-07-03)",
  "source_system": "ChatGPT",
  "source_type": "session_capture_pack",
  "source_subtype": "manual_export",
  "source_path_or_url": "00_Control_Plane/Session_Captures/CURRENT-CHATGPT-YOS-KAP-SESSION-CAPTURE.md",
  "source_repo": "yj000018/yos-cognitive-os",
  "source_branch": "main",
  "source_commit": "1e29c8c",
  "source_created_at": "2026-07-03T00:00:00Z",
  "source_observed_at": "2026-07-03T01:00:00Z",
  "extracted_at": "2026-07-03T01:30:00Z",
  "captured_by": "Manus",
  "capture_method": "manual_upload_then_git_persist",
  "content_boundary": "full",
  "language": "en",
  "project_scope": "KAP",
  "domain_tags": ["doctrine", "architecture", "kap", "yos", "session_capture"],
  "candidate_thought_lines": ["TL-ARCHITECTURE-BEFORE-ABSORPTION", "TL-GIT-AS-CANON"],
  "candidate_claims": [],
  "candidate_decisions": ["DEC-CGPT-001", "DEC-CGPT-002"],
  "candidate_impasses": [],
  "maturity_hint": "validated_gate_output",
  "authority_hint": "guardian_architect_decision",
  "provenance_confidence": "high",
  "sensitivity_level": "internal",
  "canonical_status": "active_control_plane",
  "review_status": "metadata_reviewed",
  "merge_status": "not_merged",
  "supersession_status": "active",
  "related_fragments": ["FRAG-20260702-CP02"],
  "notes": "Persisted verbatim. Doctrines and decisions extracted. 11 MPM stubs created."
}
```

---

## Example 2 — Manus Gate Report

```json
{
  "fragment_id": "FRAG-20260703-GR01",
  "fragment_title": "EVOLUTIONARY-KNOWLEDGE-MERGE-ARCHITECTURE-GATE-REPORT",
  "source_system": "Manus",
  "source_type": "gate_report",
  "source_path_or_url": "06_Reports/Gates/EVOLUTIONARY-KNOWLEDGE-MERGE-ARCHITECTURE-GATE-REPORT.md",
  "source_repo": "yj000018/KAP",
  "source_branch": "main",
  "source_commit": "0d9a72f",
  "source_created_at": "2026-07-03T00:00:00Z",
  "source_observed_at": "2026-07-03T00:30:00Z",
  "extracted_at": "2026-07-03T00:30:00Z",
  "captured_by": "Manus",
  "capture_method": "git_commit",
  "content_boundary": "full",
  "language": "en",
  "project_scope": "KAP",
  "domain_tags": ["architecture", "gate", "knowledge_merge", "thought_lines"],
  "candidate_thought_lines": ["TL-ARCHITECTURE-BEFORE-ABSORPTION"],
  "maturity_hint": "validated_gate_output",
  "authority_hint": "manus_execution_report",
  "provenance_confidence": "high",
  "sensitivity_level": "internal",
  "canonical_status": "active_control_plane",
  "review_status": "metadata_reviewed",
  "merge_status": "not_merged",
  "supersession_status": "active",
  "related_fragments": [],
  "notes": "Gate PASS. 4 registries created (28 TLs, 14 DTs, 12 impasses, 28 synthesis areas)."
}
```

---

## Example 3 — Notion Page (illustrative — not yet extracted)

```json
{
  "fragment_id": "FRAG-XXXXXXXX-NOT1",
  "fragment_title": "YOS Architecture Overview (Notion page — ILLUSTRATIVE)",
  "source_system": "Notion",
  "source_type": "notion_page",
  "source_path_or_url": "https://www.notion.so/[page-id]",
  "source_observed_at": "UNKNOWN",
  "captured_by": "PENDING",
  "capture_method": "notion_api_pending",
  "content_boundary": "metadata_only",
  "language": "fr",
  "project_scope": "YOS",
  "domain_tags": ["architecture", "notion"],
  "maturity_hint": "unknown",
  "authority_hint": "source_document",
  "provenance_confidence": "medium",
  "sensitivity_level": "internal",
  "canonical_status": "requires_review",
  "review_status": "unreviewed",
  "merge_status": "not_merged",
  "supersession_status": "unknown",
  "notes": "ILLUSTRATIVE EXAMPLE. Real Notion extraction requires NOTION-PIPELINE-CONTROLLED-EXECUTION-GATE."
}
```

---

## Example 4 — Obsidian Note (illustrative — not yet extracted)

```json
{
  "fragment_id": "FRAG-XXXXXXXX-OBS1",
  "fragment_title": "KAP Architecture Note (Obsidian — ILLUSTRATIVE)",
  "source_system": "Obsidian",
  "source_type": "obsidian_note",
  "source_path_or_url": "/Vault-YOS/KAP/architecture-notes.md",
  "source_observed_at": "UNKNOWN",
  "captured_by": "PENDING",
  "capture_method": "obsidian_pipeline_pending",
  "content_boundary": "metadata_only",
  "language": "fr",
  "project_scope": "KAP",
  "domain_tags": ["obsidian", "architecture"],
  "maturity_hint": "rough_note",
  "authority_hint": "source_document",
  "provenance_confidence": "medium",
  "sensitivity_level": "internal",
  "canonical_status": "requires_review",
  "review_status": "unreviewed",
  "merge_status": "not_merged",
  "supersession_status": "unknown",
  "notes": "ILLUSTRATIVE EXAMPLE. Real extraction requires OBSIDIAN-PIPELINE-PATCH-GATE."
}
```

---

## Example 5 — Git Commit

```json
{
  "fragment_id": "FRAG-20260703-GC01",
  "fragment_title": "KAP-ARCH-1: Workflow, Pipeline & Protocol Consolidation",
  "source_system": "Git",
  "source_type": "git_commit",
  "source_path_or_url": "https://github.com/yj000018/KAP/commit/2650c8a",
  "source_repo": "yj000018/KAP",
  "source_branch": "main",
  "source_commit": "2650c8a",
  "source_created_at": "2026-07-02T00:00:00Z",
  "source_observed_at": "2026-07-03T00:00:00Z",
  "captured_by": "Manus",
  "capture_method": "git_log",
  "content_boundary": "metadata_only",
  "language": "en",
  "project_scope": "KAP",
  "domain_tags": ["git", "architecture", "pipeline", "workflow"],
  "maturity_hint": "implementation_evidence",
  "authority_hint": "git_commit_evidence",
  "provenance_confidence": "high",
  "sensitivity_level": "public",
  "canonical_status": "historical_source",
  "review_status": "metadata_reviewed",
  "merge_status": "not_merged",
  "supersession_status": "active",
  "notes": "12 files, 20 protocols, 16 pipelines, 25 connectors."
}
```

---

## Example 6 — MPM Document

```json
{
  "fragment_id": "FRAG-20260703-MPM1",
  "fragment_title": "MPM-CONNECTOR-DESIGN-GATE (stub)",
  "source_system": "Manus",
  "source_type": "mpm",
  "source_path_or_url": "03_Modules/KAP/Gates/CONNECTOR-DESIGN-GATE/MPM-CONNECTOR-DESIGN-GATE.md",
  "source_repo": "yj000018/yos-cognitive-os",
  "source_branch": "main",
  "source_commit": "1e29c8c",
  "source_created_at": "2026-07-03T01:30:00Z",
  "source_observed_at": "2026-07-03T01:30:00Z",
  "captured_by": "Manus",
  "capture_method": "stub_from_capture_pack",
  "content_boundary": "metadata_only",
  "language": "en",
  "project_scope": "KAP",
  "domain_tags": ["mpm", "connector", "gate"],
  "maturity_hint": "proposal",
  "authority_hint": "guardian_architect_decision",
  "provenance_confidence": "medium",
  "sensitivity_level": "internal",
  "canonical_status": "candidate_evidence",
  "review_status": "unreviewed",
  "merge_status": "not_merged",
  "supersession_status": "unknown",
  "notes": "STUB — full body missing. Recover from ChatGPT parallel session."
}
```

---

## Example 7 — Architecture Decision Record

```json
{
  "fragment_id": "FRAG-20260703-ADR1",
  "fragment_title": "YOS-REPOSITORY-ARCHITECTURE-DECISION",
  "source_system": "Git",
  "source_type": "architecture_doc",
  "source_path_or_url": "02_Architecture/Decisions/YOS-REPOSITORY-ARCHITECTURE-DECISION.md",
  "source_repo": "yj000018/yos-cognitive-os",
  "source_branch": "main",
  "source_commit": "3ef6529",
  "source_created_at": "2026-07-03T00:00:00Z",
  "source_observed_at": "2026-07-03T00:00:00Z",
  "captured_by": "Manus",
  "capture_method": "git_commit",
  "content_boundary": "full",
  "language": "en",
  "project_scope": "YOS",
  "domain_tags": ["architecture", "decision", "repository"],
  "maturity_hint": "validated_gate_output",
  "authority_hint": "guardian_architect_decision",
  "provenance_confidence": "high",
  "sensitivity_level": "internal",
  "canonical_status": "active_control_plane",
  "review_status": "metadata_reviewed",
  "merge_status": "not_merged",
  "supersession_status": "active",
  "notes": "Master repo + linked/submodule repos architecture decision."
}
```

---

## Example 8 — Memory Item (Mem0)

```json
{
  "fragment_id": "FRAG-20260703-MEM1",
  "fragment_title": "Mem0 memory item — KAP architecture doctrine (ILLUSTRATIVE)",
  "source_system": "Mem0",
  "source_type": "memory_item",
  "source_path_or_url": "mem0://user/yannick/[memory-id]",
  "source_observed_at": "2026-07-03T00:00:00Z",
  "captured_by": "Manus",
  "capture_method": "mem0_api",
  "content_boundary": "snippet",
  "language": "en",
  "project_scope": "YOS",
  "domain_tags": ["mem0", "doctrine", "architecture"],
  "maturity_hint": "raw",
  "authority_hint": "memory_hint",
  "provenance_confidence": "medium",
  "sensitivity_level": "internal",
  "canonical_status": "candidate_evidence",
  "review_status": "unreviewed",
  "merge_status": "not_merged",
  "supersession_status": "unknown",
  "notes": "ILLUSTRATIVE. Mem0 is ACQUIRED. Derivative source — use as routing aid, not primary evidence."
}
```
