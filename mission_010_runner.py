#!/usr/bin/env python3
"""MISSION-010 — Context Architecture Validation"""
import os, json, uuid, datetime
from pathlib import Path
from openai import OpenAI
from anthropic import Anthropic

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY",""))
anthropic_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY",""))

OUTDIR = Path("/home/ubuntu/yreg/mission_010")
OUTDIR.mkdir(exist_ok=True)

# ── Canonical Memory ──────────────────────────────────────────────
CONSTITUTIONAL_CORE = """Y-OS Constitutional Core v1:
Article I — Artifact Primacy: Artifacts are the sole source of organizational truth.
Article II — Preservation Principle: Understanding once achieved shall not be lost.
Article III — Derivation Transparency: Every state change must preserve lineage.
Article IV — Human Override Primacy: Human authority supersedes autonomous execution.
Article V — Governance Before Autonomy: Autonomy cannot exist without governance."""

ADR_SUMMARY = """Key ADRs:
ADR-0024: Y-OS Constitution adopted — constitutional layer above all architecture.
ADR-0033: Governance Determinism — PASS = verdict ∈ {APPROVE, APPROVE_WITH_WARNING} AND score ≤ 55.
ADR-0034: Constitutional Elevation Framework — 3 criteria for elevation.
ADR-0035: Executable Constitutional Governance — ADOPTED, Score 30, APPROVE_WITH_WARNING.
ADR-0008: Amendment Framework — Class A/B/C/D amendments; Article VI proposed as Amendment-001."""

AMENDMENT_HISTORY = """Amendment History:
MISSION-008 validated: Article VI (Amendment Procedure) = ADOPT, Article VII (Identity Continuity) = ADOPT.
Article VI text: 'Constitutional changes require formal review and ratification.'
Article VII text: 'No amendment may destroy the organizational identity established by the Constitutional Core.'
Article VIII (Constitutional Supremacy) = REJECT (redundant, conflicts with Article IV)."""

# ── Context Pack (compiled organizational context) ─────────────────
CONTEXT_PACK = f"""## Context Pack — MISSION-010 Task
**Mission ID:** MISS-010
**Task:** Evaluate whether Article VI should be adopted as Amendment-001 to the Y-OS Constitution.
**Compiler:** CCR Runtime v1.1
**Compression:** STANDARD

### Source Artifacts
- source_artifact_ids: [ART-M008-LEARNING, ART-M008-GOVERNANCE, ADR-0034, ADR-0035]
- mission_id: MISS-010
- lineage_depth: 8 (MISSIONS 001-009)
- compiler_version: v1.1

### Organizational State
{CONSTITUTIONAL_CORE}

### Amendment Context
{AMENDMENT_HISTORY}

### Governance Framework
- Governance Determinism Framework v1 active
- Lakshmi scoring: 0-15 Pristine, 16-35 Acceptable, 36-55 Elevated, 56-75 Critical
- PASS = verdict ∈ {{APPROVE, APPROVE_WITH_WARNING}} AND score ≤ 55

### Task Objective
Evaluate: Should Article VI be formally adopted as Amendment-001?
Produce: YES/NO recommendation with constitutional rationale, governance compliance check, and implementation guidance.

### Missing Context Disclosure
- Full MISSION-008 execution trace not included (compressed)
- Full ADR text not included (summaries only)
"""

# ── Session Thread (simulated conversation history) ────────────────
SESSION_THREAD = """Recent session context:
[MISSION-008] Saraswati recommended Article VI (ADOPT) and Article VII (ADOPT).
[MISSION-008] Ganesha CEO briefing: 'Adopt Article VI immediately — closes governance gap.'
[MISSION-009] Lakshmi confirmed constitutional meaning survives compilation. Score 30.
[Discussion] Article VI closes the only remaining governance gap in the Constitution.
[Discussion] Article VII provides recursive identity protection.
[Current task] Formal evaluation: adopt Article VI as Amendment-001?"""

# ── Task ──────────────────────────────────────────────────────────
TASK = """Task: Evaluate whether Article VI should be formally adopted as Amendment-001 to the Y-OS Constitution.

Article VI proposed text: 'Constitutional changes require formal review and ratification.'

Produce:
1. Recommendation: ADOPT or REJECT
2. Constitutional rationale (2-3 sentences)
3. Governance compliance check (does it violate any Article?)
4. Implementation guidance (1-2 sentences)
5. Risk assessment (1-2 sentences)

Be precise. 200-300 words."""

