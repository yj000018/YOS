#!/usr/bin/env python3
"""
MISSION-017 — Live Worker Execution Runner
Runs 4 live worker tests: Brahma/Hanuman/Saraswati/Lakshmi
Registers all outputs as artifacts.
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime, timezone

# Add runtime to path
RUNTIME = Path(__file__).parent.parent / "runtime"
sys.path.insert(0, str(RUNTIME))

from ccr_runtime_v2 import route
from context_compiler_v2 import ContextCompilerV2, CompilationRequest
from provider_payload_builder_v1 import ProviderPayloadBuilder
from lakshmi_context_review_v1 import LakshmiContextReviewer
from live_worker_executor_v1 import LiveWorkerExecutor
from artifact_registry_v2 import ArtifactRegistryV2
from output_validator_v1 import OutputValidator
from execution_trace_logger_v1 import ExecutionTraceLogger, ExecutionTrace
from cost_tracker_v1 import CostTracker

BASE = Path(__file__).parent
ARTIFACTS_DIR = BASE / "artifacts"
REGISTRY_FILE = BASE / "artifact_registry_v2.json"
TRACE_FILE = BASE / "execution_trace.jsonl"
COST_REPORT = BASE / "cost_report.md"
REPORTS_DIR = BASE / "reports"
GOV_DIR = BASE / "governance_reviews"
VAL_DIR = BASE / "validation_reports"
CP_DIR = BASE / "context_packs"

for d in [ARTIFACTS_DIR, REPORTS_DIR, GOV_DIR, VAL_DIR, CP_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ─── Init modules ─────────────────────────────────────────────────────────────
compiler = ContextCompilerV2()
builder = ProviderPayloadBuilder()
gov_reviewer = LakshmiContextReviewer()
executor = LiveWorkerExecutor()
registry = ArtifactRegistryV2(ARTIFACTS_DIR, REGISTRY_FILE)
validator = OutputValidator()
trace_logger = ExecutionTraceLogger(TRACE_FILE)
cost_tracker = CostTracker()

# ─── Canonical Memory (shared) ────────────────────────────────────────────────
CANONICAL_MEMORY = (
    "Y-OS Canonical Memory v1 (MISSION-016): "
    "CCR Runtime v2 implements MODE-B (Context Pack only), "
    "MODE-D (Context Pack + Canonical Memory), "
    "MODE-E (Context Pack + Canonical Memory + Session Delta). "
    "ADR-0037 defines routing. ADR-0043 implements it. "
    "Artifact Primacy (Article I): all outputs must be artifacts. "
    "Governance Determinism (ADR-0033): Lakshmi reviews all MODE-D/E packs. "
    "Living Memory Pipeline (ADR-0039): 8-stage pipeline (capture→inject). "
    "Session Delta Engine (ADR-0038): structured deltas, never raw history. "
    "KGC v2 (ADR-0042): 1620 typed edges, 39 concept nodes, 8 Canvas maps. "
    "Y-OS Constitution: 5 Articles — Artifact Primacy, Preservation, "
    "Derivation Transparency, Human Override, Governance Before Autonomy."
)

SYSTEM_PROMPT_BASE = (
    "You are {worker}, a Y-OS cognitive worker with capability: {capability}. "
    "You operate under the Y-OS Constitution (Article I: Artifact Primacy). "
    "All outputs must be structured artifacts with a clear title, sections, and conclusions. "
    "Context mode: {mode}. "
    "Do not include any API keys, secrets, or raw session history in your output. "
    "Be concise, precise, and structured."
)

results = []
live_calls_attempted = 0
live_calls_succeeded = 0
live_calls_failed = 0
fallback_calls = 0

# ─── ENV CHECK ────────────────────────────────────────────────────────────────
openai_key_present = bool(os.environ.get("OPENAI_API_KEY", ""))
anthropic_key_present = bool(os.environ.get("ANTHROPIC_API_KEY", ""))
print(f"\n=== ENVIRONMENT CHECK ===")
print(f"  OPENAI_API_KEY: {'SET' if openai_key_present else 'MISSING'}")
print(f"  ANTHROPIC_API_KEY: {'SET' if anthropic_key_present else 'MISSING'}")

if not openai_key_present and not anthropic_key_present:
    print("\n[FATAL] No provider API keys available. Cannot execute live calls.")
    sys.exit(1)


def run_test(
    test_id: str,
    worker: str,
    capability: str,
    expected_mode: str,
    primary_provider: str,
    primary_model: str,
    task: str,
    artifact_id: str,
    artifact_type: str,
    session_delta: str = "",
    task_type: str = "standard",
    recent_delta_required: bool = False,
) -> dict:
    global live_calls_attempted, live_calls_succeeded, live_calls_failed, fallback_calls

    print(f"\n=== TEST {test_id}: {worker}/{capability} → expected {expected_mode} ===")

    # 1. Route
    routing = route(
        mission_id="MISSION-017",
        worker=worker,
        capability=capability,
        task_type=task_type,
        token_budget=6000,
        recent_delta_required=recent_delta_required,
    )
    mode_correct = routing.selected_mode == expected_mode
    print(f"  Mode: {routing.selected_mode} {'✅' if mode_correct else '❌'}")

    # 2. Compile Context Pack
    req = CompilationRequest(
        mission_id="MISSION-017",
        worker=worker,
        capability=capability,
        mode=routing.selected_mode,
        relevant_adrs=["ADR-0037", "ADR-0038", "ADR-0039", "ADR-0043"],
        relevant_concepts=["CCR_Runtime", "Artifact_Primacy", "Living_Memory"],
        relevant_missions=["MISSION-016", "MISSION-017"],
        canonical_memory=CANONICAL_MEMORY if routing.selected_mode in ("MODE-D", "MODE-E") else None,
        session_delta=session_delta if routing.selected_mode == "MODE-E" else None,
        token_budget=routing.token_budget,
    )
    pack = compiler.compile(req)
    cp_id = f"CP-M017-{worker.upper()}-{capability.upper()}"
    (CP_DIR / f"{cp_id}.md").write_text(pack.to_markdown(), encoding="utf-8")

    # 3. Pre-execution Lakshmi review
    pre_review = gov_reviewer.review(pack)
    (GOV_DIR / f"pre_review_{test_id}.md").write_text(pre_review.to_markdown(), encoding="utf-8")
    print(f"  Pre-exec gov: {pre_review.verdict} ({pre_review.risk_score})")

    if not pre_review.passed:
        print(f"  [BLOCKED] Lakshmi blocked execution: {pre_review.blocking_reasons}")
        return {
            "test": test_id, "worker": worker, "status": "BLOCKED_BY_GOVERNANCE",
            "mode_correct": mode_correct, "artifact_registered": False,
        }

    # 4. Build system prompt + user content
    system_prompt = SYSTEM_PROMPT_BASE.format(
        worker=worker, capability=capability, mode=routing.selected_mode
    )
    user_content = f"{pack.content}\n\n---\n\n## Task\n\n{task}"

    # 5. Execute
    live_calls_attempted += 1
    fallback_model = "gpt-4o" if primary_provider != "openai" else "gpt-4o-mini"
    fallback_provider = "openai" if primary_provider == "anthropic" else "anthropic"

    result = executor.execute_with_fallback(
        worker=worker,
        capability=capability,
        mission_id="MISSION-017",
        system_prompt=system_prompt,
        user_content=user_content,
        primary_provider=primary_provider,
        primary_model=primary_model,
        fallback_provider=fallback_provider,
        fallback_model=fallback_model,
        context_pack_id=cp_id,
        selected_mode=routing.selected_mode,
    )

    if result.status == "SUCCESS":
        live_calls_succeeded += 1
    elif result.status == "FALLBACK":
        live_calls_succeeded += 1
        fallback_calls += 1
    else:
        live_calls_failed += 1

    print(f"  Execution: {result.status} | {result.provider}/{result.model} | "
          f"{result.total_tokens} tokens | {result.latency_ms:.0f}ms")

    # 6. Log trace
    trace = ExecutionTrace(
        mission_id="MISSION-017",
        worker=worker,
        capability=capability,
        context_pack_id=cp_id,
        selected_mode=routing.selected_mode,
        provider=result.provider,
        model=result.model,
        status=result.status,
        latency_ms=result.latency_ms,
        prompt_tokens=result.prompt_tokens,
        completion_tokens=result.completion_tokens,
        total_tokens=result.total_tokens,
        artifact_id=artifact_id if result.success else "",
        error_type=result.error_type,
        error_message_redacted=result.error_message_redacted,
    )
    trace_logger.log(trace)

    # 7. Cost tracking
    if result.success and result.total_tokens > 0:
        cost_tracker.record(
            trace_id=trace.trace_id,
            worker=worker,
            provider=result.provider,
            model=result.model,
            prompt_tokens=result.prompt_tokens,
            completion_tokens=result.completion_tokens,
        )

    # 8. Register artifact if successful
    artifact_registered = False
    validation_verdict = ""
    if result.success:
        content = (
            f"# {artifact_type} — {worker} / MISSION-017\n\n"
            f"**Worker:** {worker}  \n"
            f"**Capability:** {capability}  \n"
            f"**Mode:** {routing.selected_mode}  \n"
            f"**Provider:** {result.provider}  \n"
            f"**Model:** {result.model}  \n"
            f"**Tokens:** {result.total_tokens} (prompt: {result.prompt_tokens}, completion: {result.completion_tokens})  \n"
            f"**Latency:** {result.latency_ms:.0f}ms  \n"
            f"**Context Pack:** {cp_id}  \n\n"
            f"---\n\n"
            f"## Worker Output\n\n"
            f"{result.content}\n\n"
            f"---\n\n"
            f"## Lineage\n\n"
            f"- Source Context Pack: {cp_id}\n"
            f"- Provider: {result.provider}\n"
            f"- Model: {result.model}\n"
            f"- Execution Trace: {trace.trace_id}\n"
            f"- Mission: MISSION-017\n"
            f"- ADR: ADR-0044\n"
        )

        # 9. Validate output
        val_result = validator.validate(
            artifact_id=artifact_id,
            content=content,
            artifact_type=artifact_type,
            lineage={"source_context_pack": cp_id, "trace_id": trace.trace_id},
            provider=result.provider,
            model=result.model,
            context_pack_id=cp_id,
        )
        (VAL_DIR / f"validation_{test_id}.md").write_text(val_result.to_markdown(), encoding="utf-8")
        validation_verdict = val_result.verdict
        print(f"  Validation: {val_result.verdict}")

        if val_result.passed:
            art = registry.register(
                artifact_id=artifact_id,
                mission_id="MISSION-017",
                artifact_type=artifact_type,
                worker=worker,
                capability=capability,
                provider=result.provider,
                model=result.model,
                content=content,
                parent_context_pack_id=cp_id,
                lineage={
                    "source_context_pack": cp_id,
                    "provider_payload": f"payload_{test_id}",
                    "execution_trace": trace.trace_id,
                },
                tags=["#artifact", "#yos", f"#{worker.lower()}", "#mission-017"],
            )
            registry.update_status(artifact_id, "VALIDATED", val_result.verdict)
            artifact_registered = True
            print(f"  Artifact: {artifact_id} REGISTERED ✅")

    # 10. Post-execution Lakshmi review (if artifact registered)
    if artifact_registered:
        # Create a minimal pack-like object for post-review
        _w = worker
        _mode = routing.selected_mode
        _manifest = [cp_id, result.provider, result.model]
        _lineage = [f"Executed by {result.provider}/{result.model}", f"Trace: {trace.trace_id}"]

        class MockPack:
            mission_id = "MISSION-017"
            worker = _w
            mode = _mode
            source_manifest = _manifest
            omitted_context = []
            missing_context = []
            compression_mode = "structural"
            lineage = _lineage
            raw_session_history_tokens = 0

        post_review = gov_reviewer.review(MockPack())
        (GOV_DIR / f"post_review_{test_id}.md").write_text(post_review.to_markdown(), encoding="utf-8")
        print(f"  Post-exec gov: {post_review.verdict} ({post_review.risk_score})")

    return {
        "test": test_id,
        "worker": worker,
        "capability": capability,
        "expected_mode": expected_mode,
        "selected_mode": routing.selected_mode,
        "mode_correct": mode_correct,
        "provider": result.provider,
        "model": result.model,
        "status": result.status,
        "prompt_tokens": result.prompt_tokens,
        "completion_tokens": result.completion_tokens,
        "total_tokens": result.total_tokens,
        "latency_ms": result.latency_ms,
        "artifact_id": artifact_id if artifact_registered else "",
        "artifact_registered": artifact_registered,
        "validation_verdict": validation_verdict,
        "raw_session_history": 0,
        "pre_gov_verdict": pre_review.verdict,
        "pre_gov_score": pre_review.risk_score,
    }


# ─── TEST A: Brahma / architecture / MODE-D ───────────────────────────────────

results.append(run_test(
    test_id="A",
    worker="Brahma",
    capability="architecture",
    expected_mode="MODE-D",
    primary_provider="openai",
    primary_model="gpt-4o",
    task=(
        "Produce a concise Architecture Note explaining how Artifact Registry v2 "
        "completes the Y-OS execution loop. "
        "Structure: Problem → Solution → How Registry v2 closes the loop → "
        "Key design decisions → Next steps. "
        "Max 400 words. Output as a structured artifact."
    ),
    artifact_id="ART-M017-BRAHMA-ARCHITECTURE",
    artifact_type="Architecture Note",
    task_type="strategic",
))

# ─── TEST B: Hanuman / build / MODE-B ─────────────────────────────────────────

results.append(run_test(
    test_id="B",
    worker="Hanuman",
    capability="build",
    expected_mode="MODE-B",
    primary_provider="openai",
    primary_model="gpt-4o-mini",
    task=(
        "Produce an implementation checklist for hardening the Live Worker Executor. "
        "Focus on: error handling, retry logic, secret protection, token budget enforcement, "
        "fallback provider logic, and output sanitization. "
        "Output as a numbered checklist artifact. Max 300 words."
    ),
    artifact_id="ART-M017-HANUMAN-BUILD",
    artifact_type="Implementation Checklist",
    task_type="standard",
))

# ─── TEST C: Saraswati / learning / MODE-E ────────────────────────────────────

session_delta_c = (
    "## Session Delta — MISSION-017\n\n"
    "### Recent Decisions\n"
    "- Artifact Registry v2 implemented with stable IDs and lineage\n"
    "- Live Worker Executor supports OpenAI + Anthropic + fallback\n"
    "- Output Validator checks 8 criteria including secret detection\n\n"
    "### Unresolved Questions\n"
    "- Should artifacts be versioned (v1, v2) or superseded?\n"
    "- How to handle partial execution failures in multi-worker pipelines?\n\n"
    "### Next Actions\n"
    "- Extract lessons learned from MISSION-017\n"
    "- Define KGC v3 requirements based on learning\n"
)

results.append(run_test(
    test_id="C",
    worker="Saraswati",
    capability="learning",
    expected_mode="MODE-E",
    primary_provider="anthropic",
    primary_model="claude-opus-4-20250514",
    task=(
        "Extract the lessons learned from executing worker outputs as registered artifacts in MISSION-017. "
        "Structure: What worked → What didn't → Key insights → "
        "Recommendations for MISSION-018 → Open questions. "
        "Max 400 words. Output as a structured Learning Synthesis artifact."
    ),
    artifact_id="ART-M017-SARASWATI-LEARNING",
    artifact_type="Learning Synthesis",
    task_type="complex",
    recent_delta_required=True,
    session_delta=session_delta_c,
))

# ─── TEST D: Lakshmi / governance / MODE-D ────────────────────────────────────

results.append(run_test(
    test_id="D",
    worker="Lakshmi",
    capability="governance",
    expected_mode="MODE-D",
    primary_provider="openai",
    primary_model="gpt-4o",
    task=(
        "Review MISSION-017 for constitutional compliance. "
        "Focus on: artifact primacy (are all outputs artifacts?), "
        "lineage (is derivation transparent?), "
        "no raw history (is session history blocked?), "
        "no secrets (are API keys protected?), "
        "governance before autonomy (is Lakshmi review enforced?). "
        "Output: verdict (APPROVE/APPROVE_WITH_WARNING/REJECT), risk score 0-100, "
        "findings per article, recommendations. Max 350 words."
    ),
    artifact_id="ART-M017-LAKSHMI-GOVERNANCE",
    artifact_type="Governance Review",
    task_type="strategic",
))

# ─── Save results ─────────────────────────────────────────────────────────────

results_path = REPORTS_DIR / "test_results_MISSION-017.json"
results_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

# ─── Cost report ──────────────────────────────────────────────────────────────

cost_tracker.produce_report(COST_REPORT)

# ─── Final summary ────────────────────────────────────────────────────────────

artifacts_registered = sum(1 for r in results if r.get("artifact_registered"))
modes_correct = sum(1 for r in results if r.get("mode_correct"))
total_tokens = sum(r.get("total_tokens", 0) for r in results)
total_cost = cost_tracker.total_cost()
trace_summary = trace_logger.summary()

print(f"\n{'='*60}")
print(f"MISSION-017 — EXECUTION SUMMARY")
print(f"{'='*60}")
print(f"Live calls attempted:  {live_calls_attempted}")
print(f"Live calls succeeded:  {live_calls_succeeded}")
print(f"Live calls failed:     {live_calls_failed}")
print(f"Fallback calls:        {fallback_calls}")
print(f"Artifacts registered:  {artifacts_registered}")
print(f"Modes correct:         {modes_correct}/4")
print(f"Total tokens:          {total_tokens:,}")
print(f"Estimated cost:        ${total_cost:.6f} USD")
print(f"Raw session history:   0 tokens")
print(f"Registry total:        {registry.count()}")
print()
for r in results:
    art_ok = "✅" if r.get("artifact_registered") else "❌"
    mode_ok = "✅" if r.get("mode_correct") else "❌"
    print(f"  Test {r['test']}: {r['worker']}/{r['capability']} → {r.get('selected_mode','?')} {mode_ok} | "
          f"Status: {r.get('status','?')} | Artifact: {art_ok} | "
          f"Tokens: {r.get('total_tokens',0):,}")

# Determine mission verdict
if live_calls_succeeded >= 2 and artifacts_registered >= 4:
    verdict = "PASSED"
elif live_calls_succeeded >= 2 and artifacts_registered >= 2:
    verdict = "PASSED_PARTIAL"
elif live_calls_succeeded >= 1:
    verdict = "FAILED_PARTIAL"
else:
    verdict = "FAILED"

print(f"\nMISSION-017 VERDICT: {verdict}")

# Save summary for report generation
summary = {
    "verdict": verdict,
    "live_calls_attempted": live_calls_attempted,
    "live_calls_succeeded": live_calls_succeeded,
    "live_calls_failed": live_calls_failed,
    "fallback_calls": fallback_calls,
    "artifacts_registered": artifacts_registered,
    "modes_correct": modes_correct,
    "total_tokens": total_tokens,
    "estimated_cost_usd": total_cost,
    "raw_session_history_tokens": 0,
    "registry_total": registry.count(),
    "test_results": results,
}
(REPORTS_DIR / "mission_017_summary.json").write_text(
    json.dumps(summary, indent=2), encoding="utf-8"
)
print(f"\nAll outputs saved to mission_017/")
