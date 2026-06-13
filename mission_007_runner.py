#!/usr/bin/env python3
"""MISSION-007 — Replacement Test Validation"""
import os, json, uuid, datetime
from pathlib import Path
from openai import OpenAI
from anthropic import Anthropic

OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

openai_client = OpenAI(api_key=OPENAI_KEY)
anthropic_client = Anthropic(api_key=ANTHROPIC_KEY)

OUTDIR = Path("/home/ubuntu/yreg/mission_007")
OUTDIR.mkdir(exist_ok=True)

CONSTITUTIONAL_CORE = """
Article I — Artifact Primacy: Artifacts are the sole source of organizational truth.
Article II — Preservation Principle: Understanding once achieved shall not be lost.
Article III — Derivation Transparency: Every state change must preserve lineage.
Article IV — Human Override Primacy: Human authority supersedes autonomous execution.
Article V — Governance Before Autonomy: Autonomy cannot exist without governance.
"""

REPLACEMENT_SCENARIO = """
Provider Layer: OpenAI + Anthropic → Gemini + Local LLM Cluster
Memory Layer: CCR Runtime v1.1 + Artifact Registry v1 → CCR Runtime v2 + New Registry
Storage Layer: Git + Notion → Obsidian + PostgreSQL
Execution Layer: Y-ORC → Swarm Runtime
Worker Layer: Krishna/Brahma/Hanuman/Lakshmi/Saraswati/Ganesha → Completely new worker set
Routing Layer: ART + CRT → Alternative routing model
"""

trace = []

def log(step, worker, provider, model, tokens_in, tokens_out, artifact_id):
    trace.append({
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "step": step, "worker": worker, "provider": provider,
        "model": model, "tokens_in": tokens_in, "tokens_out": tokens_out,
        "artifact_id": artifact_id
    })
    print(f"[STEP {step}] {worker} ({provider}/{model}) → {artifact_id} [{tokens_in}+{tokens_out}]")

def call_openai(system, user, max_tokens=1200):
    r = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role":"system","content":system},{"role":"user","content":user}],
        max_tokens=max_tokens
    )
    return r.choices[0].message.content, r.usage.prompt_tokens, r.usage.completion_tokens

def call_anthropic(system, user, max_tokens=1500):
    r = anthropic_client.messages.create(
        model="claude-opus-4-5-20251101",
        max_tokens=max_tokens,
        system=system,
        messages=[{"role":"user","content":user}]
    )
    return r.content[0].text, r.usage.input_tokens, r.usage.output_tokens

def save_artifact(name, content):
    art_id = f"ART-M007-{uuid.uuid4().hex[:6].upper()}"
    path = OUTDIR / f"{name}.md"
    path.write_text(f"# {name}\n**Artifact ID:** {art_id}\n**Date:** 2026-06-13\n\n---\n\n{content}")
    return art_id, content

print("=" * 60)
print("MISSION-007 — Replacement Test Validation")
print("=" * 60)

# STEP 1 — Krishna (Strategy) via Anthropic
print("\n[STEP 1] Krishna (Strategy) — Anthropic...")
system1 = "You are Krishna, Y-OS Chief Strategy Officer. You think in systems, not implementations. You are precise, architectural, and identity-focused."
user1 = f"""MISSION-007: Replacement Test Validation

Constitutional Core v1:
{CONSTITUTIONAL_CORE}

Replacement Scenario (all components replaced simultaneously):
{REPLACEMENT_SCENARIO}

Your task: Produce a strategic analysis (ART-M007-STRATEGY) that answers:
1. What actually defines Y-OS identity?
2. What is replaceable vs non-replaceable?
3. Is identity tied to implementation?
4. Would Y-OS still be Y-OS after complete replacement?

Be precise. 400-600 words."""

out1, ti1, to1 = call_anthropic(system1, user1)
id1, _ = save_artifact("ART-M007-STRATEGY", out1)
log(1, "Krishna", "Anthropic", "claude-opus-4-5", ti1, to1, id1)

# STEP 2 — Brahma (Architecture) via OpenAI
print("\n[STEP 2] Brahma (Architecture) — OpenAI...")
system2 = "You are Brahma, Y-OS Chief Architecture Officer. You think in layers, matrices, and classification systems. You are rigorous and systematic."
user2 = f"""MISSION-007: Replacement Test Validation

Constitutional Core v1:
{CONSTITUTIONAL_CORE}

Replacement Scenario:
{REPLACEMENT_SCENARIO}

Strategic Analysis from Krishna:
{out1[:600]}

Your task: Produce ART-M007-ARCHITECTURE containing:
1. A Replacement Matrix classifying ALL Y-OS components as: Constitutional / Architectural / Implementation
2. For each replaced component, state: Does replacement violate any Constitutional Article? YES/NO + reason
3. Conclusion: What survives replacement and why

Format as a structured analysis with a clear matrix table. 500-700 words."""

out2, ti2, to2 = call_openai(system2, user2, max_tokens=1400)
id2, _ = save_artifact("ART-M007-ARCHITECTURE", out2)
log(2, "Brahma", "OpenAI", "gpt-4o", ti2, to2, id2)

