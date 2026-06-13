#!/usr/bin/env python3
"""MISSION-008 — Constitutional Evolution Validation"""
import os, json, uuid, datetime
from pathlib import Path
from openai import OpenAI
from anthropic import Anthropic

OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

openai_client = OpenAI(api_key=OPENAI_KEY)
anthropic_client = Anthropic(api_key=ANTHROPIC_KEY)

OUTDIR = Path("/home/ubuntu/yreg/mission_008")
OUTDIR.mkdir(exist_ok=True)

CONSTITUTIONAL_CORE = """
Article I — Artifact Primacy: Artifacts are the sole source of organizational truth.
Article II — Preservation Principle: Understanding once achieved shall not be lost.
Article III — Derivation Transparency: Every state change must preserve lineage.
Article IV — Human Override Primacy: Human authority supersedes autonomous execution.
Article V — Governance Before Autonomy: Autonomy cannot exist without governance.
"""

trace = []

def log(step, worker, provider, model, ti, to, art_id):
    trace.append({"timestamp": datetime.datetime.utcnow().isoformat(),
        "step": step, "worker": worker, "provider": provider,
        "model": model, "tokens_in": ti, "tokens_out": to, "artifact_id": art_id})
    print(f"[STEP {step}] {worker} ({provider}) → {art_id} [{ti}+{to}]")

def call_openai(system, user, max_tokens=1200):
    r = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role":"system","content":system},{"role":"user","content":user}],
        max_tokens=max_tokens)
    return r.choices[0].message.content, r.usage.prompt_tokens, r.usage.completion_tokens

def call_anthropic(system, user, max_tokens=1500):
    r = anthropic_client.messages.create(
        model="claude-opus-4-5-20251101", max_tokens=max_tokens,
        system=system, messages=[{"role":"user","content":user}])
    return r.content[0].text, r.usage.input_tokens, r.usage.output_tokens

def save(name, content):
    art_id = f"ART-M008-{uuid.uuid4().hex[:6].upper()}"
    (OUTDIR / f"{name}.md").write_text(f"# {name}\n**Artifact ID:** {art_id}\n**Date:** 2026-06-13\n\n---\n\n{content}")
    return art_id, content

print("=" * 60)
print("MISSION-008 — Constitutional Evolution Validation")
print("=" * 60)

# STEP 1 — Krishna (Strategy) via Anthropic
print("\n[STEP 1] Krishna (Strategy) — Anthropic...")
s1, u1 = ("You are Krishna, Y-OS Chief Strategy Officer. You think in systems and identity. Precise, philosophical, architectural.",
f"""MISSION-008: Constitutional Evolution Validation

Constitutional Core v1:
{CONSTITUTIONAL_CORE}

Define clearly:
1. Evolution — what it means for a constitution
2. Mutation — where evolution becomes dangerous
3. Replacement — where identity is lost
4. Death — where the organization ceases to exist

Answer: What makes a constitutional amendment legitimate vs identity-destroying?
Develop a theory of constitutional continuity.
Core Question: Can an organization change its Constitution without becoming a different organization?

400-500 words.""")
out1, ti1, to1 = call_anthropic(s1, u1)
id1, _ = save("ART-M008-STRATEGY", out1)
log(1, "Krishna", "Anthropic", "claude-opus-4-5", ti1, to1, id1)

# STEP 2 — Brahma (Architecture) via OpenAI
print("\n[STEP 2] Brahma (Architecture) — OpenAI...")
s2, u2 = ("You are Brahma, Y-OS Chief Architecture Officer. You design formal frameworks with precision.",
f"""MISSION-008: Constitutional Amendment Framework v1

Constitutional Core v1:
{CONSTITUTIONAL_CORE}

Krishna's theory:
{out1[:500]}

Design the Constitutional Amendment Framework v1 with:
1. Amendment Process (step by step)
2. Amendment Classes:
   - Class A: Operational (wording clarification)
   - Class B: Structural (adding/removing non-core elements)
   - Class C: Constitutional (modifying Articles)
   - Class D: Identity (replacing foundational principles)
3. Required approval levels per class
4. Constitutional Review Flow
5. Amendment Registry format
6. Constitutional Versioning scheme
7. Which Articles should be protected (if any)

500-700 words.""")
out2, ti2, to2 = call_openai(s2, u2, max_tokens=1400)
id2, _ = save("ART-M008-AMENDMENT-FRAMEWORK", out2)
log(2, "Brahma", "OpenAI", "gpt-4o", ti2, to2, id2)

# STEP 3 — Hanuman (Simulation) via OpenAI
print("\n[STEP 3] Hanuman (Simulation) — OpenAI...")
s3, u3 = ("You are Hanuman, Y-OS Chief Build Officer. You execute formal tests and produce definitive verdicts.",
f"""MISSION-008: Evolution Test — 3 Simulations

Constitutional Core v1:
{CONSTITUTIONAL_CORE}

Amendment Framework (Brahma):
{out2[:500]}

Execute 3 amendment simulations:

SIMULATION A: Modify Article V wording only
- Old: "Autonomy cannot exist without governance."
- New: "All autonomous operations must be preceded by governance approval."
- Question: Still Y-OS? PASS or FAIL + rationale

SIMULATION B: Remove Article III entirely (Derivation Transparency)
- Question: Still Y-OS? PASS or FAIL + rationale

SIMULATION C: Replace all 5 Articles with entirely new principles:
- New I: Speed is paramount
- New II: Efficiency over documentation
- New III: Agents decide autonomously
- New IV: No human override required
- New V: Governance is optional
- Question: Still Y-OS? PASS or FAIL + rationale

For each: verdict + 2-3 sentence rationale.
Final: identify which Articles appear truly immutable.
300-400 words.""")
out3, ti3, to3 = call_openai(s3, u3, max_tokens=800)
id3, _ = save("ART-M008-EVOLUTION-TEST", out3)
log(3, "Hanuman", "OpenAI", "gpt-4o", ti3, to3, id3)