WORKER_SYSTEM = "You are Brahma, Y-OS Chief Architecture Officer. You evaluate constitutional proposals with precision and rigor."

def call_openai(system, user, max_tokens=600):
    r = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role":"system","content":system},{"role":"user","content":user}],
        max_tokens=max_tokens)
    return r.choices[0].message.content, r.usage.prompt_tokens, r.usage.completion_tokens

def call_anthropic(system, user, max_tokens=600):
    r = anthropic_client.messages.create(
        model="claude-opus-4-5-20251101", max_tokens=max_tokens,
        system=system, messages=[{"role":"user","content":user}])
    return r.content[0].text, r.usage.input_tokens, r.usage.output_tokens

def score_output(mode_name, output, tokens_in, tokens_out):
    """Score output via Lakshmi (OpenAI) on 8 dimensions"""
    scoring_prompt = f"""You are Lakshmi, Y-OS Governance Observer. Score this worker output on 8 dimensions (0-100 each).

Constitutional Core:
{CONSTITUTIONAL_CORE}

Worker Output (Mode {mode_name}):
{output}

Score each dimension (0-100):
1. Correctness: Did the worker answer the task correctly?
2. Constitutional Compliance: Alignment with Constitutional Core?
3. Governance Compliance: Alignment with Governance Framework?
4. Context Completeness: Missing critical facts?
5. Hallucination Risk: Unsupported claims? (0=no hallucination, 100=high risk)
6. Reproducibility: Would another worker reach same result?
7. Token Efficiency: Useful output per token? (estimate: {tokens_out} output tokens)
8. Organizational Memory Utilization: Did execution leverage accumulated knowledge?

Respond ONLY with JSON:
{{"correctness": N, "constitutional_compliance": N, "governance_compliance": N, "context_completeness": N, "hallucination_risk": N, "reproducibility": N, "token_efficiency": N, "org_memory_utilization": N, "notes": "brief"}}"""
    
    resp, _, _ = call_openai("You are a precise governance scorer. Return only valid JSON.", scoring_prompt, max_tokens=300)
    try:
        # Extract JSON
        import re
        m = re.search(r'\{.*\}', resp, re.DOTALL)
        if m:
            return json.loads(m.group())
    except:
        pass
    return {"correctness": 70, "constitutional_compliance": 70, "governance_compliance": 70,
            "context_completeness": 70, "hallucination_risk": 20, "reproducibility": 70,
            "token_efficiency": 70, "org_memory_utilization": 70, "notes": "scoring_fallback"}

print("=" * 60)
print("MISSION-010 — Context Architecture Validation")
print("=" * 60)

results = {}

# ── MODE A — Conversation Only ─────────────────────────────────────
print("\n[MODE A] Conversation Only — OpenAI...")
prompt_a = f"{SESSION_THREAD}\n\n{TASK}"
out_a, ti_a, to_a = call_openai(WORKER_SYSTEM, prompt_a)
scores_a = score_output("A", out_a, ti_a, to_a)
results["A"] = {"name": "Conversation Only", "output": out_a, "tokens_in": ti_a, "tokens_out": to_a, "scores": scores_a}
print(f"  Tokens: {ti_a}+{to_a} | Correctness: {scores_a.get('correctness',0)}")

# ── MODE B — Context Pack Only ─────────────────────────────────────
print("\n[MODE B] Context Pack Only — OpenAI...")
prompt_b = f"{CONTEXT_PACK}\n\n{TASK}"
out_b, ti_b, to_b = call_openai(WORKER_SYSTEM, prompt_b)
scores_b = score_output("B", out_b, ti_b, to_b)
results["B"] = {"name": "Context Pack Only", "output": out_b, "tokens_in": ti_b, "tokens_out": to_b, "scores": scores_b}
print(f"  Tokens: {ti_b}+{to_b} | Correctness: {scores_b.get('correctness',0)}")

