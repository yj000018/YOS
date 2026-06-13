#!/usr/bin/env python3
"""MISSION-009 — Executable Constitution Validation"""
import os, json, uuid, datetime
from pathlib import Path
from openai import OpenAI
from anthropic import Anthropic

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY",""))
anthropic_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY",""))

OUTDIR = Path("/home/ubuntu/yreg/mission_009")
OUTDIR.mkdir(exist_ok=True)

CONSTITUTIONAL_CORE = """
Article I — Artifact Primacy: Artifacts are the sole source of organizational truth.
Article II — Preservation Principle: Understanding once achieved shall not be lost.
Article III — Derivation Transparency: Every state change must preserve lineage.
Article IV — Human Override Primacy: Human authority supersedes autonomous execution.
Article V — Governance Before Autonomy: Autonomy cannot exist without governance.
"""

trace = []

def log(step, worker, provider, ti, to, art_id):
    trace.append({"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "step": step, "worker": worker, "provider": provider,
        "tokens_in": ti, "tokens_out": to, "artifact_id": art_id})
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
    art_id = f"ART-M009-{uuid.uuid4().hex[:6].upper()}"
    (OUTDIR / f"{name}.md").write_text(f"# {name}\n**Artifact ID:** {art_id}\n**Date:** 2026-06-13\n\n---\n\n{content}")
    return art_id, content

print("=" * 60)
print("MISSION-009 — Executable Constitution Validation")
print("=" * 60)

# STEP 1 — Krishna (Strategy) via Anthropic
print("\n[STEP 1] Krishna (Strategy) — Anthropic...")
out1, ti1, to1 = call_anthropic(
    "You are Krishna, Y-OS Chief Strategy Officer. Precise, architectural, identity-focused.",
    f"""MISSION-009: Executable Constitution Validation

Constitutional Core v1:
{CONSTITUTIONAL_CORE}

Strategic question: What advantages emerge when constitutional doctrine becomes executable law?

Address:
1. Strategic rationale for compilation
2. Failure modes prevented by executable governance
3. Risks of compilation (constitutional meaning loss)
4. Long-term implications for Y-OS autonomy
5. When does executable governance become constitutional overreach?

350-450 words.""")
id1, _ = save("ART-M009-STRATEGY", out1)
log(1, "Krishna", "Anthropic", ti1, to1, id1)

# STEP 2 — Brahma (Architecture) via OpenAI
print("\n[STEP 2] Brahma (Architecture) — OpenAI...")
out2, ti2, to2 = call_openai(
    "You are Brahma, Y-OS Chief Architecture Officer. You design formal systems with precision.",
    f"""MISSION-009: Constitution Compiler v1 Architecture

Constitutional Core v1:
{CONSTITUTIONAL_CORE}

Strategic context (Krishna):
{out1[:400]}

Design the Constitution Compiler v1 with:
1. Architecture overview (components diagram in text)
2. Components:
   - Article Parser
   - Rule Generator
   - Rule Validator
   - Governance Engine
   - Override Handler
   - Audit Logger
3. Runtime flow: Article → Compiled Rule → Enforcement Event → Verdict
4. Rule lifecycle: Draft → Compiled → Active → Deprecated
5. Integration with CCR Runtime v1.1 and Lakshmi
6. How Human Override (Article IV) is preserved in compiled rules

500-600 words.""", max_tokens=1200)
id2, _ = save("ART-M009-ARCHITECTURE", out2)
log(2, "Brahma", "OpenAI", ti2, to2, id2)

# STEP 3 — Hanuman (Specification) via OpenAI — 2500-4000 words (multi-call)
print("\n[STEP 3] Hanuman (Specification) — OpenAI (multi-call for 2500-4000w)...")

spec_system = "You are Hanuman, Y-OS Chief Build Officer. You produce comprehensive technical specifications. Be thorough, precise, and complete."

# Part 1: Sections 1-6
spec_p1, ti3a, to3a = call_openai(spec_system,
    f"""MISSION-009: Executable Constitutional Governance Specification v1 — PART 1 (Sections 1-6)

Constitutional Core v1:
{CONSTITUTIONAL_CORE}

Architecture (Brahma):
{out2[:500]}

Write sections 1-6 of the Executable Constitutional Governance Specification v1:

1. PURPOSE
   - Why executable governance
   - Scope and boundaries
   - Non-goals

2. CONSTITUTIONAL COMPILATION MODEL
   - Compilation pipeline
   - Article → Rule transformation
   - Semantic preservation guarantees
   - Compilation constraints

3. RULE SCHEMA
   - Rule structure (JSON/YAML format)
   - Required fields: rule_id, article_source, trigger, condition, action, override_allowed, audit_required
   - Example compiled rules for Articles I, II, III

4. RULE ENGINE
   - Evaluation logic
   - Conflict resolution
   - Priority ordering
   - Execution guarantees

5. ARTICLE COMPILER
   - Per-article compilation strategy
   - Article I → Artifact existence checks
   - Article II → Lineage preservation checks
   - Article III → State change logging
   - Article IV → Override injection points
   - Article V → Pre-execution governance gates

6. GOVERNANCE RUNTIME
   - Runtime loop
   - Event processing
   - Verdict generation
   - Integration with Y-ORC

Write ~1500 words for these 6 sections.""", max_tokens=3000)

