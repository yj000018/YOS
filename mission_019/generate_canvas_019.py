#!/usr/bin/env python3
"""Generate 7 Obsidian Canvas maps for MISSION-019 ODT."""

import json
from pathlib import Path

CANVAS_DIR = Path(__file__).parent.parent / "08_Visual_Maps"
CANVAS_DIR.mkdir(exist_ok=True)


def canvas(nodes: list, edges: list) -> str:
    return json.dumps({"nodes": nodes, "edges": edges}, indent=2)


def node(nid: str, label: str, x: int, y: int, w: int = 200, h: int = 60,
         color: str = "", ntype: str = "text", file: str = "") -> dict:
    n = {"id": nid, "type": ntype, "x": x, "y": y, "width": w, "height": h, "text": label}
    if color:
        n["color"] = color
    if file and ntype == "file":
        n["file"] = file
        del n["text"]
    return n


def edge(eid: str, src: str, tgt: str, label: str = "") -> dict:
    e = {"id": eid, "fromNode": src, "toNode": tgt, "fromSide": "right", "toSide": "left"}
    if label:
        e["label"] = label
    return e


# ─── 1. Master ODT Canvas ────────────────────────────────────────────────────
nodes_master = [
    node("yos", "Y-OS\nOrganizational Digital Twin", 0, 0, 260, 80, "1"),
    node("constitution", "CONSTITUTION\nY-OS_Constitution_v1", -600, -300, 200, 60, "5"),
    node("governance", "GOVERNANCE\nLakshmi · ADRs", -600, -100, 200, 60, "5"),
    node("runtime", "RUNTIME\nCCR v2 · Workers · Pipelines", -600, 100, 200, 60, "4"),
    node("memory", "MEMORY\nLiving Memory · Session Delta", -600, 300, 200, 60, "3"),
    node("pipelines", "PIPELINES\nPIPE-5C15BA64", 600, -300, 200, 60, "4"),
    node("artifacts", "ARTIFACTS\n10 registered", 600, -100, 200, 60, "2"),
    node("economics", "ECONOMICS\n$0.150 · 9,133 tokens", 600, 100, 200, 60, "6"),
    node("infra", "INFRASTRUCTURE\nGitHub · OpenAI · Anthropic", 600, 300, 200, 60, ""),
    node("kg", "KNOWLEDGE GRAPH\n645 nodes · 4,488 edges", 0, 400, 260, 60, "3"),
    node("health", "HEALTH SCORE\n90/100 — HEALTHY", 0, -300, 200, 60, "5"),
    node("missions", "MISSIONS\n18 completed", 0, 200, 200, 60, "2"),
]
edges_master = [
    edge("e1", "yos", "constitution", "governed_by"),
    edge("e2", "yos", "governance", "governed_by"),
    edge("e3", "yos", "runtime", "implements"),
    edge("e4", "yos", "memory", "stores"),
    edge("e5", "yos", "pipelines", "executes"),
    edge("e6", "yos", "artifacts", "produces"),
    edge("e7", "yos", "economics", "costs"),
    edge("e8", "yos", "infra", "runs_on"),
    edge("e9", "yos", "kg", "compiles"),
    edge("e10", "yos", "health", "observes"),
    edge("e11", "yos", "missions", "produces"),
]
Path(CANVAS_DIR / "YOS_Organizational_Digital_Twin.canvas").write_text(
    canvas(nodes_master, edges_master), encoding="utf-8"
)
print("  ✅ YOS_Organizational_Digital_Twin.canvas")