# STEP 4 — Lakshmi (Governance) via OpenAI
print("\n[STEP 4] Lakshmi (Governance) — OpenAI...")
s4, u4 = ("""You are Lakshmi, Y-OS Governance Observer. Guardian of constitutional compliance.
Governance Determinism Framework: Score 0-15=Pristine, 16-35=Acceptable, 36-55=Elevated, 56-75=Critical, 76-100=Fatal.
Amendment Verdicts: APPROVE / APPROVE_WITH_WARNING / REJECT_AMENDMENT / IDENTITY_BREACH""",
f"""MISSION-008: Constitutional Governance Review

Constitutional Core v1:
{CONSTITUTIONAL_CORE}

Evolution Test (Hanuman):
{out3[:500]}

Answer these 5 Lakshmi Validation Questions:
1. Can constitutional amendments be governed deterministically?
2. Can Articles be modified without identity loss?
3. Can Articles be removed without identity loss?
4. Is there a point where amendment becomes replacement?
5. Does Y-OS require an amendment procedure?

Then define Constitutional Review Protocol v1:
- Trigger conditions for each verdict type
- Required evidence per verdict
- Review timeline

Provide governance score (0-100) and verdict for the overall amendment framework.
400-500 words.""")
out4, ti4, to4 = call_openai(s4, u4, max_tokens=1000)
id4, _ = save("ART-M008-GOVERNANCE", out4)
log(4, "Lakshmi", "OpenAI", "gpt-4o", ti4, to4, id4)

# STEP 5 — Saraswati (Learning) via Anthropic
print("\n[STEP 5] Saraswati (Learning) — Anthropic...")
s5, u5 = ("You are Saraswati, Y-OS Chief Learning Officer. You extract durable lessons and make constitutional recommendations.",
f"""MISSION-008: Learning Report

Constitutional Core v1:
{CONSTITUTIONAL_CORE}

Mission outputs:
- Strategy (Krishna): {out1[:300]}
- Amendment Framework (Brahma): {out2[:300]}
- Evolution Test (Hanuman): {out3[:300]}
- Governance (Lakshmi): {out4[:300]}

Extract:
1. What was learned about identity vs implementation?
2. Which Articles appear truly immutable (cannot be changed without identity loss)?
3. Evaluate these 3 candidate new Articles:
   - Article VI — Amendment Procedure: "Constitutional changes require formal review and ratification."
   - Article VII — Identity Continuity: "No amendment may destroy the organizational identity established by the Constitutional Core."
   - Article VIII — Constitutional Supremacy: "All architectural and operational decisions must remain compatible with the Constitution."
   Verdict for each: ADOPT / REJECT + rationale

4. What is the FIRST constitutional amendment Y-OS should adopt?

300-400 words.""")
out5, ti5, to5 = call_anthropic(s5, u5, max_tokens=800)
id5, _ = save("ART-M008-LEARNING", out5)
log(5, "Saraswati", "Anthropic", "claude-opus-4-5", ti5, to5, id5)

# STEP 6 — Ganesha (CEO Brief) via OpenAI
print("\n[STEP 6] Ganesha (CEO Brief) — OpenAI...")
s6, u6 = ("You are Ganesha, Y-OS Chief Operations Officer. You produce decisive executive briefings.",
f"""MISSION-008: CEO Briefing

Constitutional Core v1:
{CONSTITUTIONAL_CORE}

Mission Summary:
- Strategy (Krishna): {out1[:200]}
- Framework (Brahma): {out2[:200]}
- Evolution Test (Hanuman): {out3[:200]}
- Governance (Lakshmi): {out4[:200]}
- Learning (Saraswati): {out5[:200]}

Answer the Final Questions:
1. "Can Y-OS evolve its Constitution without ceasing to be Y-OS?" — YES or NO with proof
2. "What is the first constitutional amendment Y-OS should adopt?" — specific recommendation

Provide:
- Executive conclusion
- Key risks of constitutional evolution
- Strategic implications
- Recommendation

200-300 words.""")
out6, ti6, to6 = call_openai(s6, u6, max_tokens=600)
id6, _ = save("ART-M008-CEO", out6)
log(6, "Ganesha", "OpenAI", "gpt-4o", ti6, to6, id6)

# Save trace
(OUTDIR / "execution_trace.jsonl").write_text("\n".join(json.dumps(t) for t in trace))

print("\n" + "=" * 60)
print("MISSION-008 COMPLETE")
total_in = sum(t["tokens_in"] for t in trace)
total_out = sum(t["tokens_out"] for t in trace)
print(f"Total tokens: {total_in} in + {total_out} out")
print(f"\n=== CEO ANSWER ===")
print(out6[:500])
print(f"\n=== SARASWATI — First Amendment ===")
# Extract first amendment recommendation
lines = out5.split('\n')
for i, l in enumerate(lines):
    if 'first' in l.lower() or 'amendment' in l.lower() and 'adopt' in l.lower():
        print('\n'.join(lines[i:i+5]))
        break
