#!/usr/bin/env python3
"""
MISSION-014 — Generate 12 Concept Node files for Y-OS Cognitive Graph
"""

from pathlib import Path

CONCEPTS_DIR = Path("/home/ubuntu/yreg/concepts")
CONCEPTS_DIR.mkdir(exist_ok=True)

TODAY = "2026-06-13"

CONCEPTS = [
    {
        "slug": "artifact-primacy",
        "title": "Artifact Primacy",
        "domain": "constitution",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article I"],
        "adr_lineage": ["ADR-0021", "ADR-0024", "ADR-0034"],
        "mission_evidence": ["mission_001", "mission_002", "mission_006"],
        "definition": "Artifact Primacy is the foundational principle of Y-OS stating that all organizational knowledge, decisions, and outputs must be materialized as explicit, versioned, and traceable artifacts. No knowledge exists unless it is an artifact. No decision is valid unless it is documented. No capability is real unless it is encoded. This principle prevents knowledge from residing only in agent memory or session context, ensuring that every meaningful act of organizational intelligence produces a durable, auditable record.",
        "current_status": "FROZEN — Constitutional Article I. Cannot be amended without supermajority.",
        "implements": [],
        "depends_on": [],
        "supersedes": [],
        "tags": ["#constitution", "#yos", "#accepted"],
        "aliases": ["Artifact First", "Article I"],
    },
    {
        "slug": "preservation-principle",
        "title": "Preservation Principle",
        "domain": "constitution",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article II"],
        "adr_lineage": ["ADR-0024", "ADR-0040"],
        "mission_evidence": ["mission_013"],
        "definition": "The Preservation Principle mandates that no Y-OS artifact, once canonicalized, may be deleted, overwritten, or silently modified. All changes must be additive or versioned. Superseded artifacts are archived, not destroyed. This principle ensures that the organizational memory of Y-OS is cumulative and auditable — every version of every decision is recoverable. It is the foundation of Git-backed memory and the non-destructive constraint in all KGC operations.",
        "current_status": "FROZEN — Constitutional Article II. Enforced by KGC dry-run constraint and Git history.",
        "implements": [],
        "depends_on": ["[[Artifact_Primacy]]"],
        "supersedes": [],
        "tags": ["#constitution", "#yos", "#accepted"],
        "aliases": ["Preservation", "Article II", "Non-Destructive Principle"],
    },
    {
        "slug": "derivation-transparency",
        "title": "Derivation Transparency",
        "domain": "constitution",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article III"],
        "adr_lineage": ["ADR-0024", "ADR-0016", "ADR-0017"],
        "mission_evidence": ["mission_001", "mission_005"],
        "definition": "Derivation Transparency requires that every Y-OS artifact explicitly declares its origin — which mission produced it, which ADR governs it, which model generated it, which worker executed it. No artifact may exist without a traceable lineage. This principle enables full audit trails, prevents orphaned knowledge, and ensures that the provenance of every organizational decision is permanently visible. It is enforced through the YAML frontmatter schema (owner, worker, provider, model, derived_from fields).",
        "current_status": "FROZEN — Constitutional Article III. Enforced by frontmatter schema.",
        "implements": [],
        "depends_on": ["[[Artifact_Primacy]]"],
        "supersedes": [],
        "tags": ["#constitution", "#yos", "#accepted"],
        "aliases": ["Lineage Transparency", "Article III"],
    },
    {
        "slug": "human-override",
        "title": "Human Override",
        "domain": "constitution",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article IV"],
        "adr_lineage": ["ADR-0024", "ADR-0034"],
        "mission_evidence": ["mission_006", "mission_009"],
        "definition": "Human Override is the constitutional principle that no Y-OS agent, runtime, or automated process may take irreversible action without explicit human authorization. All destructive operations (deletion, force-push, financial transactions, external API writes) require prior human confirmation. This principle ensures that Y-OS remains a human-directed system — agents are operators, not principals. The human architect retains final authority over all organizational decisions.",
        "current_status": "FROZEN — Constitutional Article IV. Enforced by K7 rule (financial) and K2 rule (spending).",
        "implements": [],
        "depends_on": ["[[Governance_Before_Autonomy]]"],
        "supersedes": [],
        "tags": ["#constitution", "#yos", "#accepted"],
        "aliases": ["Human Authority", "Article IV", "Human-in-the-Loop"],
    },
    {
        "slug": "governance-before-autonomy",
        "title": "Governance Before Autonomy",
        "domain": "constitution",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article V"],
        "adr_lineage": ["ADR-0024", "ADR-0033", "ADR-0034", "ADR-0035"],
        "mission_evidence": ["mission_005c", "mission_006", "mission_009"],
        "definition": "Governance Before Autonomy mandates that every significant architectural decision in Y-OS must pass a Lakshmi governance review before adoption. No ADR is ACCEPTED without a governance verdict. No mission is PASSED without a risk score. Autonomy is earned through validated governance, not assumed. This principle prevents ungoverned capability expansion and ensures that Y-OS evolves through deliberate, auditable decisions rather than unchecked agent action.",
        "current_status": "FROZEN — Constitutional Article V. Enforced by Lakshmi review requirement in every mission.",
        "implements": [],
        "depends_on": ["[[Constitutional_Governance]]"],
        "supersedes": [],
        "tags": ["#constitution", "#governance", "#yos", "#accepted"],
        "aliases": ["Governance First", "Article V"],
    },
    {
        "slug": "ccr-runtime",
        "title": "CCR Runtime",
        "domain": "context",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article I", "Article III"],
        "adr_lineage": ["ADR-0029", "ADR-0030", "ADR-0037"],
        "mission_evidence": ["mission_005", "mission_005b", "mission_011"],
        "definition": "The CCR Runtime (Context Compiler Runtime) is the Y-OS component responsible for compiling, routing, and injecting execution context into mission cycles. It transforms raw session history and canonical memory into optimized context packs that maximize cognitive ROI per token. CCR v1 (ADR-0029) established the baseline compiler. CCR v1.1 (ADR-0030) added governance patch. CCR v2 (ADR-0037) introduced Mode B/D context routing with 140.9 ROI/1k tokens for Mode B (production default).",
        "current_status": "CCR v2 is the production default. Mode B = 623 tokens, ROI 140.9/1k.",
        "implements": ["[[Context_Pack]]", "[[Context_Router]]"],
        "depends_on": ["[[Session_Delta]]", "[[Canonical_Memory]]"],
        "supersedes": [],
        "tags": ["#context", "#ccr", "#runtime", "#yos", "#accepted"],
        "aliases": ["Context Compiler Runtime", "CCR", "Context Compiler"],
    },
    {
        "slug": "session-delta",
        "title": "Session Delta",
        "domain": "memory",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article I", "Article II"],
        "adr_lineage": ["ADR-0038"],
        "mission_evidence": ["mission_012"],
        "definition": "Session Delta is the Y-OS mechanism for computing the incremental knowledge contribution of a single session relative to the existing canonical memory. Rather than re-processing full session history, the Session Delta Engine (ADR-0038) identifies what is genuinely new — new decisions, new artifacts, new relationships — and produces a minimal, high-signal delta artifact. This delta is the input to the Living Memory Pipeline's summarize and archive stages.",
        "current_status": "Designed (ADR-0038). Implementation pending MISSION-015.",
        "implements": ["[[Living_Memory]]"],
        "depends_on": ["[[CCR_Runtime]]"],
        "supersedes": [],
        "tags": ["#memory", "#session-delta", "#yos", "#accepted"],
        "aliases": ["Delta Engine", "Session Delta Engine"],
    },
    {
        "slug": "living-memory",
        "title": "Living Memory",
        "domain": "memory",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article I", "Article II", "Article III"],
        "adr_lineage": ["ADR-0039"],
        "mission_evidence": ["mission_012b"],
        "definition": "Living Memory is the Y-OS concept of organizational memory as a continuously evolving, self-compacting knowledge graph rather than a static archive. Unlike traditional document storage, Living Memory is alive — it grows with each session, compresses redundancy, surfaces canonical knowledge, and feeds directly into execution context. The Living Memory Pipeline (ADR-0039) defines the 8-stage lifecycle: Capture → Compress → Delta → Summarize → Archive → Canonicalize → Compile → Inject.",
        "current_status": "Doctrine defined (ADR-0039). Pipeline implementation pending MISSION-015.",
        "implements": [],
        "depends_on": ["[[Session_Delta]]", "[[CCR_Runtime]]", "[[Canonical_Memory]]"],
        "supersedes": [],
        "tags": ["#memory", "#living-memory", "#yos", "#accepted"],
        "aliases": ["LMP", "Living Memory Pipeline", "Organizational Memory"],
    },
    {
        "slug": "context-pack",
        "title": "Context Pack",
        "domain": "context",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article I"],
        "adr_lineage": ["ADR-0036", "ADR-0037"],
        "mission_evidence": ["mission_010", "mission_011"],
        "definition": "A Context Pack is a structured, pre-compiled artifact that contains the minimal sufficient context for executing a Y-OS mission. It replaces raw session history as the primary context injection mechanism. A Context Pack contains: current mission definition, relevant ADR summaries, active worker registry, constitutional constraints, and session delta from previous missions. Mode B (Context Pack Only) achieves 140.9 ROI/1k tokens — the highest efficiency of all context modes.",
        "current_status": "Production default (Mode B). Schema defined in Context_Pack_Schema_v1.",
        "implements": [],
        "depends_on": ["[[CCR_Runtime]]"],
        "supersedes": [],
        "tags": ["#context", "#ccr", "#yos", "#accepted"],
        "aliases": ["Context Pack v1", "Mode B Context"],
    },
    {
        "slug": "context-router",
        "title": "Context Router",
        "domain": "context",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article I", "Article III"],
        "adr_lineage": ["ADR-0037"],
        "mission_evidence": ["mission_011"],
        "definition": "The Context Router is the CCR v2 component that selects the appropriate context mode (A through F) based on mission type, token budget, and constitutional requirements. Mode B (Context Pack Only, 623 tokens) is the production default for standard missions. Mode D (Context Pack + Canonical Memory, 1100 tokens) is used for constitutional work. The Context Router enforces the principle that context selection is a governance decision, not an ad-hoc choice.",
        "current_status": "Designed (ADR-0037). Mode B in production. Mode D for constitutional work.",
        "implements": ["[[CCR_Runtime]]"],
        "depends_on": ["[[Context_Pack]]", "[[Canonical_Memory]]"],
        "supersedes": [],
        "tags": ["#context", "#ccr", "#yos", "#accepted"],
        "aliases": ["Mode Router", "CCR v2 Router"],
    },
    {
        "slug": "constitutional-governance",
        "title": "Constitutional Governance",
        "domain": "governance",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article V"],
        "adr_lineage": ["ADR-0033", "ADR-0034", "ADR-0035"],
        "mission_evidence": ["mission_005c", "mission_006", "mission_009"],
        "definition": "Constitutional Governance is the Y-OS framework that makes the Y-OS Constitution operationally enforceable — not merely aspirational. It defines how Lakshmi (CLO/Risk) evaluates every architectural decision against the 5 constitutional articles, assigns a risk score (0–100), and produces a deterministic verdict (APPROVE / APPROVE_WITH_WARNING / REJECT). A score ≤ 55 with zero blocking reasons is required for ACCEPT. This framework prevents governance from being a rubber stamp and ensures that constitutional compliance is measurable.",
        "current_status": "Operational. Lakshmi governance review required for all ADRs.",
        "implements": ["[[Governance_Before_Autonomy]]"],
        "depends_on": ["[[Governance_Determinism]]"],
        "supersedes": [],
        "tags": ["#governance", "#constitution", "#yos", "#accepted"],
        "aliases": ["Executable Constitution", "Constitutional Compliance"],
    },
    {
        "slug": "governance-determinism",
        "title": "Governance Determinism",
        "domain": "governance",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article V"],
        "adr_lineage": ["ADR-0033"],
        "mission_evidence": ["mission_005c"],
        "definition": "Governance Determinism is the principle that Y-OS governance decisions must be deterministic — given the same inputs (ADR content, constitutional articles, risk criteria), the governance verdict must be reproducible and consistent. This eliminates subjective or context-dependent governance and makes Lakshmi's review process auditable. The Governance Determinism Framework (ADR-0033) defines the scoring rubric, verdict thresholds, and blocking condition taxonomy that make governance outcomes predictable and verifiable.",
        "current_status": "Operational. Scoring rubric defined in Governance_Determinism_Framework_v1.",
        "implements": ["[[Constitutional_Governance]]"],
        "depends_on": [],
        "supersedes": [],
        "tags": ["#governance", "#yos", "#accepted"],
        "aliases": ["Deterministic Governance", "ADR-0033"],
    },
]

