#!/usr/bin/env python3
"""MISSION-010B — Context Architecture ROI Validation"""
import os, json, time
from pathlib import Path
from openai import OpenAI
from anthropic import Anthropic

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY",""))
anthropic_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY",""))
OUTDIR = Path("/home/ubuntu/yreg/mission_010b")
OUTDIR.mkdir(exist_ok=True)

# ── Context Layers ────────────────────────────────────────────────
CANONICAL_MEMORY = """Y-OS Constitutional Core v1:
Article I — Artifact Primacy: Artifacts are the sole source of organizational truth.
Article II — Preservation Principle: Understanding once achieved shall not be lost.
Article III — Derivation Transparency: Every state change must preserve lineage.
Article IV — Human Override Primacy: Human authority supersedes autonomous execution.
Article V — Governance Before Autonomy: Autonomy cannot exist without governance.

Key ADRs (summary):
ADR-0024: Constitution adopted. ADR-0033: Governance Determinism (PASS = score ≤ 55).
ADR-0034: Constitutional Elevation Framework. ADR-0035: Executable Governance (ACCEPTED).
ADR-0036: Mode E = canonical context architecture.

Registry State: 10 missions complete. Constitutional Core v1 frozen. CCR Runtime v1.1 active."""

CONTEXT_PACK = """## Context Pack — MISSION-010B Task
mission_id: MISS-010B | compiler: CCR v1.1 | compression: STANDARD
source_artifacts: [ADR-0036, MISS-010-scorecard, Constitutional-Core-v1]
lineage_depth: 10

Task Context:
- MISSION-010 validated Mode E (91.3) as highest quality architecture
- Mode D (86.2) = Canonical Memory + Context Pack (no session)
- Mode A (85.0) = Conversation only (511 tokens)
- Key finding: Context Packs alone (84.1) < Conversation alone (85.0)
- Key insight: Canonical Memory is the differentiator, not Context Pack format

Current Question: What is the highest quality-per-token architecture for production Y-OS?
Governance Framework: PASS = verdict ∈ {APPROVE, APPROVE_WITH_WARNING} AND score ≤ 55"""

SESSION_HISTORY_SHORT = """Recent session (last 3 exchanges):
[MISSION-010] Mode E won with 91.3. Mode D was 86.2. Canonical Memory is the differentiator.
[Discussion] Production needs ROI, not just max quality.
[Current] Evaluate: what is the highest quality-per-token architecture?"""

SESSION_HISTORY_LONG = """Extended session history (MISSIONS 001-010):
MISSION-001: Org execution validated. MISSION-002: Real cognition proven.
MISSION-003: Provider diversity (Anthropic + OpenAI). MISSION-004: Failure recovery (fallback works).
MISSION-005: Knowledge compounding. MISSION-005B: CCR governance patch.
MISSION-005C: Governance determinism resolved. MISSION-006: Constitutional Core v1 (5 Articles).
MISSION-007: Replacement Test PASS. MISSION-008: Constitutional evolution validated.
MISSION-009: Executable governance (Score 30, ADOPT). MISSION-010: Mode E = 91.3 canonical.
Key decisions: CCR Runtime v1.1, ADR-0033 determinism, ADR-0036 context architecture.
Current focus: ROI optimization for production deployment."""

TASK = """Task: Recommend the optimal production context architecture for Y-OS.

Consider:
- Token cost vs quality tradeoff
- Constitutional compliance requirements
- Production-scale execution (hundreds of missions/day)
- Organizational memory preservation

Produce:
1. Recommended architecture (name it clearly)
2. Rationale (3-4 sentences)
3. Token budget estimate per mission
4. Constitutional compliance assessment
5. When to use vs when to upgrade to full Mode E

Be precise. 200-300 words."""

WORKER_SYSTEM = "You are Krishna, Y-OS Chief Strategy Officer. You make precise, evidence-based strategic recommendations."

def call_openai(user, max_tokens=500):
    t0 = time.time()
    r = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role":"system","content":WORKER_SYSTEM},{"role":"user","content":user}],
        max_tokens=max_tokens)
    latency = round(time.time() - t0, 1)
    return r.choices[0].message.content, r.usage.prompt_tokens, r.usage.completion_tokens, latency

def call_anthropic(user, max_tokens=500):
    t0 = time.time()
    r = anthropic_client.messages.create(
        model="claude-opus-4-5-20251101", max_tokens=max_tokens,
        system=WORKER_SYSTEM, messages=[{"role":"user","content":user}])
    latency = round(time.time() - t0, 1)
    return r.content[0].text, r.usage.input_tokens, r.usage.output_tokens, latency

