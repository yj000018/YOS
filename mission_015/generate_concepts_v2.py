#!/usr/bin/env python3
"""
MISSION-015 — Expand concept nodes from 12 to 30+
Generates new concept files in concepts/ (skips existing ones)
"""

from pathlib import Path

CONCEPTS_DIR = Path("/home/ubuntu/yreg/concepts")
CONCEPTS_DIR.mkdir(exist_ok=True)
TODAY = "2026-06-14"

NEW_CONCEPTS = [
    # ── Constitution / Governance (additional) ──────────────────────────────
    {
        "slug": "constitutional-core",
        "title": "Constitutional Core",
        "domain": "constitution",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article I", "Article II", "Article III", "Article IV", "Article V"],
        "adr_lineage": ["ADR-0024", "ADR-0034"],
        "mission_evidence": ["mission_006", "mission_009"],
        "definition": "The Constitutional Core is the minimal set of invariant principles that define Y-OS identity and cannot be changed without a supermajority constitutional amendment. It comprises the five Articles of the Y-OS Constitution: Artifact Primacy, Preservation Principle, Derivation Transparency, Human Override, and Governance Before Autonomy. The Constitutional Core is the single source of truth for all architectural decisions and the ultimate constraint on all agent behavior.",
        "current_status": "FROZEN. Encoded in Y-OS_Constitution_v1.md and ADR-0034.",
        "implements": [], "depends_on": [], "supersedes": [],
        "tags": ["#constitution", "#yos", "#accepted"],
        "aliases": ["Constitutional Foundation", "Y-OS Constitution"],
    },
    {
        "slug": "replacement-test",
        "title": "Replacement Test",
        "domain": "constitution",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article I", "Article III"],
        "adr_lineage": ["ADR-0022"],
        "mission_evidence": ["mission_007"],
        "definition": "The Replacement Test is a Y-OS constitutional evaluation criterion that asks: if the current agent, worker, or model were replaced by a different one, would the system still produce the same outputs given the same inputs? If yes, the system passes the Replacement Test — its behavior is encoded in artifacts, not in agent memory. If no, the system fails — it has hidden dependencies on specific agent state. The Replacement Test enforces Artifact Primacy and Derivation Transparency.",
        "current_status": "Operational. Applied in mission governance reviews.",
        "implements": ["[[Artifact_Primacy]]"], "depends_on": [], "supersedes": [],
        "tags": ["#constitution", "#governance", "#yos", "#accepted"],
        "aliases": ["Replaceability Test", "Agent Independence Test"],
    },
    {
        "slug": "amendment-procedure",
        "title": "Amendment Procedure",
        "domain": "constitution",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article V"],
        "adr_lineage": ["ADR-0024", "ADR-0034"],
        "mission_evidence": ["mission_006"],
        "definition": "The Amendment Procedure defines the formal process for modifying the Y-OS Constitution. Any amendment requires: (1) a formal ADR proposing the change, (2) a Lakshmi governance review with risk score ≤ 35, (3) explicit CEO authorization (Human Override), and (4) a supermajority decision. No constitutional article may be amended unilaterally by any agent. This procedure ensures that the Constitutional Core remains stable while allowing deliberate evolution.",
        "current_status": "Defined but not yet invoked. Constitution v1 is the current canonical version.",
        "implements": ["[[Governance_Before_Autonomy]]"], "depends_on": ["[[Constitutional_Core]]"], "supersedes": [],
        "tags": ["#constitution", "#governance", "#yos", "#accepted"],
        "aliases": ["Constitutional Amendment", "Amendment Protocol"],
    },
    {
        "slug": "lakshmi-governance",
        "title": "Lakshmi Governance",
        "domain": "governance",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article V"],
        "adr_lineage": ["ADR-0033", "ADR-0035"],
        "mission_evidence": ["mission_005c", "mission_009"],
        "definition": "Lakshmi Governance refers to the role and function of the Lakshmi worker (CLO/Risk) in the Y-OS governance system. Lakshmi evaluates every ADR and mission against the five constitutional articles, assigns a risk score (0–100), and produces a deterministic verdict: APPROVE (score ≤ 35), APPROVE_WITH_WARNING (36–55), or REJECT (> 55 or blocking condition). Lakshmi is the operational implementation of Constitutional Governance and Governance Determinism.",
        "current_status": "Operational. Required for all ADR acceptance.",
        "implements": ["[[Constitutional_Governance]]", "[[Governance_Determinism]]"], "depends_on": [], "supersedes": [],
        "tags": ["#governance", "#yos", "#accepted"],
        "aliases": ["Lakshmi", "CLO", "Risk Officer", "Governance Worker"],
    },
    # ── Runtime ──────────────────────────────────────────────────────────────
    {
        "slug": "y-orc",
        "title": "Y-ORC",
        "domain": "runtime",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article I", "Article III"],
        "adr_lineage": ["ADR-0025"],
        "mission_evidence": ["mission_005"],
        "definition": "Y-ORC (Y-OS Orchestration Runtime Core) is the central orchestration engine of Y-OS. It receives mission definitions, routes tasks to appropriate workers (ART, CRT, CCR), manages execution state, and ensures that all outputs are materialized as artifacts. Y-ORC is the operational heart of the Y-OS runtime — it does not execute tasks directly but coordinates the workers that do. Y-ORC enforces Artifact Primacy by ensuring every worker output is captured.",
        "current_status": "Implemented in yorc_runtime_v1.py.",
        "implements": [], "depends_on": ["[[ART]]", "[[CRT]]", "[[CCR_Runtime]]"], "supersedes": [],
        "tags": ["#runtime", "#yos", "#accepted"],
        "aliases": ["Y-OS Orchestration Runtime Core", "Orchestrator"],
    },
    {
        "slug": "art",
        "title": "ART",
        "domain": "runtime",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article I"],
        "adr_lineage": ["ADR-0026"],
        "mission_evidence": ["mission_005"],
        "definition": "ART (Artifact Runtime) is the Y-OS worker responsible for creating, versioning, and storing artifacts. Every time a Y-OS process produces an output — a document, a report, a code file, a schema — ART captures it, assigns a canonical ID, and stores it in the Artifact Registry. ART is the operational implementation of Artifact Primacy. Without ART, knowledge would remain in agent memory rather than in durable, versioned artifacts.",
        "current_status": "Implemented in art_runtime_v1.py.",
        "implements": ["[[Artifact_Primacy]]"], "depends_on": ["[[Y-ORC]]"], "supersedes": [],
        "tags": ["#runtime", "#yos", "#accepted"],
        "aliases": ["Artifact Runtime", "Artifact Worker"],
    },
    {
        "slug": "crt",
        "title": "CRT",
        "domain": "runtime",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article I", "Article III"],
        "adr_lineage": ["ADR-0028"],
        "mission_evidence": ["mission_005"],
        "definition": "CRT (Context Runtime) is the Y-OS worker responsible for managing execution context. CRT reads the current context pack, injects it into the active mission, and updates the context state after each execution cycle. CRT works in conjunction with CCR (Context Compiler Runtime) — CCR compiles the context pack, CRT injects it. CRT ensures that every mission execution has access to the right context at the right time.",
        "current_status": "Implemented in crt_runtime_v1.py.",
        "implements": ["[[Context_Pack]]"], "depends_on": ["[[CCR_Runtime]]", "[[Y-ORC]]"], "supersedes": [],
        "tags": ["#runtime", "#yos", "#accepted"],
        "aliases": ["Context Runtime", "Context Worker"],
    },
    {
        "slug": "context-compiler",
        "title": "Context Compiler",
        "domain": "context",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article I"],
        "adr_lineage": ["ADR-0029", "ADR-0030", "ADR-0037"],
        "mission_evidence": ["mission_005", "mission_011"],
        "definition": "The Context Compiler is the core algorithm within CCR Runtime that transforms raw session history, canonical memory, and mission definitions into an optimized context pack. It applies compression, deduplication, and relevance scoring to maximize cognitive ROI per token. The Context Compiler is the computational heart of CCR — it is what makes Mode B (Context Pack Only) achieve 140.9 ROI/1k tokens.",
        "current_status": "Implemented in context_compiler_v1.py.",
        "implements": ["[[CCR_Runtime]]"], "depends_on": ["[[Context_Pack]]"], "supersedes": [],
        "tags": ["#context", "#ccr", "#runtime", "#yos", "#accepted"],
        "aliases": ["CCR Compiler", "Context Compilation Algorithm"],
    },
    {
        "slug": "provider-adapter",
        "title": "Provider Adapter",
        "domain": "runtime",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article I", "Article III"],
        "adr_lineage": ["ADR-0027"],
        "mission_evidence": ["mission_005"],
        "definition": "The Provider Adapter is the Y-OS abstraction layer that normalizes access to external LLM providers (Anthropic, OpenAI, Gemini, Grok). It translates Y-OS execution requests into provider-specific API calls and normalizes responses back into Y-OS artifact format. The Provider Adapter enforces Derivation Transparency by recording which provider and model generated each artifact. It enables provider-agnostic mission execution.",
        "current_status": "Defined in ADR-0027. Implemented in provider registry.",
        "implements": [], "depends_on": ["[[Y-ORC]]"], "supersedes": [],
        "tags": ["#runtime", "#yos", "#accepted"],
        "aliases": ["Provider Layer", "LLM Adapter", "Model Adapter"],
    },
    {
        "slug": "worker-registry",
        "title": "Worker Registry",
        "domain": "runtime",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article I", "Article III"],
        "adr_lineage": ["ADR-0025"],
        "mission_evidence": ["mission_005"],
        "definition": "The Worker Registry is the canonical catalog of all Y-OS workers — their names, roles, capabilities, and current status. Workers include: CEO, Krishna, Brahma, Ganesha, Hanuman, Lakshmi, Saraswati. The Worker Registry enforces Derivation Transparency by ensuring that every artifact records which worker produced it. It also enables Y-ORC to route tasks to the correct worker based on capability matching.",
        "current_status": "Defined in worker_registry.json.",
        "implements": [], "depends_on": ["[[Y-ORC]]"], "supersedes": [],
        "tags": ["#runtime", "#yos", "#accepted"],
        "aliases": ["Worker Catalog", "Agent Registry"],
    },
    {
        "slug": "model-registry",
        "title": "Model Registry",
        "domain": "runtime",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article III"],
        "adr_lineage": ["ADR-0027"],
        "mission_evidence": ["mission_005"],
        "definition": "The Model Registry is the canonical catalog of all LLM models available to Y-OS workers — their provider, version, capabilities, cost, and routing rules. It enables the Provider Adapter to select the optimal model for each task based on type (reasoning, coding, vision, long-context) and budget constraints. The Model Registry enforces Derivation Transparency by recording which model generated each artifact.",
        "current_status": "Defined in model_registry.json.",
        "implements": [], "depends_on": ["[[Provider_Adapter]]"], "supersedes": [],
        "tags": ["#runtime", "#yos", "#accepted"],
        "aliases": ["LLM Registry", "Model Catalog"],
    },
    {
        "slug": "artifact-registry",
        "title": "Artifact Registry",
        "domain": "runtime",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article I", "Article II"],
        "adr_lineage": ["ADR-0016", "ADR-0017"],
        "mission_evidence": ["mission_001", "mission_002"],
        "definition": "The Artifact Registry is the canonical index of all Y-OS artifacts — their IDs, types, versions, owners, and storage locations. It is the operational implementation of Artifact Primacy. Every artifact created by ART is registered here. The Artifact Registry enables discovery, versioning, and retrieval of any Y-OS artifact across sessions. It is the foundation of the Living Memory system.",
        "current_status": "Defined in ADR-0016/0017. Implemented as YAML frontmatter + Git.",
        "implements": ["[[Artifact_Primacy]]"], "depends_on": ["[[ART]]"], "supersedes": [],
        "tags": ["#runtime", "#artifact", "#yos", "#accepted"],
        "aliases": ["Artifact Index", "Artifact Catalog"],
    },
    # ── Memory ───────────────────────────────────────────────────────────────
    {
        "slug": "canonical-memory",
        "title": "Canonical Memory",
        "domain": "memory",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article I", "Article II"],
        "adr_lineage": ["ADR-0039"],
        "mission_evidence": ["mission_012b"],
        "definition": "Canonical Memory is the distilled, deduplicated, and validated subset of Y-OS organizational memory that has been canonicalized through the Living Memory Pipeline. Unlike raw session history or intermediate summaries, Canonical Memory contains only knowledge that has passed the canonicalization stage — it is stable, authoritative, and directly injectable into mission context. Canonical Memory is the output of the 'canonicalize' stage of the LMP.",
        "current_status": "Doctrine defined (ADR-0039). Implementation pending MISSION-016.",
        "implements": ["[[Living_Memory]]"], "depends_on": ["[[Session_Delta]]"], "supersedes": [],
        "tags": ["#memory", "#yos", "#accepted"],
        "aliases": ["Canonical Knowledge", "Distilled Memory"],
    },
    {
        "slug": "archive-reference",
        "title": "Archive Reference",
        "domain": "memory",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article II"],
        "adr_lineage": ["ADR-0039"],
        "mission_evidence": ["mission_012b"],
        "definition": "An Archive Reference is a pointer in the Y-OS memory system to a canonicalized artifact that has been archived but is no longer in active context. Archive References enable the Living Memory Pipeline to maintain a complete organizational memory without loading all historical artifacts into active context. They are the mechanism by which Y-OS achieves infinite memory with finite context.",
        "current_status": "Doctrine defined (ADR-0039).",
        "implements": ["[[Living_Memory]]"], "depends_on": ["[[Canonical_Memory]]"], "supersedes": [],
        "tags": ["#memory", "#yos", "#accepted"],
        "aliases": ["Archive Pointer", "Memory Reference"],
    },
    {
        "slug": "knowledge-graph-compiler",
        "title": "Knowledge Graph Compiler",
        "domain": "memory",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article I", "Article III"],
        "adr_lineage": ["ADR-0040", "ADR-0041", "ADR-0042"],
        "mission_evidence": ["mission_013", "mission_013b", "mission_014", "mission_015"],
        "definition": "The Knowledge Graph Compiler (KGC) is the Y-OS tool that transforms the Markdown artifact corpus into an Obsidian-native knowledge graph. KGC v1 (ADR-0040) added YAML frontmatter, wikilinks, and MOCs. KGC v2 (ADR-0042) adds semantic relationship inference, concept nodes, Canvas visual maps, and Dataview dashboards. The KGC is the operational bridge between the artifact corpus and the cognitive navigation interface.",
        "current_status": "KGC v2 operational (MISSION-015). kg_compiler_v2.py deployed.",
        "implements": ["[[Cognitive_Graph]]"], "depends_on": ["[[Artifact_Registry]]"], "supersedes": [],
        "tags": ["#memory", "#artifact", "#yos", "#accepted"],
        "aliases": ["KGC", "KGC v1", "KGC v2", "Graph Compiler"],
    },
    {
        "slug": "cognitive-graph",
        "title": "Cognitive Graph",
        "domain": "memory",
        "status": "EVOLVING",
        "constitutional_grounding": ["Article I", "Article III"],
        "adr_lineage": ["ADR-0041", "ADR-0042"],
        "mission_evidence": ["mission_014", "mission_015"],
        "definition": "The Cognitive Graph is the target state of the Y-OS knowledge architecture — a graph where concepts are first-class entities, relationships are typed and traversable, and navigation is intent-based rather than filename-based. A human should be able to ask 'What created CCR Runtime?' and receive a traversable answer through the graph. The Cognitive Graph is the third stage of the document→concept→cognitive evolution model.",
        "current_status": "Stage 2 (Concept Graph) complete. Stage 3 (Cognitive Graph) in progress.",
        "implements": [], "depends_on": ["[[Knowledge_Graph_Compiler]]"], "supersedes": [],
        "tags": ["#memory", "#yos", "#accepted"],
        "aliases": ["Cognitive Knowledge Graph", "Y-OS Cognitive Graph"],
    },
    {
        "slug": "organizational-digital-twin",
        "title": "Organizational Digital Twin",
        "domain": "memory",
        "status": "EVOLVING",
        "constitutional_grounding": ["Article I", "Article II", "Article III"],
        "adr_lineage": ["ADR-0041", "ADR-0042"],
        "mission_evidence": ["mission_014", "mission_015"],
        "definition": "The Organizational Digital Twin is the complete, navigable, visual representation of Y-OS as a living system — its constitution, governance, workers, runtime, memory, missions, and artifacts — encoded as a graph that can be explored, queried, and updated. It is the highest-level abstraction of the Y-OS knowledge architecture. The YOS_Organizational_Digital_Twin.canvas is the entry point for drill-down navigation into the entire Y-OS system.",
        "current_status": "First version generated in MISSION-015 as Canvas map.",
        "implements": ["[[Cognitive_Graph]]"], "depends_on": ["[[Knowledge_Graph_Compiler]]"], "supersedes": [],
        "tags": ["#memory", "#yos", "#accepted"],
        "aliases": ["Digital Twin", "Y-OS System Map", "ODT"],
    },
    # ── Organization (Workers) ───────────────────────────────────────────────
    {
        "slug": "ganesha",
        "title": "Ganesha",
        "domain": "organization",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article IV", "Article V"],
        "adr_lineage": ["ADR-0024"],
        "mission_evidence": ["mission_001"],
        "definition": "Ganesha is the Y-OS CEO worker — the final decision authority for all architectural and organizational decisions. Ganesha synthesizes inputs from all other workers (Brahma, Lakshmi, Saraswati, Hanuman) and produces CEO Recommendations that either ADOPT or REJECT proposed ADRs. Ganesha embodies Human Override — no architectural decision is final without Ganesha's explicit authorization.",
        "current_status": "Operational. CEO Recommendations required for all ADR acceptance.",
        "implements": ["[[Human_Override]]"], "depends_on": [], "supersedes": [],
        "tags": ["#organization", "#yos", "#accepted"],
        "aliases": ["CEO", "Chief Executive Officer", "Y-OS CEO"],
    },
    {
        "slug": "brahma",
        "title": "Brahma",
        "domain": "organization",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article I", "Article III"],
        "adr_lineage": ["ADR-0024"],
        "mission_evidence": ["mission_001"],
        "definition": "Brahma is the Y-OS CTO worker — responsible for architectural design, ADR authoring, and technical decision-making. Brahma proposes ADRs, designs system components, and ensures that all technical decisions are grounded in the constitutional principles. Brahma is the primary author of the Y-OS architecture and the owner of the ADR register.",
        "current_status": "Operational. Primary ADR author.",
        "implements": ["[[Derivation_Transparency]]"], "depends_on": [], "supersedes": [],
        "tags": ["#organization", "#yos", "#accepted"],
        "aliases": ["CTO", "Chief Technology Officer", "Architecture Worker"],
    },
    {
        "slug": "lakshmi",
        "title": "Lakshmi",
        "domain": "organization",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article V"],
        "adr_lineage": ["ADR-0033", "ADR-0035"],
        "mission_evidence": ["mission_005c"],
        "definition": "Lakshmi is the Y-OS CLO (Chief Legal Officer) / Risk worker — responsible for governance reviews, risk scoring, and constitutional compliance verification. Lakshmi evaluates every ADR against the five constitutional articles and produces a deterministic verdict. Lakshmi is the operational implementation of Governance Before Autonomy and Governance Determinism.",
        "current_status": "Operational. Governance review required for all ADRs.",
        "implements": ["[[Lakshmi_Governance]]"], "depends_on": [], "supersedes": [],
        "tags": ["#organization", "#governance", "#yos", "#accepted"],
        "aliases": ["CLO", "Risk Officer", "Governance Worker", "Lakshmi Worker"],
    },
    {
        "slug": "saraswati",
        "title": "Saraswati",
        "domain": "organization",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article I"],
        "adr_lineage": ["ADR-0024"],
        "mission_evidence": ["mission_001"],
        "definition": "Saraswati is the Y-OS CLO (Chief Learning Officer) worker — responsible for learning reports, knowledge synthesis, and organizational intelligence. Saraswati analyzes mission outcomes, identifies patterns, and produces learning artifacts that feed into the Living Memory Pipeline. Saraswati is the primary producer of learning_report type artifacts.",
        "current_status": "Operational. Learning reports generated after each mission.",
        "implements": ["[[Living_Memory]]"], "depends_on": [], "supersedes": [],
        "tags": ["#organization", "#yos", "#accepted"],
        "aliases": ["CLO", "Chief Learning Officer", "Learning Worker"],
    },
    {
        "slug": "hanuman",
        "title": "Hanuman",
        "domain": "organization",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article I"],
        "adr_lineage": ["ADR-0024"],
        "mission_evidence": ["mission_001"],
        "definition": "Hanuman is the Y-OS COO (Chief Operations Officer) worker — responsible for execution, implementation, and operational delivery. Hanuman takes architectural decisions (ADRs) and turns them into working code, deployed systems, and operational artifacts. Hanuman is the bridge between design (Brahma) and reality (running systems).",
        "current_status": "Operational. Primary implementation worker.",
        "implements": [], "depends_on": ["[[Y-ORC]]"], "supersedes": [],
        "tags": ["#organization", "#yos", "#accepted"],
        "aliases": ["COO", "Chief Operations Officer", "Execution Worker"],
    },
    {
        "slug": "krishna",
        "title": "Krishna",
        "domain": "organization",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article I", "Article IV"],
        "adr_lineage": ["ADR-0024"],
        "mission_evidence": ["mission_001"],
        "definition": "Krishna is the Y-OS CPO (Chief Product Officer) worker — responsible for product vision, user experience, and strategic alignment. Krishna translates organizational goals into mission definitions and ensures that Y-OS capabilities serve the broader vision of the Architect of New Society. Krishna is the voice of the user in the Y-OS worker system.",
        "current_status": "Operational. Mission definition and product strategy.",
        "implements": [], "depends_on": [], "supersedes": [],
        "tags": ["#organization", "#yos", "#accepted"],
        "aliases": ["CPO", "Chief Product Officer", "Product Worker"],
    },
    # ── Technical Infrastructure ─────────────────────────────────────────────
    {
        "slug": "git-backed-memory",
        "title": "Git-backed Memory",
        "domain": "technical",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article I", "Article II"],
        "adr_lineage": ["ADR-0040"],
        "mission_evidence": ["mission_013"],
        "definition": "Git-backed Memory is the Y-OS approach to persistent organizational memory — all artifacts are stored in a Git repository (yj000018/YOS, branch y-os-doctrine), providing versioning, audit trails, and recovery capabilities. Git serves as the durable, distributed backup for the Obsidian vault. Every commit is a snapshot of organizational knowledge at a point in time. Git-backed Memory enforces the Preservation Principle by making all changes reversible.",
        "current_status": "Operational. 71+ commits on y-os-doctrine.",
        "implements": ["[[Preservation_Principle]]"], "depends_on": [], "supersedes": [],
        "tags": ["#technical", "#yos", "#accepted"],
        "aliases": ["Git Memory", "Git Repository", "y-os-doctrine"],
    },
    {
        "slug": "obsidian-vault",
        "title": "Obsidian Vault",
        "domain": "technical",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article I"],
        "adr_lineage": ["ADR-0040", "ADR-0041", "ADR-0042"],
        "mission_evidence": ["mission_013", "mission_014", "mission_015"],
        "definition": "The Obsidian Vault is the primary human-facing interface for the Y-OS knowledge graph. It is a local clone of the y-os-doctrine branch, opened in Obsidian, providing graph view, wikilink navigation, Canvas maps, and Dataview queries. The Obsidian Vault is where the Cognitive Graph becomes navigable by a human. It is not the source of truth (Git is) but the cognitive interface to it.",
        "current_status": "Operational. Clone: git clone https://github.com/yj000018/YOS.git --branch y-os-doctrine",
        "implements": ["[[Cognitive_Graph]]"], "depends_on": ["[[Git-backed_Memory]]"], "supersedes": [],
        "tags": ["#technical", "#yos", "#accepted"],
        "aliases": ["Obsidian", "Knowledge Vault", "Y-OS Vault"],
    },
    {
        "slug": "markdown-corpus",
        "title": "Markdown Corpus",
        "domain": "technical",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article I", "Article II"],
        "adr_lineage": ["ADR-0040"],
        "mission_evidence": ["mission_013"],
        "definition": "The Markdown Corpus is the complete collection of Y-OS Markdown artifacts — currently 330+ files — that form the document layer of the Cognitive Graph. Each file is a Y-OS artifact with YAML frontmatter, typed relationships, and wikilinks. The Markdown Corpus is the raw material that KGC transforms into a knowledge graph. It is stored in Git and navigated through Obsidian.",
        "current_status": "330+ files, 100% frontmatter, 1620+ semantic edges (KGC v2).",
        "implements": [], "depends_on": ["[[Artifact_Registry]]"], "supersedes": [],
        "tags": ["#technical", "#yos", "#accepted"],
        "aliases": ["Markdown Archive", "Y-OS Corpus", "Document Corpus"],
    },
    {
        "slug": "github-remote",
        "title": "GitHub Remote",
        "domain": "technical",
        "status": "CANONICAL",
        "constitutional_grounding": ["Article II"],
        "adr_lineage": ["ADR-0040"],
        "mission_evidence": ["mission_013"],
        "definition": "The GitHub Remote is the authoritative cloud backup of the Y-OS Markdown Corpus — repository yj000018/YOS, branch y-os-doctrine. It provides distributed storage, SSH-authenticated access, and public visibility for the Y-OS doctrine corpus. The GitHub Remote is the recovery point if the local sandbox is lost. It is the external persistence layer that makes Y-OS memory durable across sandbox recreations.",
        "current_status": "Operational. SSH auth via y_os_github key. 71+ commits pushed.",
        "implements": ["[[Preservation_Principle]]", "[[Git-backed_Memory]]"], "depends_on": [], "supersedes": [],
        "tags": ["#technical", "#yos", "#accepted"],
        "aliases": ["GitHub", "yj000018/YOS", "Remote Repository"],
    },
]

