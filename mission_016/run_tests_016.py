#!/usr/bin/env python3
"""
MISSION-016 — Test Runner
Runs 3 test compilations: Brahma/MODE-D, Hanuman/MODE-B, Saraswati/MODE-E
Generates all required artifacts.
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timezone

# Add runtime to path
sys.path.insert(0, str(Path(__file__).parent.parent / "runtime"))

from ccr_runtime_v2 import route, RoutingRequest
from session_delta_engine_v1 import SessionDeltaEngine
from living_memory_pipeline_v1 import LivingMemoryPipeline
from context_compiler_v2 import ContextCompilerV2, CompilationRequest
from provider_payload_builder_v1 import ProviderPayloadBuilder
from lakshmi_context_review_v1 import LakshmiContextReviewer

BASE = Path(__file__).parent
PACKS_DIR = BASE / "context_packs"
DELTAS_DIR = BASE / "session_deltas"
PAYLOADS_DIR = BASE / "compiled_payloads"
GOV_DIR = BASE / "governance_reviews"
TRACES_DIR = BASE / "traces"
REPORTS_DIR = BASE / "reports"

for d in [PACKS_DIR, DELTAS_DIR, PAYLOADS_DIR, GOV_DIR, TRACES_DIR, REPORTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

compiler = ContextCompilerV2()
builder = ProviderPayloadBuilder()
reviewer = LakshmiContextReviewer()

results = []

# ─── TEST A: Brahma / architecture / MODE-D ───────────────────────────────────

print("\n=== TEST A: Brahma / architecture → expected MODE-D ===")

routing_a = route(
    mission_id="MISSION-016-A",
    worker="Brahma",
    capability="architecture",
    task_type="strategic",
    governance_risk=30,
    token_budget=8000,
    constitutional_scope=False,
)
print(f"  Mode selected: {routing_a.selected_mode}")
print(f"  Reason: {routing_a.reason[:80]}...")

# Session Delta
delta_engine_a = SessionDeltaEngine(DELTAS_DIR)
delta_a = delta_engine_a.create_delta(
    "MISSION-016-A",
    recent_decisions=["CCR Runtime v2 architecture approved", "MODE-D selected for Brahma"],
    unresolved_questions=["Should CCR v3 support MODE-F for constitutional amendments?"],
    next_actions=["Implement CCR Runtime v2", "Write ADR-0043"],
)
delta_path_a = delta_engine_a.emit_delta(delta_a, "session_delta_MISSION-016-A.md")

# LMP
lmp_a = LivingMemoryPipeline(TRACES_DIR)
lmp_result_a = lmp_a.run(
    mission_id="MISSION-016-A",
    raw_inputs=["CCR Runtime v2 architecture design session"],
    recent_decisions=delta_a.recent_decisions,
    unresolved_questions=delta_a.unresolved_questions,
    next_actions=delta_a.next_actions,
    relevant_adrs=["ADR-0037", "ADR-0043"],
)
lmp_a.emit_trace("lmp_trace_MISSION-016-A.txt")

# Context Compilation
canonical_memory_a = (
    "Y-OS Canonical Memory: CCR Runtime v2 implements MODE-B (Context Pack only), "
    "MODE-D (Context Pack + Canonical Memory), MODE-E (Context Pack + Canonical Memory + Session Delta). "
    "ADR-0037 defines the routing logic. ADR-0043 implements it in code. "
    "Artifact Primacy (Article I) requires all outputs to be artifacts. "
    "Governance Determinism (ADR-0033) requires Lakshmi review for all MODE-D/E packs."
)

req_a = CompilationRequest(
    mission_id="MISSION-016-A",
    worker="Brahma",
    capability="architecture",
    mode=routing_a.selected_mode,
    relevant_adrs=["ADR-0037", "ADR-0038", "ADR-0039", "ADR-0043"],
    relevant_concepts=["CCR_Runtime", "Artifact_Primacy", "Governance_Determinism"],
    relevant_missions=["MISSION-011", "MISSION-012", "MISSION-016"],
    canonical_memory=canonical_memory_a,
    token_budget=routing_a.token_budget,
)
pack_a = compiler.compile(req_a)
(PACKS_DIR / "context_pack_MISSION-016-A.md").write_text(pack_a.to_markdown(), encoding="utf-8")
(PACKS_DIR / "context_pack_MISSION-016-A.json").write_text(pack_a.to_json(), encoding="utf-8")

# Governance
review_a = reviewer.review(pack_a)
(GOV_DIR / "governance_review_MISSION-016-A.md").write_text(review_a.to_markdown(), encoding="utf-8")

# Payloads
payloads_a = builder.build_all(pack_a)
for p in payloads_a:
    (PAYLOADS_DIR / f"payload_MISSION-016-A_{p.provider}.md").write_text(p.to_markdown(), encoding="utf-8")

print(f"  Context Pack: {pack_a.token_estimate} tokens, sources={len(pack_a.source_manifest)}")
print(f"  Governance: {review_a.verdict}, score={review_a.risk_score}, passed={review_a.passed}")
print(f"  Raw session history: {pack_a.raw_session_history_tokens}")

results.append({
    "test": "A",
    "worker": "Brahma",
    "capability": "architecture",
    "expected_mode": "MODE-D",
    "selected_mode": routing_a.selected_mode,
    "mode_correct": routing_a.selected_mode == "MODE-D",
    "token_estimate": pack_a.token_estimate,
    "source_count": len(pack_a.source_manifest),
    "omitted_count": len(pack_a.omitted_context),
    "missing_count": len(pack_a.missing_context),
    "governance_verdict": review_a.verdict,
    "governance_score": review_a.risk_score,
    "governance_passed": review_a.passed,
    "raw_session_history": pack_a.raw_session_history_tokens,
    "lineage_integrity": review_a.lineage_integrity_score,
})


# ─── TEST B: Hanuman / build / MODE-B ─────────────────────────────────────────

print("\n=== TEST B: Hanuman / build → expected MODE-B ===")

routing_b = route(
    mission_id="MISSION-016-B",
    worker="Hanuman",
    capability="build",
    task_type="standard",
    governance_risk=10,
    token_budget=4000,
)
print(f"  Mode selected: {routing_b.selected_mode}")

delta_engine_b = SessionDeltaEngine(DELTAS_DIR)
delta_b = delta_engine_b.create_delta(
    "MISSION-016-B",
    recent_decisions=["Build phase started", "MODE-B selected for Hanuman/build"],
    next_actions=["Execute build tasks", "Deploy to y-os-doctrine"],
)
delta_engine_b.emit_delta(delta_b, "session_delta_MISSION-016-B.md")

lmp_b = LivingMemoryPipeline(TRACES_DIR)
lmp_b.run(
    mission_id="MISSION-016-B",
    raw_inputs=["Build execution session"],
    recent_decisions=delta_b.recent_decisions,
    next_actions=delta_b.next_actions,
    relevant_adrs=["ADR-0043"],
)
lmp_b.emit_trace("lmp_trace_MISSION-016-B.txt")

req_b = CompilationRequest(
    mission_id="MISSION-016-B",
    worker="Hanuman",
    capability="build",
    mode=routing_b.selected_mode,
    relevant_adrs=["ADR-0043"],
    relevant_concepts=["Y_ORC", "Artifact_Primacy"],
    relevant_missions=["MISSION-016"],
    token_budget=routing_b.token_budget,
    # No canonical_memory for MODE-B
)
pack_b = compiler.compile(req_b)
(PACKS_DIR / "context_pack_MISSION-016-B.md").write_text(pack_b.to_markdown(), encoding="utf-8")
(PACKS_DIR / "context_pack_MISSION-016-B.json").write_text(pack_b.to_json(), encoding="utf-8")

review_b = reviewer.review(pack_b)
(GOV_DIR / "governance_review_MISSION-016-B.md").write_text(review_b.to_markdown(), encoding="utf-8")

payloads_b = builder.build_all(pack_b)
for p in payloads_b:
    (PAYLOADS_DIR / f"payload_MISSION-016-B_{p.provider}.md").write_text(p.to_markdown(), encoding="utf-8")

print(f"  Context Pack: {pack_b.token_estimate} tokens, sources={len(pack_b.source_manifest)}")
print(f"  Governance: {review_b.verdict}, score={review_b.risk_score}, passed={review_b.passed}")
print(f"  Raw session history: {pack_b.raw_session_history_tokens}")

results.append({
    "test": "B",
    "worker": "Hanuman",
    "capability": "build",
    "expected_mode": "MODE-B",
    "selected_mode": routing_b.selected_mode,
    "mode_correct": routing_b.selected_mode == "MODE-B",
    "token_estimate": pack_b.token_estimate,
    "source_count": len(pack_b.source_manifest),
    "omitted_count": len(pack_b.omitted_context),
    "missing_count": len(pack_b.missing_context),
    "governance_verdict": review_b.verdict,
    "governance_score": review_b.risk_score,
    "governance_passed": review_b.passed,
    "raw_session_history": pack_b.raw_session_history_tokens,
    "lineage_integrity": review_b.lineage_integrity_score,
})


# ─── TEST C: Saraswati / learning / MODE-E (recent delta present) ─────────────

print("\n=== TEST C: Saraswati / learning / recent_delta → expected MODE-E ===")

routing_c = route(
    mission_id="MISSION-016-C",
    worker="Saraswati",
    capability="learning",
    task_type="complex",
    governance_risk=25,
    token_budget=10000,
    recent_delta_required=True,
)
print(f"  Mode selected: {routing_c.selected_mode}")

delta_engine_c = SessionDeltaEngine(DELTAS_DIR)
delta_c = delta_engine_c.create_delta(
    "MISSION-016-C",
    recent_decisions=["KGC v2 deployed", "39 concept nodes created"],
    unresolved_questions=[
        "Should KGC v3 include body wikilink rewriting?",
        "How to handle concept node versioning?",
        "What is the optimal token budget for MODE-E?",
    ],
    open_loops=["ADR coverage below 80% for mission files", "Excalidraw deferred to MISSION-016"],
    next_actions=["Research KGC v3 requirements", "Synthesize learning from MISSION-013 to 016"],
)
delta_engine_c.emit_delta(delta_c, "session_delta_MISSION-016-C.md")

lmp_c = LivingMemoryPipeline(TRACES_DIR)
lmp_c.run(
    mission_id="MISSION-016-C",
    raw_inputs=["Learning synthesis session — KGC evolution"],
    recent_decisions=delta_c.recent_decisions,
    unresolved_questions=delta_c.unresolved_questions,
    next_actions=delta_c.next_actions,
    relevant_adrs=["ADR-0040", "ADR-0041", "ADR-0042", "ADR-0043"],
)
lmp_c.emit_trace("lmp_trace_MISSION-016-C.txt")

canonical_memory_c = (
    "Y-OS Canonical Memory: KGC v1 (ADR-0040) created 301 files with 565 wikilinks. "
    "KGC v2 (ADR-0042) added 1620 typed edges, 39 concept nodes, 8 Canvas maps, 9 dashboards. "
    "Cognitive Graph Architecture (ADR-0041) defines 12 typed relationships. "
    "CCR Runtime v2 (ADR-0043) implements MODE-B/D/E context routing."
)

session_delta_c = delta_c.to_markdown()

req_c = CompilationRequest(
    mission_id="MISSION-016-C",
    worker="Saraswati",
    capability="learning",
    mode=routing_c.selected_mode,
    relevant_adrs=["ADR-0040", "ADR-0041", "ADR-0042", "ADR-0043"],
    relevant_concepts=["Knowledge_Graph_Compiler", "Cognitive_Graph", "Living_Memory", "Session_Delta"],
    relevant_missions=["MISSION-013", "MISSION-013b", "MISSION-014", "MISSION-015", "MISSION-016"],
    canonical_memory=canonical_memory_c,
    session_delta=session_delta_c,
    token_budget=routing_c.token_budget,
)
pack_c = compiler.compile(req_c)
(PACKS_DIR / "context_pack_MISSION-016-C.md").write_text(pack_c.to_markdown(), encoding="utf-8")
(PACKS_DIR / "context_pack_MISSION-016-C.json").write_text(pack_c.to_json(), encoding="utf-8")

review_c = reviewer.review(pack_c)
(GOV_DIR / "governance_review_MISSION-016-C.md").write_text(review_c.to_markdown(), encoding="utf-8")

payloads_c = builder.build_all(pack_c)
for p in payloads_c:
    (PAYLOADS_DIR / f"payload_MISSION-016-C_{p.provider}.md").write_text(p.to_markdown(), encoding="utf-8")

print(f"  Context Pack: {pack_c.token_estimate} tokens, sources={len(pack_c.source_manifest)}")
print(f"  Governance: {review_c.verdict}, score={review_c.risk_score}, passed={review_c.passed}")
print(f"  Raw session history: {pack_c.raw_session_history_tokens}")

results.append({
    "test": "C",
    "worker": "Saraswati",
    "capability": "learning",
    "expected_mode": "MODE-E",
    "selected_mode": routing_c.selected_mode,
    "mode_correct": routing_c.selected_mode == "MODE-E",
    "token_estimate": pack_c.token_estimate,
    "source_count": len(pack_c.source_manifest),
    "omitted_count": len(pack_c.omitted_context),
    "missing_count": len(pack_c.missing_context),
    "governance_verdict": review_c.verdict,
    "governance_score": review_c.risk_score,
    "governance_passed": review_c.passed,
    "raw_session_history": pack_c.raw_session_history_tokens,
    "lineage_integrity": review_c.lineage_integrity_score,
})


# ─── Save Results JSON ────────────────────────────────────────────────────────

results_path = REPORTS_DIR / "test_results_MISSION-016.json"
results_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

# ─── Summary ─────────────────────────────────────────────────────────────────

print("\n=== SUMMARY ===")
all_modes_correct = all(r["mode_correct"] for r in results)
all_gov_passed = all(r["governance_passed"] for r in results)
total_raw = sum(r["raw_session_history"] for r in results)

print(f"All modes correct: {all_modes_correct}")
print(f"All governance passed: {all_gov_passed}")
print(f"Total raw session history used: {total_raw}")

for r in results:
    mode_ok = "✅" if r["mode_correct"] else "❌"
    gov_ok = "✅" if r["governance_passed"] else "❌"
    print(f"  Test {r['test']}: {r['worker']}/{r['capability']} → {r['selected_mode']} {mode_ok} | "
          f"Gov: {r['governance_verdict']} ({r['governance_score']}) {gov_ok} | "
          f"Tokens: {r['token_estimate']} | Raw: {r['raw_session_history']}")

print(f"\nResults saved: {results_path}")
print("MISSION-016 tests COMPLETE.")