# ─── 2. ODT_Runtime_Executions ───────────────────────────────────────────────
nodes_rt = [
    node("ceo", "CEO\nDirective", -600, 0, 160, 60, "1"),
    node("brahma", "Brahma\nArchitecture", -300, -200, 160, 60, "4"),
    node("hanuman", "Hanuman\nBuild", -300, 0, 160, 60, "4"),
    node("saraswati", "Saraswati\nLearning", -300, 200, 160, 60, "4"),
    node("lakshmi", "Lakshmi\nGovernance", 0, -100, 160, 60, "5"),
    node("ganesha", "Ganesha\nReporting", 0, 100, 160, 60, "4"),
    node("ccr", "CCR Runtime v2\nMODE-B/D/E", 300, 0, 180, 60, "3"),
    node("openai", "OpenAI\ngpt-4o / mini", 600, -100, 160, 60, ""),
    node("anthropic", "Anthropic\nclaude-opus-4", 600, 100, 160, 60, ""),
    node("validator", "Output Validator\n100% VALID", 300, 300, 180, 60, "5"),
    node("registry", "Artifact Registry\n10 artifacts", 600, 300, 180, 60, "2"),
]
edges_rt = [
    edge("e1", "ceo", "brahma", "routes_to"),
    edge("e2", "ceo", "hanuman", "routes_to"),
    edge("e3", "ceo", "saraswati", "routes_to"),
    edge("e4", "brahma", "ccr", "executed_by"),
    edge("e5", "hanuman", "ccr", "executed_by"),
    edge("e6", "saraswati", "ccr", "executed_by"),
    edge("e7", "lakshmi", "ccr", "executed_by"),
    edge("e8", "ganesha", "ccr", "executed_by"),
    edge("e9", "ccr", "openai", "runs_on"),
    edge("e10", "ccr", "anthropic", "runs_on"),
    edge("e11", "ccr", "validator", "produces"),
    edge("e12", "validator", "registry", "stores"),
]
Path(CANVAS_DIR / "ODT_Runtime_Executions.canvas").write_text(
    canvas(nodes_rt, edges_rt), encoding="utf-8"
)
print("  ✅ ODT_Runtime_Executions.canvas")

# ─── 3. ODT_Pipeline_Flow ────────────────────────────────────────────────────
nodes_pf = [
    node("pipe", "PIPE-5C15BA64\nMISSION-018", 0, 0, 200, 60, "1"),
    node("s0", "S0: CEO Directive", -400, -300, 180, 60, ""),
    node("s1", "S1: Brahma\nArchitecture", -200, -300, 180, 60, "4"),
    node("s2", "S2: Hanuman\nBuild", 0, -300, 180, 60, "4"),
    node("s3", "S3: Saraswati\nLearning", 200, -300, 180, 60, "4"),
    node("s4", "S4: Lakshmi\nGovernance", 400, -300, 180, 60, "5"),
    node("s5", "S5: Ganesha\nCEO Briefing", 600, -300, 180, 60, "4"),
    node("ckpt", "6 Checkpoints\nS0→S5", 0, 200, 180, 60, "3"),
    node("rollback", "Rollback Engine\n1 simulated", 300, 200, 180, 60, "6"),
    node("vq", "Validation Queue\n5/5 PASS", -300, 200, 180, 60, "5"),
    node("git", "Git Commit\n688f374", 0, 400, 180, 60, ""),
]
edges_pf = [
    edge("e1", "pipe", "s0", "produces_artifact"),
    edge("e2", "s0", "s1", "produces_artifact"),
    edge("e3", "s1", "s2", "produces_artifact"),
    edge("e4", "s2", "s3", "produces_artifact"),
    edge("e5", "s3", "s4", "produces_artifact"),
    edge("e6", "s4", "s5", "produces_artifact"),
    edge("e7", "pipe", "ckpt", "checkpointed_by"),
    edge("e8", "pipe", "rollback", "recovered_by"),
    edge("e9", "pipe", "vq", "validated_by"),
    edge("e10", "pipe", "git", "committed_to"),
]
Path(CANVAS_DIR / "ODT_Pipeline_Flow.canvas").write_text(
    canvas(nodes_pf, edges_pf), encoding="utf-8"
)
print("  ✅ ODT_Pipeline_Flow.canvas")