# Part 2: Sections 7-11
spec_p2, ti3b, to3b = call_openai(spec_system,
    f"""MISSION-009: Executable Constitutional Governance Specification v1 — PART 2 (Sections 7-11)

Constitutional Core v1:
{CONSTITUTIONAL_CORE}

Continue the specification with sections 7-11:

7. OVERRIDE INTEGRATION
   - Human Override Protocol (Article IV implementation)
   - Override trigger conditions
   - Override audit trail
   - Override escalation path
   - Ensuring override cannot be compiled away

8. AUDIT REQUIREMENTS
   - Audit event schema
   - Mandatory audit points per Article
   - Audit retention policy
   - Audit query interface
   - Constitutional compliance reporting

9. REGISTRY INTEGRATION
   - How compiled rules are stored as Artifacts
   - Rule versioning in Registry
   - Lineage of rule changes
   - Rule activation/deactivation as state changes

10. FAILURE MODES
    - Compilation failures
    - Runtime enforcement failures
    - Override failures
    - Audit failures
    - Constitutional drift detection
    - Recovery procedures

11. OPEN QUESTIONS
    - What cannot yet be compiled
    - Philosophical limits of executable governance
    - Future research directions
    - Constitutional questions requiring human judgment

Write ~1200 words for these 5 sections.""", max_tokens=2500)

# Combine
full_spec = f"{spec_p1}\n\n---\n\n{spec_p2}"
ti3 = ti3a + ti3b
to3 = to3a + to3b
id3, _ = save("ART-M009-EXECUTABLE-SPEC", full_spec)
wc = len(full_spec.split())
print(f"  Spec word count: ~{wc}")
log(3, "Hanuman", "OpenAI", ti3, to3, id3)

# STEP 4 — Lakshmi (Governance) via OpenAI
print("\n[STEP 4] Lakshmi (Governance) — OpenAI...")
out4, ti4, to4 = call_openai(
    """You are Lakshmi, Y-OS Governance Observer. Guardian of constitutional compliance.
Governance Determinism Framework: Score 0-15=Pristine, 16-35=Acceptable, 36-55=Elevated, 56-75=Critical, 76-100=Fatal.
Verdict: APPROVE / APPROVE_WITH_WARNING / RECOMPILE_REQUIRED / BLOCK_EXECUTION""",
    f"""MISSION-009: Governance Review of Executable Constitutional Governance

Constitutional Core v1:
{CONSTITUTIONAL_CORE}

Specification summary (Hanuman):
{full_spec[:800]}

Evaluate whether constitutional meaning survives compilation. Check each Article:
1. Article I (Artifact Primacy) — preserved in compiled rules? YES/NO
2. Article II (Preservation Principle) — preserved? YES/NO
3. Article III (Derivation Transparency) — preserved? YES/NO
4. Article IV (Human Override) — preserved and uncompilable-away? YES/NO
5. Article V (Governance Before Autonomy) — preserved? YES/NO

Then:
- Risk Score (0-100) with breakdown
- Governance Verdict
- Missing safeguards (if any)
- Required patches (if any)

400-500 words.""", max_tokens=1000)
id4, _ = save("ART-M009-GOVERNANCE", out4)
log(4, "Lakshmi", "OpenAI", ti4, to4, id4)

# STEP 5 — Saraswati (Learning) via Anthropic
print("\n[STEP 5] Saraswati (Learning) — Anthropic...")
out5, ti5, to5 = call_anthropic(
    "You are Saraswati, Y-OS Chief Learning Officer. You extract durable lessons and constitutional insights.",
    f"""MISSION-009: Learning Report

Constitutional Core v1:
{CONSTITUTIONAL_CORE}

Mission outputs:
- Strategy (Krishna): {out1[:300]}
- Architecture (Brahma): {out2[:300]}
- Governance (Lakshmi): {out4[:300]}

Extract:
1. What new constitutional knowledge was discovered?
2. Does executable governance = constitutional evolution or architectural evolution?
3. ADR candidates identified
4. Constitutional candidates (new Articles?)
5. Key organizational learning

250-350 words.""", max_tokens=700)
id5, _ = save("ART-M009-LEARNING", out5)
log(5, "Saraswati", "Anthropic", ti5, to5, id5)

# STEP 6 — Ganesha (CEO Brief) via OpenAI
print("\n[STEP 6] Ganesha (CEO Brief) — OpenAI...")
out6, ti6, to6 = call_openai(
    "You are Ganesha, Y-OS Chief Operations Officer. You produce decisive executive recommendations.",
    f"""MISSION-009: CEO Recommendation

Constitutional Core v1:
{CONSTITUTIONAL_CORE}

Mission Summary:
- Strategy (Krishna): {out1[:200]}
- Architecture (Brahma): {out2[:200]}
- Governance (Lakshmi): {out4[:200]}
- Learning (Saraswati): {out5[:200]}

Final Recommendation: Should Y-OS adopt Executable Constitutional Governance?

Output: ADOPT or REJECT with:
1. Rationale (3-4 sentences)
2. Key conditions for adoption
3. Strategic implications
4. First implementation step

150-250 words.""", max_tokens=500)
id6, _ = save("ART-M009-CEO", out6)
log(6, "Ganesha", "OpenAI", ti6, to6, id6)

# Save trace
(OUTDIR / "execution_trace.jsonl").write_text("\n".join(json.dumps(t) for t in trace))

print("\n" + "=" * 60)
print("MISSION-009 COMPLETE")
total_in = sum(t["tokens_in"] for t in trace)
total_out = sum(t["tokens_out"] for t in trace)
print(f"Total tokens: {total_in} in + {total_out} out")
print(f"Spec word count: ~{wc}")
print(f"\n=== CEO RECOMMENDATION ===")
print(out6[:400])
print(f"\n=== LAKSHMI VERDICT ===")
for line in out4.split('\n'):
    if any(x in line.upper() for x in ['VERDICT', 'SCORE', 'APPROVE', 'BLOCK', 'RECOMPILE']):
        print(line)