def generate_concept_node(c: dict) -> str:
    grounding = "\n".join(f"- {a}" for a in c["constitutional_grounding"])
    lineage = "\n".join(f"- [[{a}]]" for a in c["adr_lineage"])
    evidence = "\n".join(f"- [[{m}]]" for m in c["mission_evidence"])
    implements = "\n".join(f"- {i}" for i in c["implements"]) if c["implements"] else "- (none)"
    depends = "\n".join(f"- {d}" for d in c["depends_on"]) if c["depends_on"] else "- (none)"

    # YAML frontmatter
    fm_implements = str(c["implements"]).replace("'", '"') if c["implements"] else "[]"
    fm_depends = str(c["depends_on"]).replace("'", '"') if c["depends_on"] else "[]"
    fm_tags = "\n".join(f"  - '{t}'" for t in c["tags"])
    fm_aliases = "\n".join(f"  - {a}" for a in c["aliases"])
    fm_grounding = "\n".join(f"  - '{a}'" for a in c["constitutional_grounding"])
    fm_lineage = "\n".join(f"  - '[[{a}]]'" for a in c["adr_lineage"])
    fm_evidence = "\n".join(f"  - '[[{m}]]'" for m in c["mission_evidence"])

    return f"""---
id: yos-concept-{c["slug"]}
title: {c["title"]}
type: concept
status: {c["status"]}
domain: {c["domain"]}
date: '{TODAY}'
owner: Brahma
parent: '[[10_Concepts_MOC]]'
constitutional_grounding:
{fm_grounding}
adr_lineage:
{fm_lineage}
mission_evidence:
{fm_evidence}
implements: {fm_implements}
depends_on: {fm_depends}
tags:
{fm_tags}
aliases:
{fm_aliases}
source_branch: y-os-doctrine
canonical: true
---

# {c["title"]}

**Type:** Concept  
**Domain:** {c["domain"].title()}  
**Status:** {c["status"]}  
**Constitutional Grounding:** {", ".join(c["constitutional_grounding"])}

---

## Definition

{c["definition"]}

---

## Constitutional Grounding

{grounding}

---

## ADR Lineage

{lineage}

---

## Mission Evidence

{evidence}

---

## Relationships

**Implements:**
{implements}

**Depends on:**
{depends}

---

## Current Status

{c["current_status"]}

---

## Navigation

- [[10_Concepts_MOC]] — All Y-OS Concepts
- [[01_Constitution_MOC]] — Constitutional Layer
- [[00_Y-OS_Home]] — Home
"""

if __name__ == "__main__":
    generated = []
    for c in CONCEPTS:
        filename = f"{c['title'].replace(' ', '_')}.md"
        path = CONCEPTS_DIR / filename
        content = generate_concept_node(c)
        path.write_text(content, encoding="utf-8")
        generated.append(filename)
        print(f"  ✅ {filename}")

    print(f"\nGenerated {len(generated)} concept nodes in {CONCEPTS_DIR}")