# ─── 4. ODT_Artifact_Lineage ─────────────────────────────────────────────────
nodes_al = [
    node("ceo_dir", "CEO Directive", -600, 0, 180, 60, "1"),
    node("brahma_art", "Brahma Architecture\nART-M018-BRAHMA", -300, -200, 200, 60, "4"),
    node("hanuman_art", "Hanuman Build\nART-M018-HANUMAN", -300, 0, 200, 60, "4"),
    node("saraswati_art", "Saraswati Learning\nART-M018-SARASWATI", -300, 200, 200, 60, "4"),
    node("lakshmi_art", "Lakshmi Governance\nART-M018-LAKSHMI", 100, -100, 200, 60, "5"),
    node("ganesha_art", "Ganesha CEO Briefing\nART-M018-GANESHA", 100, 100, 200, 60, "4"),
    node("registry", "Artifact Registry v2\n10 artifacts", 500, 0, 200, 60, "2"),
    node("git_commit", "Git y-os-doctrine\n688f374", 500, 200, 200, 60, ""),
]
edges_al = [
    edge("e1", "ceo_dir", "brahma_art", "produces_artifact"),
    edge("e2", "brahma_art", "hanuman_art", "produces_artifact"),
    edge("e3", "brahma_art", "saraswati_art", "produces_artifact"),
    edge("e4", "hanuman_art", "lakshmi_art", "produces_artifact"),
    edge("e5", "saraswati_art", "lakshmi_art", "produces_artifact"),
    edge("e6", "lakshmi_art", "ganesha_art", "produces_artifact"),
    edge("e7", "brahma_art", "registry", "stores"),
    edge("e8", "hanuman_art", "registry", "stores"),
    edge("e9", "saraswati_art", "registry", "stores"),
    edge("e10", "lakshmi_art", "registry", "stores"),
    edge("e11", "ganesha_art", "registry", "stores"),
    edge("e12", "registry", "git_commit", "committed_to"),
]
Path(CANVAS_DIR / "ODT_Artifact_Lineage.canvas").write_text(
    canvas(nodes_al, edges_al), encoding="utf-8"
)
print("  ✅ ODT_Artifact_Lineage.canvas")

# ─── 5. ODT_Governance_System ────────────────────────────────────────────────
nodes_gov = [
    node("constitution", "Y-OS Constitution\n5 Articles", 0, -400, 220, 60, "1"),
    node("lakshmi_gov", "Lakshmi\nGovernance Worker", 0, -200, 200, 60, "5"),
    node("pre_review", "Pre-Review\nBefore LLM call", -300, 0, 180, 60, "5"),
    node("post_review", "Post-Review\nAfter artifact", 300, 0, 180, 60, "5"),
    node("adr_gov", "ADR Governance\nADR-0040→0046", -300, 200, 180, 60, "3"),
    node("artifact_gov", "Artifact Governance\n10 APPROVE", 300, 200, 180, 60, "2"),
    node("risk_score", "Risk Scores\n3-18/100", 0, 200, 180, 60, "5"),
    node("compliance", "Constitutional\nCompliance ✅", 0, 400, 200, 60, "5"),
]
edges_gov = [
    edge("e1", "constitution", "lakshmi_gov", "governed_by"),
    edge("e2", "lakshmi_gov", "pre_review", "produces"),
    edge("e3", "lakshmi_gov", "post_review", "produces"),
    edge("e4", "pre_review", "risk_score", "validates"),
    edge("e5", "post_review", "risk_score", "validates"),
    edge("e6", "lakshmi_gov", "adr_gov", "audits"),
    edge("e7", "lakshmi_gov", "artifact_gov", "audits"),
    edge("e8", "risk_score", "compliance", "validates"),
]
Path(CANVAS_DIR / "ODT_Governance_System.canvas").write_text(
    canvas(nodes_gov, edges_gov), encoding="utf-8"
)
print("  ✅ ODT_Governance_System.canvas")