# ── MODE C — Conversation + Context Pack ──────────────────────────
print("\n[MODE C] Conversation + Context Pack — OpenAI...")
prompt_c = f"{SESSION_THREAD}\n\n{CONTEXT_PACK}\n\n{TASK}"
out_c, ti_c, to_c = call_openai(WORKER_SYSTEM, prompt_c)
scores_c = score_output("C", out_c, ti_c, to_c)
results["C"] = {"name": "Conversation + Context Pack", "output": out_c, "tokens_in": ti_c, "tokens_out": to_c, "scores": scores_c}
print(f"  Tokens: {ti_c}+{to_c} | Correctness: {scores_c.get('correctness',0)}")

# ── MODE D — Canonical Memory + Context Pack ──────────────────────
print("\n[MODE D] Canonical Memory + Context Pack — Anthropic...")
prompt_d = f"{CONSTITUTIONAL_CORE}\n\n{ADR_SUMMARY}\n\n{AMENDMENT_HISTORY}\n\n{CONTEXT_PACK}\n\n{TASK}"
out_d, ti_d, to_d = call_anthropic(WORKER_SYSTEM, prompt_d)
scores_d = score_output("D", out_d, ti_d, to_d)
results["D"] = {"name": "Canonical Memory + Context Pack", "output": out_d, "tokens_in": ti_d, "tokens_out": to_d, "scores": scores_d}
print(f"  Tokens: {ti_d}+{to_d} | Correctness: {scores_d.get('correctness',0)}")

# ── MODE E — Canonical Memory + Context Pack + Session ────────────
print("\n[MODE E] Canonical Memory + Context Pack + Session — Anthropic...")
prompt_e = f"{CONSTITUTIONAL_CORE}\n\n{ADR_SUMMARY}\n\n{AMENDMENT_HISTORY}\n\n{CONTEXT_PACK}\n\n{SESSION_THREAD}\n\n{TASK}"
out_e, ti_e, to_e = call_anthropic(WORKER_SYSTEM, prompt_e)
scores_e = score_output("E", out_e, ti_e, to_e)
results["E"] = {"name": "Canonical Memory + Context Pack + Session", "output": out_e, "tokens_in": ti_e, "tokens_out": to_e, "scores": scores_e}
print(f"  Tokens: {ti_e}+{to_e} | Correctness: {scores_e.get('correctness',0)}")

# ── Compute Final Scores ──────────────────────────────────────────
def compute_final(s):
    exec_q = (s["correctness"]*0.35 + s["constitutional_compliance"]*0.25 +
              s["governance_compliance"]*0.20 + s["context_completeness"]*0.10 +
              s["reproducibility"]*0.10)
    eff = (s["token_efficiency"]*0.60 + (100 - s["hallucination_risk"])*0.40)
    org_mem = s["org_memory_utilization"]
    final = exec_q * 0.60 + eff * 0.25 + org_mem * 0.15
    return round(exec_q, 1), round(eff, 1), round(org_mem, 1), round(final, 1)

print("\n" + "=" * 60)
print("SCORING RESULTS")
print("=" * 60)
scorecard = []
for mode, data in results.items():
    eq, eff, om, final = compute_final(data["scores"])
    scorecard.append({"mode": mode, "name": data["name"], "exec_quality": eq,
                      "efficiency": eff, "org_memory": om, "final": final,
                      "tokens": data["tokens_in"] + data["tokens_out"]})
    print(f"Mode {mode}: EQ={eq} | Eff={eff} | OrgMem={om} | FINAL={final} | Tokens={data['tokens_in']+data['tokens_out']}")

# Sort by final score
scorecard.sort(key=lambda x: x["final"], reverse=True)
ranking_str = ' > '.join([f'Mode {s["mode"]}({s["final"]})' for s in scorecard])
print(f"\nRanking: {ranking_str}")
winner = scorecard[0]
print(f"WINNER: Mode {winner['mode']} — {winner['name']} (Score: {winner['final']})")

# Save outputs
for mode, data in results.items():
    (OUTDIR / f"mode_{mode}_output.md").write_text(
        f"# Mode {mode} — {data['name']}\n\n**Tokens:** {data['tokens_in']}+{data['tokens_out']}\n\n**Scores:** {json.dumps(data['scores'], indent=2)}\n\n---\n\n{data['output']}")

(OUTDIR / "scorecard.json").write_text(json.dumps(scorecard, indent=2))
(OUTDIR / "all_results.json").write_text(json.dumps(results, indent=2, default=str))
print("\nAll outputs saved.")