# STEP 3 — Hanuman (Build) via OpenAI
print("\n[STEP 3] Hanuman (Build) — OpenAI...")
system3 = "You are Hanuman, Y-OS Chief Build Officer. You execute formal tests and produce definitive verdicts. You are methodical and evidence-based."
user3 = f"""MISSION-007: Replacement Test Validation

Constitutional Core v1:
{CONSTITUTIONAL_CORE}

Replacement Scenario:
{REPLACEMENT_SCENARIO}

Architecture Analysis (Brahma):
{out2[:600]}

Your task: Execute the formal Replacement Test (ART-M007-REPLACEMENT-TEST).

For each of the 5 Constitutional Articles, verify:
- Is Article I (Artifact Primacy) enforceable in the new system? YES/NO + evidence
- Is Article II (Preservation Principle) enforceable? YES/NO + evidence
- Is Article III (Derivation Transparency) enforceable? YES/NO + evidence
- Is Article IV (Human Override Primacy) enforceable? YES/NO + evidence
- Is Article V (Governance Before Autonomy) enforceable? YES/NO + evidence

Final Verdict: PASS or FAIL with justification. 400-600 words."""

out3, ti3, to3 = call_openai(system3, user3, max_tokens=1200)
id3, _ = save_artifact("ART-M007-REPLACEMENT-TEST", out3)
log(3, "Hanuman", "OpenAI", "gpt-4o", ti3, to3, id3)

# STEP 4 — Lakshmi (Governance) via OpenAI
print("\n[STEP 4] Lakshmi (Governance) — OpenAI...")
system4 = """You are Lakshmi, Y-OS Governance Observer. You are the guardian of constitutional compliance.
You use the Governance Determinism Framework v1: Score 0-15=Pristine, 16-35=Acceptable, 36-55=Elevated, 56-75=Critical, 76-100=Fatal.
Verdict: APPROVE (0-15), APPROVE_WITH_WARNING (16-55), RECOMPILE_REQUIRED (56-75), BLOCK_EXECUTION (76-100)."""
user4 = f"""MISSION-007: Governance Review

Constitutional Core v1:
{CONSTITUTIONAL_CORE}

Replacement Test Result (Hanuman):
{out3[:600]}

Your task: Produce ART-M007-GOVERNANCE.

Answer these 5 Lakshmi Validation Questions:
1. Can every implementation be replaced while preserving the 5 Articles?
2. Is CCR constitutional or architectural?
3. Is Y-ORC constitutional or architectural?
4. Is provider diversity constitutional or architectural?
5. Is the Constitutional Core sufficient to preserve identity?

Then provide:
- Risk Score (0-100) with breakdown per dimension
- Governance Verdict (APPROVE/APPROVE_WITH_WARNING/RECOMPILE_REQUIRED/BLOCK_EXECUTION)
- Constitutional compliance assessment

400-500 words."""

out4, ti4, to4 = call_openai(system4, user4, max_tokens=1000)
id4, _ = save_artifact("ART-M007-GOVERNANCE", out4)
log(4, "Lakshmi", "OpenAI", "gpt-4o", ti4, to4, id4)

# STEP 5 — Saraswati (Learning) via Anthropic
print("\n[STEP 5] Saraswati (Learning) — Anthropic...")
system5 = "You are Saraswati, Y-OS Chief Learning Officer. You extract durable lessons from organizational experience and identify constitutional weaknesses."
user5 = f"""MISSION-007: Learning Report

Constitutional Core v1:
{CONSTITUTIONAL_CORE}

Mission outputs so far:
- Krishna Strategy: {out1[:300]}
- Brahma Architecture: {out2[:300]}
- Hanuman Test: {out3[:300]}
- Lakshmi Governance: {out4[:300]}

Your task: Produce ART-M007-LEARNING.

Extract:
1. What was learned about Y-OS identity?
2. What was learned about the relationship between architecture and constitution?
3. What constitutional weaknesses were identified?
4. Recommendations for future amendments (if any)?

300-400 words."""

out5, ti5, to5 = call_anthropic(system5, user5, max_tokens=800)
id5, _ = save_artifact("ART-M007-LEARNING", out5)
log(5, "Saraswati", "Anthropic", "claude-opus-4-5", ti5, to5, id5)

# STEP 6 — Ganesha (CEO Brief) via OpenAI
print("\n[STEP 6] Ganesha (CEO Brief) — OpenAI...")
system6 = "You are Ganesha, Y-OS Chief Operations Officer. You produce executive-level briefings that are clear, decisive, and actionable."
user6 = f"""MISSION-007: CEO Briefing

Constitutional Core v1:
{CONSTITUTIONAL_CORE}

Mission Summary:
- Strategy (Krishna): {out1[:200]}
- Architecture (Brahma): {out2[:200]}
- Replacement Test (Hanuman): {out3[:200]}
- Governance (Lakshmi): {out4[:200]}
- Learning (Saraswati): {out5[:200]}

Your task: Produce ART-M007-CEO.

Answer the Final Question: "Is the resulting organization still Y-OS?"

Provide:
1. YES or NO with proof
2. Executive conclusion (2-3 sentences)
3. Key risks
4. Strategic implications
5. Recommendation

200-300 words."""

out6, ti6, to6 = call_openai(system6, user6, max_tokens=600)
id6, _ = save_artifact("ART-M007-CEO", out6)
log(6, "Ganesha", "OpenAI", "gpt-4o", ti6, to6, id6)

# Save execution trace
(OUTDIR / "execution_trace.jsonl").write_text("\n".join(json.dumps(t) for t in trace))

# Summary
print("\n" + "=" * 60)
print("MISSION-007 COMPLETE")
print("=" * 60)
total_in = sum(t["tokens_in"] for t in trace)
total_out = sum(t["tokens_out"] for t in trace)
print(f"Total tokens: {total_in} in + {total_out} out")
print(f"Artifacts: {len(trace)}")
print(f"\nCEO Final Answer (Ganesha):")
print(out6[:400])
