#!/usr/bin/env python3
"""
MISSION-005 — Knowledge Compounding Validation
Produce CCR Runtime v1 architectural specification (3000-5000 words)
Identify ADR candidates. Prove Y-OS generates compounding architectural knowledge.
"""

import os, json, uuid, time, datetime
from pathlib import Path

MISSION_ID = "MISSION-005"
OUT_DIR = Path("/home/ubuntu/yreg/mission_005")
OUT_DIR.mkdir(exist_ok=True)
(OUT_DIR / "artifacts").mkdir(exist_ok=True)

registry = {}
lineage = []
execution_trace = []

def make_id():
    return f"ART-M005-{uuid.uuid4().hex[:6].upper()}"

def register_artifact(art_id, art_type, worker, provider, model, parent_id, content):
    ts = datetime.datetime.now(datetime.UTC).isoformat()
    art = {"id": art_id, "type": art_type, "worker": worker, "provider": provider,
           "model": model, "parent_id": parent_id, "status": "Done", "created_at": ts}
    registry[art_id] = art
    if parent_id:
        lineage.append({"child": art_id, "parent": parent_id, "ts": ts})
        if parent_id in registry:
            registry[parent_id]["status"] = "Consumed"
    path = OUT_DIR / "artifacts" / f"{art_id}.md"
    path.write_text(f"# {art_id} — {art_type}\n\n**Worker:** {worker}  \n**Provider:** {provider}  \n**Model:** {model}  \n**Parent:** {parent_id or '—'}\n\n---\n\n{content}\n")
    return art

def call_openai(system_prompt, user_prompt, max_tokens=4000):
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    start = time.time()
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}],
        max_tokens=max_tokens
    )
    return {
        "content": resp.choices[0].message.content,
        "provider": "openai", "model": resp.model,
        "prompt_tokens": resp.usage.prompt_tokens,
        "completion_tokens": resp.usage.completion_tokens,
        "ms": int((time.time()-start)*1000)
    }

def call_anthropic(system_prompt, user_prompt, max_tokens=4000):
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    start = time.time()
    resp = client.messages.create(
        model="claude-opus-4-5-20251101",
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role":"user","content":user_prompt}]
    )
    return {
        "content": resp.content[0].text,
        "provider": "anthropic", "model": resp.model,
        "prompt_tokens": resp.usage.input_tokens,
        "completion_tokens": resp.usage.output_tokens,
        "ms": int((time.time()-start)*1000)
    }