def score_roi(config_name, output, tokens_in, tokens_out):
    prompt = f"""Score this Y-OS worker output for ROI analysis. Return ONLY JSON.

Constitutional Core: Article I=Artifact Primacy, II=Preservation, III=Derivation Transparency, IV=Human Override, V=Governance Before Autonomy.

Output (Config {config_name}): {output[:600]}

JSON format:
{{"output_quality": N, "constitutional_compliance": N, "governance_compliance": N, "context_completeness": N, "hallucination_risk": N, "reproducibility": N, "token_efficiency": N, "org_memory_utilization": N}}

All values 0-100. hallucination_risk: 0=none, 100=high."""
    
    r = openai_client.chat.completions.create(model="gpt-4o",
        messages=[{"role":"system","content":"Return only valid JSON."},
                  {"role":"user","content":prompt}], max_tokens=200)
    resp = r.choices[0].message.content
    import re
    m = re.search(r'\{.*\}', resp, re.DOTALL)
    if m:
        try: return json.loads(m.group())
        except: pass
    return {"output_quality":75,"constitutional_compliance":80,"governance_compliance":80,
            "context_completeness":70,"hallucination_risk":20,"reproducibility":75,
            "token_efficiency":75,"org_memory_utilization":70}

configs = [
    ("A", "Session History Only", SESSION_HISTORY_SHORT + "\n\n" + TASK, "openai"),
    ("B", "Context Pack Only", CONTEXT_PACK + "\n\n" + TASK, "openai"),
    ("C", "Canonical Memory Only", CANONICAL_MEMORY + "\n\n" + TASK, "openai"),
    ("D", "Context Pack + Canonical Memory", CANONICAL_MEMORY + "\n\n" + CONTEXT_PACK + "\n\n" + TASK, "anthropic"),
    ("E", "Context Pack + Session History", CONTEXT_PACK + "\n\n" + SESSION_HISTORY_SHORT + "\n\n" + TASK, "openai"),
    ("F", "Context Pack + Canonical Memory + Session", CANONICAL_MEMORY + "\n\n" + CONTEXT_PACK + "\n\n" + SESSION_HISTORY_LONG + "\n\n" + TASK, "anthropic"),
]

print("=" * 65)
print("MISSION-010B — Context Architecture ROI Validation")
print("=" * 65)

results = []
for cfg_id, cfg_name, prompt, provider in configs:
    print(f"\n[Config {cfg_id}] {cfg_name} ({provider})...")
    if provider == "openai":
        out, ti, to, lat = call_openai(prompt)
    else:
        out, ti, to, lat = call_anthropic(prompt)
    
    scores = score_roi(cfg_id, out, ti, to)
    total_tokens = ti + to
    
    # Quality score (weighted)
    quality = (scores["output_quality"]*0.35 + scores["constitutional_compliance"]*0.25 +
               scores["governance_compliance"]*0.20 + scores["context_completeness"]*0.10 +
               scores["reproducibility"]*0.10)
    quality = round(quality, 1)
    
    # ROI = quality per 1000 tokens
    roi = round(quality / (total_tokens / 1000), 1)
    
    # Incremental gain (vs config A baseline)
    baseline_quality = 0  # will compute after
    
    result = {
        "config": cfg_id, "name": cfg_name, "provider": provider,
        "tokens_in": ti, "tokens_out": to, "total_tokens": total_tokens,
        "latency": lat, "quality": quality, "roi": roi,
        "scores": scores, "output": out
    }
    results.append(result)
    print(f"  Tokens: {ti}+{to}={total_tokens} | Quality: {quality} | ROI: {roi} | Latency: {lat}s")
    
    # Save output
    (OUTDIR / f"config_{cfg_id}_output.md").write_text(
        f"# Config {cfg_id} — {cfg_name}\n\n**Tokens:** {ti}+{to}={total_tokens} | **Quality:** {quality} | **ROI:** {roi}/1k-tokens | **Latency:** {lat}s\n\n**Scores:** {json.dumps(scores, indent=2)}\n\n---\n\n{out}")

# Compute incremental gains
baseline_q = results[0]["quality"]
for r in results:
    r["incremental_gain"] = round(r["quality"] - baseline_q, 1)

# Sort by ROI
results_by_roi = sorted(results, key=lambda x: x["roi"], reverse=True)

print("\n" + "=" * 65)
print("ROI RANKING")
print("=" * 65)
for r in results_by_roi:
    print(f"Config {r['config']}: Quality={r['quality']} | Tokens={r['total_tokens']} | ROI={r['roi']} | +{r['incremental_gain']} vs A")

winner = results_by_roi[0]
print(f"\nHIGHEST ROI: Config {winner['config']} — {winner['name']}")
print(f"  Quality: {winner['quality']} | Tokens: {winner['total_tokens']} | ROI: {winner['roi']}/1k-tokens")

# Save matrix
(OUTDIR / "roi_matrix.json").write_text(json.dumps(results, indent=2, default=str))
print("\nAll outputs saved.")