def generate_concept_node(c: dict) -> str:
    fm_tags = "\n".join(f"  - '{t}'" for t in c["tags"])
    fm_aliases = "\n".join(f"  - {a}" for a in c["aliases"])
    fm_grounding = "\n".join(f"  - '{a}'" for a in c["constitutional_grounding"])
    fm_lineage = "\n".join(f"  - '[[{a}]]'" for a in c["adr_lineage"])
    fm_evidence = "\n".join(f"  - '[[{m}]]'" for m in c["mission_evidence"])
    fm_implements = str(c["implements"]).replace("'", '"') if c["implements"] else "[]"
    fm_depends = str(c["depends_on"]).replace("'", '"') if c["depends_on"] else "[]"

    grounding = "\n".join(f"- {a}" for a in c["constitutional_grounding"])
    lineage = "\n".join(f"- [[{a}]]" for a in c["adr_lineage"])
    evidence = "\n".join(f"- [[{m}]]" for m in c["mission_evidence"])
    implements = "\n".join(f"- {i}" for i in c["implements"]) if c["implements"] else "- (none)"
    depends = "\n".join(f"- {d}" for d in c["depends_on"]) if c["depends_on"] else "- (none)"

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
- [[00_Y-OS_Home]] — Home
"""

if __name__ == "__main__":
    generated = []
    skipped = []
    for c in NEW_CONCEPTS:
        filename = f"{c['title'].replace(' ', '_').replace('-', '_')}.md"
        path = CONCEPTS_DIR / filename
        if path.exists():
            skipped.append(filename)
            continue
        content = generate_concept_node(c)
        path.write_text(content, encoding="utf-8")
        generated.append(filename)
        print(f"  ✅ {filename}")

    if skipped:
        print(f"\nSkipped (already exist): {len(skipped)}")
        for s in skipped:
            print(f"  ⏭️  {s}")
    print(f"\nGenerated {len(generated)} new concept nodes")
    print(f"Total in concepts/: {len(list(CONCEPTS_DIR.glob('*.md')))}")