# ─── 6. ODT_Economics ────────────────────────────────────────────────────────
nodes_eco = [
    node("total", "TOTAL COST\n$0.150190 USD\n9,133 tokens", 0, 0, 220, 80, "6"),
    node("openai_eco", "OpenAI\n$0.120 · 6,412 tokens\n8 calls", -400, -200, 200, 80, ""),
    node("anthropic_eco", "Anthropic\n$0.030 · 2,601 tokens\n2 calls", -400, 100, 200, 80, ""),
    node("m017_eco", "MISSION-017\n4,297 tokens\n$0.076055", 400, -200, 200, 80, "2"),
    node("m018_eco", "MISSION-018\n4,836 tokens\n$0.074135", 400, 100, 200, 80, "2"),
    node("brahma_eco", "Brahma\n1,957 tokens", 0, -300, 160, 60, "4"),
    node("saraswati_eco", "Saraswati\n2,601 tokens", 0, -100, 160, 60, "4"),
    node("lakshmi_eco", "Lakshmi\n1,809 tokens", 0, 100, 160, 60, "5"),
    node("hanuman_eco", "Hanuman\n1,595 tokens", 0, 300, 160, 60, "4"),
]
edges_eco = [
    edge("e1", "openai_eco", "total", "costs"),
    edge("e2", "anthropic_eco", "total", "costs"),
    edge("e3", "m017_eco", "total", "costs"),
    edge("e4", "m018_eco", "total", "costs"),
    edge("e5", "brahma_eco", "openai_eco", "runs_on"),
    edge("e6", "saraswati_eco", "anthropic_eco", "runs_on"),
    edge("e7", "lakshmi_eco", "openai_eco", "runs_on"),
    edge("e8", "hanuman_eco", "openai_eco", "runs_on"),
]
Path(CANVAS_DIR / "ODT_Economics.canvas").write_text(
    canvas(nodes_eco, edges_eco), encoding="utf-8"
)
print("  ✅ ODT_Economics.canvas")

# ─── 7. ODT_Evolution_Map ────────────────────────────────────────────────────
nodes_ev = [
    node("m013", "M-013\nDoc Graph\n301 files", -700, 0, 160, 80, ""),
    node("m014", "M-014\nCognitive Graph\n12 concepts", -500, 0, 160, 80, ""),
    node("m015", "M-015\nKGC v2\n39 concepts\n4,498 links", -300, 0, 160, 80, ""),
    node("m016", "M-016\nCCR Runtime v2\n6 modules", -100, 0, 160, 80, "4"),
    node("m017", "M-017\nLive Workers\n4 artifacts", 100, 0, 160, 80, "4"),
    node("m018", "M-018\nPipeline\n6 artifacts", 300, 0, 160, 80, "4"),
    node("m019", "M-019\nODT Runtime\n645 nodes", 500, 0, 160, 80, "1"),
    node("adr_growth", "ADR Growth\n20 → 26", 0, -200, 160, 60, "3"),
    node("cost_growth", "Cost Growth\n$0 → $0.150", 0, 200, 160, 60, "6"),
    node("graph_growth", "Graph Growth\n565 → 4,488 edges", 200, -200, 180, 60, "3"),
]
edges_ev = [
    edge("e1", "m013", "m014", "evolves_into"),
    edge("e2", "m014", "m015", "evolves_into"),
    edge("e3", "m015", "m016", "evolves_into"),
    edge("e4", "m016", "m017", "evolves_into"),
    edge("e5", "m017", "m018", "evolves_into"),
    edge("e6", "m018", "m019", "evolves_into"),
    edge("e7", "m019", "adr_growth", "produces"),
    edge("e8", "m019", "cost_growth", "produces"),
    edge("e9", "m019", "graph_growth", "produces"),
]
Path(CANVAS_DIR / "ODT_Evolution_Map.canvas").write_text(
    canvas(nodes_ev, edges_ev), encoding="utf-8"
)
print("  ✅ ODT_Evolution_Map.canvas")

print(f"\n7 Canvas maps generated in {CANVAS_DIR}")