def run_mission():
    print("="*60)
    print("MISSION-005 — Knowledge Compounding Validation")
    print("="*60)

    # Step 0: CEO Directive
    dir_id = make_id()
    directive = "Design the definitive production architecture of the Y-OS Context Continuity Layer (CCR Runtime v1). This result must become a real ADR candidate and permanently change the future design of Y-OS."
    register_artifact(dir_id, "CEO Directive", "CEO", "Human", "Human", None, directive)
    print(f"\n[STEP 0] CEO Directive → {dir_id}")

    # Step 1: Krishna — Strategic Analysis (Anthropic)
    print(f"\n[STEP 1] STRATEGY → Krishna (Anthropic/claude-opus-4-5)")
    r1 = call_anthropic(
        "You are Krishna, Chief Strategy Officer of Y-OS. You define WHAT and WHY. Architectural precision. No filler.",
        """Mission: Design the definitive production architecture of CCR Runtime v1 — the Y-OS Context Continuity Layer.

Your question: Why do most memory and context systems fail to preserve cognitive continuity across sessions, providers, and time?

Analyze:
1. The fundamental failure modes of existing memory systems (RAG, conversation history, vector DBs, session state)
2. Why context loss is an organizational problem, not just a technical one
3. The 5 strategic principles that a production CCR must satisfy
4. Why artifact-centric context is superior to conversation-centric context
5. What "cognitive continuity" means in an AI-native organization

Write a Strategic Brief. Governance-quality. 600-900 words.""",
        max_tokens=1200
    )
    art1 = make_id()
    register_artifact(art1, "Strategy Brief", "Krishna", r1["provider"], r1["model"], dir_id, r1["content"])
    print(f"  ✅ {art1} | {r1['provider']}/{r1['model']} | {r1['prompt_tokens']}+{r1['completion_tokens']} tokens | {r1['ms']}ms")

    # Step 2: Brahma — Architecture (OpenAI)
    print(f"\n[STEP 2] ARCHITECTURE → Brahma (OpenAI/gpt-4o)")
    r2 = call_openai(
        "You are Brahma, Chief Architect of Y-OS. You define HOW — precise component design, data flows, interfaces.",
        f"""Strategic Brief received:

{r1['content'][:800]}

Your question: What is the definitive architecture of CCR Runtime v1?

Design the complete architecture including:

1. COMPONENTS (name, responsibility, interface)
   - Artifact Retriever
   - Lineage Traverser
   - Context Selector
   - Compression Engine
   - Context Pack Generator
   - Mission Continuity Manager
   - Governance Hook

2. DATA FLOWS
   - Input: Mission ID + Worker + Capability
   - Processing pipeline (step by step)
   - Output: Context Pack (YAML schema)

3. CONTEXT PACK SCHEMA v2
   - Required fields
   - Optional fields
   - Compression levels (FULL / COMPRESSED / MINIMAL)
   - Provider portability requirements

4. RETRIEVAL STRATEGY
   - Artifact selection algorithm
   - Lineage depth rules
   - Relevance scoring

5. COMPRESSION STRATEGY
   - Token budget per compression level
   - What gets preserved vs summarized
   - Quality preservation rules

6. GOVERNANCE HOOKS
   - What Lakshmi observes
   - Audit trail requirements
   - Override mechanisms

Be precise. This becomes a production specification.""",
        max_tokens=2000
    )
    art2 = make_id()
    register_artifact(art2, "Architecture Package", "Brahma", r2["provider"], r2["model"], art1, r2["content"])
    print(f"  ✅ {art2} | {r2['provider']}/{r2['model']} | {r2['prompt_tokens']}+{r2['completion_tokens']} tokens | {r2['ms']}ms")

    # Step 3: Hanuman — Full Specification (OpenAI, high token budget)
    print(f"\n[STEP 3] BUILD → Hanuman (OpenAI/gpt-4o) — 3000-5000 word spec")
    r3 = call_openai(
        "You are Hanuman, Lead Builder of Y-OS. Build exactly what Brahma architected. Production-quality technical writing. No filler, no repetition.",
        f"""Build the complete specification document: "CCR Runtime v1 — Context Continuity Engine"

Strategy (Krishna):
{r1['content'][:600]}

Architecture (Brahma):
{r2['content'][:1200]}

Produce a production-ready architectural specification with these sections:

# CCR Runtime v1 — Context Continuity Engine
## Executive Summary
## 1. Purpose and Scope
## 2. Architectural Principles
## 3. Component Specifications
   ### 3.1 Artifact Retriever
   ### 3.2 Lineage Traverser
   ### 3.3 Context Selector
   ### 3.4 Compression Engine
   ### 3.5 Context Pack Generator
   ### 3.6 Mission Continuity Manager
   ### 3.7 Governance Hook
## 4. Runtime Pipeline
## 5. Context Pack Schema v2 (YAML)
## 6. Retrieval Strategy
## 7. Compression Strategy
## 8. Provider Portability
## 9. Governance Integration
## 10. Implementation Notes
## 11. Open Questions

Each section must be substantive and actionable.
Target: 3000-5000 words of real specification content.
This document will become an ADR candidate.""",
        max_tokens=4000
    )
    art3 = make_id()
    register_artifact(art3, "CCR Runtime v1 Specification", "Hanuman", r3["provider"], r3["model"], art2, r3["content"])
    print(f"  ✅ {art3} | {r3['provider']}/{r3['model']} | {r3['prompt_tokens']}+{r3['completion_tokens']} tokens | {r3['ms']}ms")
    word_count = len(r3['content'].split())
    print(f"     Word count: {word_count}")

    # Step 4: Lakshmi — Governance Review (OpenAI)
    print(f"\n[STEP 4] GOVERNANCE → Lakshmi (OpenAI/gpt-4o)")
    r4 = call_openai(
        "You are Lakshmi, ECO of Y-OS. Observe and audit. Never modify artifacts. Governance-quality analysis.",
        f"""Governance Review for CCR Runtime v1 specification.

Specification summary (first 1000 words):
{r3['content'][:1500]}

Verify compliance with Y-OS constitutional principles:

1. ARTIFACT PRIMACY — Does CCR treat artifacts as the source of truth?
2. CAPABILITY INDEPENDENCE — Is CCR independent of specific agents/models?
3. LINEAGE PRESERVATION — Does CCR preserve causal lineage?
4. CONTEXT CONTINUITY — Does CCR guarantee cognitive continuity across providers?
5. HUMAN OVERRIDE — Can humans override CCR decisions?

For each principle: COMPLIANT / NON-COMPLIANT / PARTIAL + justification.

Also identify:
- Any architectural risks
- Any missing governance hooks
- Recommendation: APPROVE / CONDITIONAL APPROVE / REJECT

Produce a formal Governance Review.""",
        max_tokens=1200
    )
    art4 = make_id()
    register_artifact(art4, "Governance Review", "Lakshmi", r4["provider"], r4["model"], art3, r4["content"])
    print(f"  ✅ {art4} | {r4['provider']}/{r4['model']} | {r4['prompt_tokens']}+{r4['completion_tokens']} tokens | {r4['ms']}ms")

    # Step 5: Saraswati — Learning Report + ADR Candidates (Anthropic)
    print(f"\n[STEP 5] LEARNING → Saraswati (Anthropic/claude-opus-4-5)")
    r5 = call_anthropic(
        "You are Saraswati, CODO of Y-OS. Extract organizational learning. Identify what deserves permanent preservation.",
        f"""Learning Report for MISSION-005 — Knowledge Compounding Validation.

Strategy Brief (Krishna):
{r1['content'][:500]}

Architecture Package (Brahma):
{r2['content'][:500]}

Governance Review (Lakshmi):
{r4['content'][:400]}

Analyze and answer explicitly:

1. WHAT NEW ARCHITECTURAL KNOWLEDGE WAS DISCOVERED?
   List the 3-5 most important architectural insights.

2. WHAT SHOULD BECOME A PERMANENT ADR?
   Identify specific decisions that deserve ADR status.
   For each: title, decision statement, rationale.

3. WHAT SHOULD BECOME CONSTITUTIONAL LAW?
   Identify any principle that should be elevated to the Y-OS Constitution.

4. WHAT REMAINS EXPERIMENTAL?
   What needs more validation before becoming permanent?

5. KNOWLEDGE COMPOUNDING ASSESSMENT
   Did this mission generate knowledge that will change future Y-OS design?
   Evidence: yes/no + specific examples.

Produce a Learning Report that itself becomes a permanent artifact.""",
        max_tokens=1500
    )
    art5 = make_id()
    register_artifact(art5, "Learning Report", "Saraswati", r5["provider"], r5["model"], art4, r5["content"])
    print(f"  ✅ {art5} | {r5['provider']}/{r5['model']} | {r5['prompt_tokens']}+{r5['completion_tokens']} tokens | {r5['ms']}ms")

    # Step 6: Ganesha — CEO Briefing + ADOPT/REVISE/REJECT (OpenAI)
    print(f"\n[STEP 6] REPORTING → Ganesha (OpenAI/gpt-4o)")
    r6 = call_openai(
        "You are Ganesha, COO of Y-OS. Dense CEO Briefing. No filler. Clear recommendation.",
        f"""CEO Briefing for MISSION-005 — Knowledge Compounding Validation.

Question: Should CCR Runtime v1 be adopted as the official Y-OS architecture?

Evidence:
- Strategy: {r1['content'][:300]}
- Architecture: {r2['content'][:300]}
- Governance: {r4['content'][:300]}
- Learning: {r5['content'][:300]}

Produce:
1. RECOMMENDATION: ADOPT / REVISE / REJECT
2. Justification (3-5 sentences)
3. If ADOPT: what must happen next?
4. If REVISE: what specifically must change?
5. ADR candidate title and one-sentence decision statement
6. Knowledge compounding verdict: did this mission generate permanent architectural knowledge?

Maximum 400 words.""",
        max_tokens=600
    )
    art6 = make_id()
    register_artifact(art6, "CEO Briefing", "Ganesha", r6["provider"], r6["model"], art5, r6["content"])
    print(f"  ✅ {art6} | {r6['provider']}/{r6['model']} | {r6['prompt_tokens']}+{r6['completion_tokens']} tokens | {r6['ms']}ms")

    # Save state
    (OUT_DIR / "registry.json").write_text(json.dumps(registry, indent=2))
    (OUT_DIR / "lineage.json").write_text(json.dumps(lineage, indent=2))

    print("\n" + "="*60)
    print(f"MISSION-005 COMPLETE")
    print(f"Artifacts: {len(registry)}")
    print(f"Lineage records: {len(lineage)}")
    print(f"Primary spec word count: {word_count}")
    print("="*60)

    return {
        "spec_id": art3, "spec": r3["content"],
        "learning_id": art5, "learning": r5["content"],
        "ceo_id": art6, "ceo": r6["content"],
        "governance_id": art4, "governance": r4["content"],
        "word_count": word_count
    }

if __name__ == "__main__":
    result = run_mission()
    # Print CEO recommendation
    print("\n--- CEO RECOMMENDATION ---")
    print(result["ceo"][:500])
