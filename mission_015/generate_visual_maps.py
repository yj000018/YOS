#!/usr/bin/env python3
"""
MISSION-015 — Generate 8 Canvas maps + 8 Mermaid maps
All maps link back to source Markdown artifacts.
"""

import json
from pathlib import Path

MAPS_DIR = Path("/home/ubuntu/yreg/08_Visual_Maps")
MAPS_DIR.mkdir(exist_ok=True)
TODAY = "2026-06-14"

# ─── Canvas Map Generator ─────────────────────────────────────────────────────

def make_node(id, x, y, width, height, label, color=None, file=None):
    node = {
        "id": id,
        "type": "text" if not file else "file",
        "x": x, "y": y,
        "width": width, "height": height,
    }
    if file:
        node["file"] = file
    else:
        node["text"] = label
    if color:
        node["color"] = color
    return node

def make_edge(id, from_id, to_id, label=""):
    e = {"id": id, "fromNode": from_id, "toNode": to_id, "fromSide": "right", "toSide": "left"}
    if label:
        e["label"] = label
    return e

def save_canvas(name, nodes, edges):
    path = MAPS_DIR / f"{name}.canvas"
    data = {"nodes": nodes, "edges": edges}
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"  ✅ {name}.canvas ({len(nodes)} nodes, {len(edges)} edges)")
    return path

# ─── 1. YOS_Organizational_Digital_Twin ──────────────────────────────────────

def gen_organizational_digital_twin():
    nodes = []
    edges = []
    nid = 0

    def n(x, y, w, h, label, color=None, file=None):
        nonlocal nid
        nid += 1
        return make_node(str(nid), x, y, w, h, label, color, file)

    def e(from_id, to_id, label=""):
        nonlocal nid
        nid += 1
        return make_edge(str(nid), from_id, to_id, label)

    # Title
    title = n(-200, -1400, 600, 80, "# Y-OS Organizational Digital Twin", "1")
    nodes.append(title)

    # Layer 1 — Constitution
    l1 = n(-200, -1250, 600, 60, "**Layer 1 — Constitution**", "6")
    nodes.append(l1)
    arts = [
        n(-900, -1150, 200, 60, "Article I\nArtifact Primacy", "1", "CONSTITUTION/Y-OS_Constitution_v1.md"),
        n(-650, -1150, 200, 60, "Article II\nPreservation", "1", "CONSTITUTION/Y-OS_Constitution_v1.md"),
        n(-400, -1150, 200, 60, "Article III\nDerivation", "1", "CONSTITUTION/Y-OS_Constitution_v1.md"),
        n(-150, -1150, 200, 60, "Article IV\nHuman Override", "1", "CONSTITUTION/Y-OS_Constitution_v1.md"),
        n(100, -1150, 200, 60, "Article V\nGovernance First", "1", "CONSTITUTION/Y-OS_Constitution_v1.md"),
    ]
    nodes.extend(arts)

    # Layer 2 — Governance
    l2 = n(-200, -1000, 600, 60, "**Layer 2 — Governance**", "5")
    nodes.append(l2)
    gov_nodes = [
        n(-900, -900, 200, 60, "Lakshmi\nCLO / Risk", "5", "concepts/Lakshmi.md"),
        n(-650, -900, 200, 60, "Governance\nDeterminism", "5", "concepts/Governance_Determinism.md"),
        n(-400, -900, 200, 60, "Risk Score\n≤ 35 = APPROVE", "5"),
        n(-150, -900, 200, 60, "Human Override\n(Ganesha)", "5", "concepts/Human_Override.md"),
        n(100, -900, 200, 60, "Constitutional\nReview", "5", "concepts/Constitutional_Governance.md"),
    ]
    nodes.extend(gov_nodes)

    # Layer 3 — Organization
    l3 = n(-200, -750, 600, 60, "**Layer 3 — Organization**", "3")
    nodes.append(l3)
    org_nodes = [
        n(-1100, -650, 180, 60, "CEO\nGanesha", "3", "concepts/Ganesha.md"),
        n(-880, -650, 180, 60, "Krishna\nCPO", "3", "concepts/Krishna.md"),
        n(-660, -650, 180, 60, "Brahma\nCTO", "3", "concepts/Brahma.md"),
        n(-440, -650, 180, 60, "Hanuman\nCOO", "3", "concepts/Hanuman.md"),
        n(-220, -650, 180, 60, "Lakshmi\nCLO", "3", "concepts/Lakshmi.md"),
        n(0, -650, 180, 60, "Saraswati\nCLO (Learn)", "3", "concepts/Saraswati.md"),
    ]
    nodes.extend(org_nodes)

    # Layer 4 — Orchestration
    l4 = n(-200, -500, 600, 60, "**Layer 4 — Orchestration**", "4")
    nodes.append(l4)
    orch_nodes = [
        n(-900, -400, 180, 60, "Y-ORC\nOrchestrator", "4", "concepts/Y_ORC.md"),
        n(-680, -400, 180, 60, "ART\nArtifact RT", "4", "concepts/ART.md"),
        n(-460, -400, 180, 60, "CRT\nContext RT", "4", "concepts/CRT.md"),
        n(-240, -400, 180, 60, "CCR\nContext Compiler", "4", "concepts/CCR_Runtime.md"),
        n(-20, -400, 180, 60, "Context Router\nMode A/B/C/D", "4", "concepts/Context_Router.md"),
    ]
    nodes.extend(orch_nodes)

    # Layer 5 — Memory Pipeline
    l5 = n(-200, -250, 600, 60, "**Layer 5 — Living Memory Pipeline**", "2")
    nodes.append(l5)
    mem_nodes = [
        n(-1100, -150, 140, 60, "Capture", "2"),
        n(-930, -150, 140, 60, "Compress", "2"),
        n(-760, -150, 140, 60, "Delta", "2", "concepts/Session_Delta.md"),
        n(-590, -150, 140, 60, "Summarize", "2"),
        n(-420, -150, 140, 60, "Archive", "2", "concepts/Archive_Reference.md"),
        n(-250, -150, 140, 60, "Canonicalize", "2", "concepts/Canonical_Memory.md"),
        n(-80, -150, 140, 60, "Compile", "2", "concepts/Knowledge_Graph_Compiler.md"),
        n(90, -150, 140, 60, "Inject", "2", "concepts/Context_Pack.md"),
    ]
    nodes.extend(mem_nodes)

    # Layer 6 — Runtime
    l6 = n(-200, 0, 600, 60, "**Layer 6 — Runtime**", "6")
    nodes.append(l6)
    rt_nodes = [
        n(-900, 100, 180, 60, "Artifact Registry", "6", "concepts/Artifact_Registry.md"),
        n(-680, 100, 180, 60, "Context Packs", "6", "concepts/Context_Pack.md"),
        n(-460, 100, 180, 60, "Workers", "6", "concepts/Worker_Registry.md"),
        n(-240, 100, 180, 60, "Providers", "6", "concepts/Provider_Adapter.md"),
        n(-20, 100, 180, 60, "Models", "6", "concepts/Model_Registry.md"),
        n(200, 100, 180, 60, "Git / Obsidian", "6", "concepts/Git_backed_Memory.md"),
    ]
    nodes.extend(rt_nodes)

    # Layer 7 — Validation
    l7 = n(-200, 250, 600, 60, "**Layer 7 — Validation History**", "1")
    nodes.append(l7)
    val_nodes = [
        n(-900, 350, 400, 60, "MISSION-001 → MISSION-015", "1", "03_Missions_MOC.md"),
        n(-450, 350, 400, 60, "ADR-0024 → ADR-0042", "1", "02_ADRs_MOC.md"),
    ]
    nodes.extend(val_nodes)

    # Edges: layer connections (simplified — top to bottom flow)
    for art in arts:
        edges.append(e(l1["id"], art["id"], "defines"))
    for gn in gov_nodes:
        edges.append(e(l2["id"], gn["id"], "governs"))
    for on in org_nodes:
        edges.append(e(l3["id"], on["id"], "employs"))
    for on in orch_nodes:
        edges.append(e(l4["id"], on["id"], "runs"))
    for mn in mem_nodes:
        edges.append(e(l5["id"], mn["id"], "stage"))
    for rn in rt_nodes:
        edges.append(e(l6["id"], rn["id"], "contains"))
    for vn in val_nodes:
        edges.append(e(l7["id"], vn["id"], "validates"))

    save_canvas("YOS_Organizational_Digital_Twin", nodes, edges)

# ─── 2. YOS_Constitutional_Stack ─────────────────────────────────────────────

def gen_constitutional_stack():
    nodes = []
    edges = []
    nid = [0]

    def n(x, y, w, h, label, color=None, file=None):
        nid[0] += 1
        return make_node(str(nid[0]), x, y, w, h, label, color, file)

    def e(from_id, to_id, label=""):
        nid[0] += 1
        return make_edge(str(nid[0]), from_id, to_id, label)

    title = n(-100, -800, 400, 60, "# Y-OS Constitutional Stack", "1")
    nodes.append(title)

    const = n(-100, -680, 400, 80, "**Y-OS Constitution v1**\n5 Articles — FROZEN", "1", "CONSTITUTION/Y-OS_Constitution_v1.md")
    nodes.append(const)

    articles = [
        n(-700, -550, 220, 80, "**Article I**\nArtifact Primacy\n[[Artifact_Primacy]]", "1", "concepts/Artifact_Primacy.md"),
        n(-450, -550, 220, 80, "**Article II**\nPreservation Principle\n[[Preservation_Principle]]", "2", "concepts/Preservation_Principle.md"),
        n(-200, -550, 220, 80, "**Article III**\nDerivation Transparency\n[[Derivation_Transparency]]", "3", "concepts/Derivation_Transparency.md"),
        n(50, -550, 220, 80, "**Article IV**\nHuman Override\n[[Human_Override]]", "4", "concepts/Human_Override.md"),
        n(300, -550, 220, 80, "**Article V**\nGovernance First\n[[Governance_Before_Autonomy]]", "5", "concepts/Governance_Before_Autonomy.md"),
    ]
    nodes.extend(articles)

    for art in articles:
        edges.append(e(const["id"], art["id"], "defines"))

    gov_det = n(-100, -350, 300, 60, "Governance Determinism\n[[Governance_Determinism]]", "5", "concepts/Governance_Determinism.md")
    nodes.append(gov_det)
    edges.append(e(articles[4]["id"], gov_det["id"], "enables"))

    lakshmi = n(-100, -230, 300, 60, "Lakshmi Governance\n[[Lakshmi_Governance]]", "5", "concepts/Lakshmi_Governance.md")
    nodes.append(lakshmi)
    edges.append(e(gov_det["id"], lakshmi["id"], "implements"))

    adr_chain = n(-100, -110, 300, 60, "ADR Register\nADR-0024 → ADR-0042", "6", "02_ADRs_MOC.md")
    nodes.append(adr_chain)
    edges.append(e(lakshmi["id"], adr_chain["id"], "validates"))

    save_canvas("YOS_Constitutional_Stack", nodes, edges)

# ─── 3. YOS_Runtime_Flow ─────────────────────────────────────────────────────

def gen_runtime_flow():
    nodes = []
    edges = []
    nid = [0]

    def n(x, y, w, h, label, color=None, file=None):
        nid[0] += 1
        return make_node(str(nid[0]), x, y, w, h, label, color, file)

    def e(from_id, to_id, label=""):
        nid[0] += 1
        return make_edge(str(nid[0]), from_id, to_id, label)

    title = n(0, -600, 400, 60, "# Y-OS Runtime Flow", "4")
    nodes.append(title)

    mission = n(-600, -450, 200, 60, "Mission\nDefinition", "3", "03_Missions_MOC.md")
    yorc = n(-350, -450, 200, 60, "Y-ORC\nOrchestrator", "4", "concepts/Y_ORC.md")
    ccr = n(-100, -450, 200, 60, "CCR\nContext Compiler", "4", "concepts/CCR_Runtime.md")
    crt = n(150, -450, 200, 60, "CRT\nContext Runtime", "4", "concepts/CRT.md")
    art = n(400, -450, 200, 60, "ART\nArtifact Runtime", "4", "concepts/ART.md")
    nodes.extend([mission, yorc, ccr, crt, art])

    edges.append(e(mission["id"], yorc["id"], "triggers"))
    edges.append(e(yorc["id"], ccr["id"], "requests context"))
    edges.append(e(ccr["id"], crt["id"], "compiles pack"))
    edges.append(e(crt["id"], yorc["id"], "injects context"))
    edges.append(e(yorc["id"], art["id"], "captures output"))

    provider = n(-100, -280, 200, 60, "Provider Adapter\n(Claude/GPT/Gemini)", "2", "concepts/Provider_Adapter.md")
    worker = n(150, -280, 200, 60, "Worker\n(Brahma/Hanuman...)", "3", "concepts/Worker_Registry.md")
    artifact = n(400, -280, 200, 60, "Artifact\n(Canonical Output)", "1", "concepts/Artifact_Registry.md")
    nodes.extend([provider, worker, artifact])

    edges.append(e(yorc["id"], provider["id"], "routes to"))
    edges.append(e(yorc["id"], worker["id"], "assigns to"))
    edges.append(e(art["id"], artifact["id"], "stores"))

    save_canvas("YOS_Runtime_Flow", nodes, edges)

# ─── 4. YOS_Context_Architecture ─────────────────────────────────────────────

def gen_context_architecture():
    nodes = []
    edges = []
    nid = [0]

    def n(x, y, w, h, label, color=None, file=None):
        nid[0] += 1
        return make_node(str(nid[0]), x, y, w, h, label, color, file)

    def e(from_id, to_id, label=""):
        nid[0] += 1
        return make_edge(str(nid[0]), from_id, to_id, label)

    title = n(0, -700, 500, 60, "# Y-OS Context Architecture (CCR v2)", "4")
    nodes.append(title)

    modes = [
        n(-700, -550, 200, 80, "**Mode A**\nFull History\nROI: 23.4", "2"),
        n(-460, -550, 200, 80, "**Mode B** ⭐\nContext Pack Only\nROI: 140.9", "3"),
        n(-220, -550, 200, 80, "**Mode C**\nHybrid\nROI: 89.2", "4"),
        n(20, -550, 200, 80, "**Mode D**\nDelta Only\nROI: 67.8", "5"),
    ]
    nodes.extend(modes)

    router = n(-200, -380, 300, 60, "Context Router\n(CCR v2 — ADR-0037)", "4", "concepts/Context_Router.md")
    nodes.append(router)
    for m in modes:
        edges.append(e(router["id"], m["id"], "selects"))

    ctx_pack = n(-700, -220, 200, 60, "Context Pack\n[[Context_Pack]]", "3", "concepts/Context_Pack.md")
    session_delta = n(-460, -220, 200, 60, "Session Delta\n[[Session_Delta]]", "5", "concepts/Session_Delta.md")
    canon_mem = n(-220, -220, 200, 60, "Canonical Memory\n[[Canonical_Memory]]", "1", "concepts/Canonical_Memory.md")
    mission_ctx = n(20, -220, 200, 60, "Mission Context\n(injected)", "3")
    nodes.extend([ctx_pack, session_delta, canon_mem, mission_ctx])

    edges.append(e(ctx_pack["id"], router["id"], "feeds"))
    edges.append(e(session_delta["id"], ctx_pack["id"], "delta → pack"))
    edges.append(e(canon_mem["id"], ctx_pack["id"], "canonical → pack"))
    edges.append(e(router["id"], mission_ctx["id"], "injects"))

    save_canvas("YOS_Context_Architecture", nodes, edges)

# ─── 5. YOS_Living_Memory_Pipeline ───────────────────────────────────────────

def gen_living_memory_pipeline():
    nodes = []
    edges = []
    nid = [0]

    def n(x, y, w, h, label, color=None, file=None):
        nid[0] += 1
        return make_node(str(nid[0]), x, y, w, h, label, color, file)

    def e(from_id, to_id, label=""):
        nid[0] += 1
        return make_edge(str(nid[0]), from_id, to_id, label)

    title = n(0, -500, 500, 60, "# Y-OS Living Memory Pipeline (ADR-0039)", "2")
    nodes.append(title)

    stages = [
        ("Capture", "Session artifacts\nraw output", "2", None),
        ("Compress", "Token reduction\n60-80%", "2", None),
        ("Delta", "Session Delta\n[[Session_Delta]]", "5", "concepts/Session_Delta.md"),
        ("Summarize", "Canonical Summary\nper session", "2", None),
        ("Archive", "Archive Reference\n[[Archive_Reference]]", "6", "concepts/Archive_Reference.md"),
        ("Canonicalize", "Canonical Memory\n[[Canonical_Memory]]", "1", "concepts/Canonical_Memory.md"),
        ("Compile", "KGC v2\n[[Knowledge_Graph_Compiler]]", "4", "concepts/Knowledge_Graph_Compiler.md"),
        ("Inject", "Context Pack\n[[Context_Pack]]", "3", "concepts/Context_Pack.md"),
    ]

    prev = None
    for i, (stage, desc, color, file) in enumerate(stages):
        node = n(-800 + i * 220, -300, 200, 80, f"**{stage}**\n{desc}", color, file)
        nodes.append(node)
        if prev:
            edges.append(e(prev["id"], node["id"], "→"))
        prev = node

    # Loop back: Inject → Capture (next session)
    edges.append(e(nodes[-1]["id"], nodes[1]["id"], "next session"))

    save_canvas("YOS_Living_Memory_Pipeline", nodes, edges)

# ─── 6. YOS_Mission_Evolution ────────────────────────────────────────────────

def gen_mission_evolution():
    nodes = []
    edges = []
    nid = [0]

    def n(x, y, w, h, label, color=None, file=None):
        nid[0] += 1
        return make_node(str(nid[0]), x, y, w, h, label, color, file)

    def e(from_id, to_id, label=""):
        nid[0] += 1
        return make_edge(str(nid[0]), from_id, to_id, label)

    title = n(0, -600, 500, 60, "# Y-OS Mission Evolution (001 → 015)", "3")
    nodes.append(title)

    missions = [
        ("001", "Foundation\nArtifact Primacy", "1"),
        ("002", "Artifact\nRegistry v1", "1"),
        ("003", "Context\nPack v1", "2"),
        ("004", "Worker\nRegistry", "3"),
        ("005", "Y-ORC\nRuntime v1", "4"),
        ("005c", "Governance\nDeterminism", "5"),
        ("006", "Constitutional\nCore v1", "1"),
        ("007", "Replacement\nTest", "1"),
        ("008", "Provider\nAdapter", "4"),
        ("009", "Executable\nConstitution", "1"),
        ("010", "Context\nArchitecture", "2"),
        ("011", "CCR Runtime\nv2", "4"),
        ("012", "Session Delta\nEngine", "5"),
        ("012b", "Living Memory\nPipeline", "2"),
        ("013", "KGC v1\nDocument Graph", "6"),
        ("013b", "Graph Quality\nAudit", "6"),
        ("014", "Cognitive Graph\nArchitecture", "6"),
        ("015", "KGC v2\nVisual Drill-Down", "6"),
    ]

    prev = None
    row = 0
    col = 0
    for i, (mid, label, color) in enumerate(missions):
        x = -900 + col * 220
        y = -400 + row * 160
        node = n(x, y, 200, 80, f"**M-{mid}**\n{label}", color)
        nodes.append(node)
        if prev:
            edges.append(e(prev["id"], node["id"], "→"))
        prev = node
        col += 1
        if col >= 6:
            col = 0
            row += 1

    save_canvas("YOS_Mission_Evolution", nodes, edges)

# ─── 7. YOS_ADR_Dependency_Map ───────────────────────────────────────────────

def gen_adr_dependency_map():
    nodes = []
    edges = []
    nid = [0]

    def n(x, y, w, h, label, color=None, file=None):
        nid[0] += 1
        return make_node(str(nid[0]), x, y, w, h, label, color, file)

    def e(from_id, to_id, label=""):
        nid[0] += 1
        return make_edge(str(nid[0]), from_id, to_id, label)

    title = n(0, -700, 500, 60, "# Y-OS ADR Dependency Map", "6")
    nodes.append(title)

    # Key ADRs with dependencies
    adrs = {
        "ADR-0024": ("Constitution\nFoundation", "1", -800, -550),
        "ADR-0025": ("Y-ORC\nRuntime", "4", -550, -550),
        "ADR-0026": ("ART\nArtifact RT", "4", -300, -550),
        "ADR-0027": ("Provider\nAdapter", "4", -50, -550),
        "ADR-0028": ("CRT\nContext RT", "4", 200, -550),
        "ADR-0029": ("CCR\nRuntime v1", "2", -800, -380),
        "ADR-0030": ("CCR\nRuntime v1.1", "2", -550, -380),
        "ADR-0033": ("Governance\nDeterminism", "5", -300, -380),
        "ADR-0034": ("Constitutional\nCore v1", "1", -50, -380),
        "ADR-0035": ("Executable\nConstitution", "1", 200, -380),
        "ADR-0036": ("Context\nArchitecture", "2", -800, -210),
        "ADR-0037": ("CCR Runtime\nv2", "4", -550, -210),
        "ADR-0038": ("Session Delta\nEngine", "5", -300, -210),
        "ADR-0039": ("Living Memory\nPipeline", "2", -50, -210),
        "ADR-0040": ("KGC v1\nDoc Graph", "6", 200, -210),
        "ADR-0041": ("Cognitive Graph\nArchitecture", "6", -400, -40),
        "ADR-0042": ("KGC v2\nVisual Layer", "6", -100, -40),
    }

    adr_nodes = {}
    for adr_id, (label, color, x, y) in adrs.items():
        node = n(x, y, 200, 70, f"**{adr_id}**\n{label}", color)
        nodes.append(node)
        adr_nodes[adr_id] = node

    # Key dependency edges
    dep_edges = [
        ("ADR-0024", "ADR-0025", "enables"),
        ("ADR-0024", "ADR-0026", "enables"),
        ("ADR-0024", "ADR-0027", "enables"),
        ("ADR-0024", "ADR-0028", "enables"),
        ("ADR-0025", "ADR-0029", "depends_on"),
        ("ADR-0029", "ADR-0030", "evolves_into"),
        ("ADR-0030", "ADR-0037", "evolves_into"),
        ("ADR-0033", "ADR-0037", "governs"),
        ("ADR-0034", "ADR-0035", "enables"),
        ("ADR-0036", "ADR-0037", "informs"),
        ("ADR-0037", "ADR-0038", "depends_on"),
        ("ADR-0038", "ADR-0039", "enables"),
        ("ADR-0039", "ADR-0040", "enables"),
        ("ADR-0040", "ADR-0041", "evolves_into"),
        ("ADR-0041", "ADR-0042", "evolves_into"),
    ]

    for src, tgt, label in dep_edges:
        if src in adr_nodes and tgt in adr_nodes:
            edges.append(e(adr_nodes[src]["id"], adr_nodes[tgt]["id"], label))

    save_canvas("YOS_ADR_Dependency_Map", nodes, edges)

# ─── 8. YOS_Governance_Flow ──────────────────────────────────────────────────

def gen_governance_flow():
    nodes = []
    edges = []
    nid = [0]

    def n(x, y, w, h, label, color=None, file=None):
        nid[0] += 1
        return make_node(str(nid[0]), x, y, w, h, label, color, file)

    def e(from_id, to_id, label=""):
        nid[0] += 1
        return make_edge(str(nid[0]), from_id, to_id, label)

    title = n(0, -700, 500, 60, "# Y-OS Governance Flow", "5")
    nodes.append(title)

    proposal = n(-200, -580, 300, 60, "ADR Proposal\n(Brahma / any worker)", "3")
    nodes.append(proposal)

    lakshmi_review = n(-200, -460, 300, 80, "Lakshmi Review\n5 Articles × Risk Score\n[[Lakshmi_Governance]]", "5", "concepts/Lakshmi_Governance.md")
    nodes.append(lakshmi_review)
    edges.append(e(proposal["id"], lakshmi_review["id"], "submits"))

    approve = n(-500, -320, 200, 60, "APPROVE\nScore ≤ 35", "3")
    warn = n(-200, -320, 200, 60, "APPROVE\nWITH WARNING\n36–55", "4")
    reject = n(100, -320, 200, 60, "REJECT\n> 55 or\nblocking", "1")
    nodes.extend([approve, warn, reject])
    edges.append(e(lakshmi_review["id"], approve["id"], "≤ 35"))
    edges.append(e(lakshmi_review["id"], warn["id"], "36–55"))
    edges.append(e(lakshmi_review["id"], reject["id"], "> 55"))

    ceo = n(-350, -160, 250, 60, "CEO Recommendation\nGanesha — ADOPT/REJECT", "3", "concepts/Ganesha.md")
    nodes.append(ceo)
    edges.append(e(approve["id"], ceo["id"], "→ CEO"))
    edges.append(e(warn["id"], ceo["id"], "→ CEO"))

    accepted = n(-500, -20, 200, 60, "ADR ACCEPTED\n(canonical)", "3")
    revised = n(-100, -20, 200, 60, "ADR REVISED\nor SUPERSEDED", "4")
    nodes.extend([accepted, revised])
    edges.append(e(ceo["id"], accepted["id"], "ADOPT"))
    edges.append(e(ceo["id"], revised["id"], "REJECT → revise"))
    edges.append(e(reject["id"], revised["id"], "revise"))

    save_canvas("YOS_Governance_Flow", nodes, edges)

# ─── Mermaid Fallback Maps ────────────────────────────────────────────────────

MERMAID_MAPS = {
    "YOS_Organizational_Digital_Twin": """---
title: Y-OS Organizational Digital Twin
type: visual_map
tags: ['#visual', '#yos', '#canvas']
---

# Y-OS Organizational Digital Twin — Mermaid Fallback

*See [[YOS_Organizational_Digital_Twin.canvas]] for interactive Canvas version.*

```mermaid
graph TB
    subgraph L1["Layer 1 — Constitution"]
        A1[Article I: Artifact Primacy]
        A2[Article II: Preservation]
        A3[Article III: Derivation]
        A4[Article IV: Human Override]
        A5[Article V: Governance First]
    end
    subgraph L2["Layer 2 — Governance"]
        G1[Lakshmi CLO]
        G2[Governance Determinism]
        G3[Risk Score ≤35]
        G4[Human Override]
        G5[Constitutional Review]
    end
    subgraph L3["Layer 3 — Organization"]
        O1[Ganesha CEO]
        O2[Krishna CPO]
        O3[Brahma CTO]
        O4[Hanuman COO]
        O5[Lakshmi CLO]
        O6[Saraswati CLO]
    end
    subgraph L4["Layer 4 — Orchestration"]
        R1[Y-ORC]
        R2[ART]
        R3[CRT]
        R4[CCR]
        R5[Context Router]
    end
    subgraph L5["Layer 5 — Memory Pipeline"]
        M1[Capture] --> M2[Compress] --> M3[Delta] --> M4[Summarize]
        M4 --> M5[Archive] --> M6[Canonicalize] --> M7[Compile] --> M8[Inject]
        M8 -.->|next session| M1
    end
    subgraph L6["Layer 6 — Runtime"]
        RT1[Artifact Registry]
        RT2[Context Packs]
        RT3[Workers]
        RT4[Providers]
        RT5[Models]
        RT6[Git/Obsidian]
    end
    L1 --> L2 --> L3 --> L4 --> L5 --> L6
```
""",
    "YOS_Constitutional_Stack": """---
title: Y-OS Constitutional Stack
type: visual_map
tags: ['#visual', '#constitution', '#yos']
---

# Y-OS Constitutional Stack — Mermaid Fallback

*See [[YOS_Constitutional_Stack.canvas]] for interactive Canvas version.*

```mermaid
graph TD
    CONST["Y-OS Constitution v1 — FROZEN"]
    CONST --> A1["Article I: Artifact Primacy\\n[[Artifact_Primacy]]"]
    CONST --> A2["Article II: Preservation Principle\\n[[Preservation_Principle]]"]
    CONST --> A3["Article III: Derivation Transparency\\n[[Derivation_Transparency]]"]
    CONST --> A4["Article IV: Human Override\\n[[Human_Override]]"]
    CONST --> A5["Article V: Governance Before Autonomy\\n[[Governance_Before_Autonomy]]"]
    A5 --> GD["Governance Determinism\\n[[Governance_Determinism]]"]
    GD --> LG["Lakshmi Governance\\n[[Lakshmi_Governance]]"]
    LG --> ADR["ADR Register\\nADR-0024 → ADR-0042"]
```
""",
    "YOS_Runtime_Flow": """---
title: Y-OS Runtime Flow
type: visual_map
tags: ['#visual', '#runtime', '#yos']
---

# Y-OS Runtime Flow — Mermaid Fallback

*See [[YOS_Runtime_Flow.canvas]] for interactive Canvas version.*

```mermaid
sequenceDiagram
    participant M as Mission
    participant YORC as Y-ORC
    participant CCR as CCR Compiler
    participant CRT as CRT Runtime
    participant ART as ART
    participant P as Provider
    participant W as Worker

    M->>YORC: trigger mission
    YORC->>CCR: request context pack
    CCR->>CRT: compiled pack
    CRT->>YORC: inject context
    YORC->>W: assign task
    W->>P: call provider
    P-->>W: LLM response
    W-->>YORC: output
    YORC->>ART: capture artifact
    ART-->>M: canonical artifact
```
""",
    "YOS_Context_Architecture": """---
title: Y-OS Context Architecture
type: visual_map
tags: ['#visual', '#context', '#ccr', '#yos']
---

# Y-OS Context Architecture — Mermaid Fallback

*See [[YOS_Context_Architecture.canvas]] for interactive Canvas version.*

```mermaid
graph LR
    SD["Session Delta\\n[[Session_Delta]]"] --> CP["Context Pack\\n[[Context_Pack]]"]
    CM["Canonical Memory\\n[[Canonical_Memory]]"] --> CP
    CP --> CR["Context Router\\n(CCR v2)"]
    CR --> MA["Mode A: Full History\\nROI: 23.4"]
    CR --> MB["Mode B: Pack Only ⭐\\nROI: 140.9"]
    CR --> MC["Mode C: Hybrid\\nROI: 89.2"]
    CR --> MD["Mode D: Delta Only\\nROI: 67.8"]
    MB --> MI["Mission Context\\n(injected)"]
```
""",
    "YOS_Living_Memory_Pipeline": """---
title: Y-OS Living Memory Pipeline
type: visual_map
tags: ['#visual', '#memory', '#lmp', '#yos']
---

# Y-OS Living Memory Pipeline — Mermaid Fallback

*See [[YOS_Living_Memory_Pipeline.canvas]] for interactive Canvas version.*

```mermaid
graph LR
    CAP[Capture] --> COMP[Compress]
    COMP --> DELTA["Delta\\n[[Session_Delta]]"]
    DELTA --> SUM[Summarize]
    SUM --> ARCH["Archive\\n[[Archive_Reference]]"]
    ARCH --> CANON["Canonicalize\\n[[Canonical_Memory]]"]
    CANON --> COMPILE["Compile\\n[[Knowledge_Graph_Compiler]]"]
    COMPILE --> INJ["Inject\\n[[Context_Pack]]"]
    INJ -.->|next session| CAP
```
""",
    "YOS_Mission_Evolution": """---
title: Y-OS Mission Evolution
type: visual_map
tags: ['#visual', '#missions', '#yos']
---

# Y-OS Mission Evolution — Mermaid Fallback

*See [[YOS_Mission_Evolution.canvas]] for interactive Canvas version.*

```mermaid
timeline
    title Y-OS Mission Timeline
    section Foundation
        M-001 : Artifact Primacy
        M-002 : Artifact Registry v1
        M-003 : Context Pack v1
        M-004 : Worker Registry
    section Runtime
        M-005 : Y-ORC Runtime v1
        M-005c : Governance Determinism
        M-006 : Constitutional Core v1
        M-007 : Replacement Test
        M-008 : Provider Adapter
    section Architecture
        M-009 : Executable Constitution
        M-010 : Context Architecture
        M-011 : CCR Runtime v2
        M-012 : Session Delta Engine
        M-012b : Living Memory Pipeline
    section Knowledge Graph
        M-013 : KGC v1 Document Graph
        M-013b : Graph Quality Audit
        M-014 : Cognitive Graph Architecture
        M-015 : KGC v2 Visual Drill-Down
```
""",
    "YOS_ADR_Dependency_Map": """---
title: Y-OS ADR Dependency Map
type: visual_map
tags: ['#visual', '#adrs', '#yos']
---

# Y-OS ADR Dependency Map — Mermaid Fallback

*See [[YOS_ADR_Dependency_Map.canvas]] for interactive Canvas version.*

```mermaid
graph TD
    ADR24["ADR-0024\\nConstitution Foundation"] --> ADR25["ADR-0025\\nY-ORC Runtime"]
    ADR24 --> ADR26["ADR-0026\\nART"]
    ADR24 --> ADR27["ADR-0027\\nProvider Adapter"]
    ADR24 --> ADR28["ADR-0028\\nCRT"]
    ADR25 --> ADR29["ADR-0029\\nCCR Runtime v1"]
    ADR29 --> ADR30["ADR-0030\\nCCR Runtime v1.1"]
    ADR30 --> ADR37["ADR-0037\\nCCR Runtime v2"]
    ADR33["ADR-0033\\nGovernance Determinism"] --> ADR37
    ADR34["ADR-0034\\nConstitutional Core"] --> ADR35["ADR-0035\\nExecutable Constitution"]
    ADR36["ADR-0036\\nContext Architecture"] --> ADR37
    ADR37 --> ADR38["ADR-0038\\nSession Delta Engine"]
    ADR38 --> ADR39["ADR-0039\\nLiving Memory Pipeline"]
    ADR39 --> ADR40["ADR-0040\\nKGC v1"]
    ADR40 --> ADR41["ADR-0041\\nCognitive Graph Architecture"]
    ADR41 --> ADR42["ADR-0042\\nKGC v2 Visual Layer"]
```
""",
    "YOS_Governance_Flow": """---
title: Y-OS Governance Flow
type: visual_map
tags: ['#visual', '#governance', '#yos']
---

# Y-OS Governance Flow — Mermaid Fallback

*See [[YOS_Governance_Flow.canvas]] for interactive Canvas version.*

```mermaid
flowchart TD
    PROP["ADR Proposal\\n(Brahma / any worker)"]
    PROP --> LAK["Lakshmi Review\\n5 Articles × Risk Score"]
    LAK --> |Score ≤ 35| APP["APPROVE"]
    LAK --> |36–55| WARN["APPROVE WITH WARNING"]
    LAK --> |> 55 or blocking| REJ["REJECT"]
    APP --> CEO["CEO Recommendation\\nGanesha"]
    WARN --> CEO
    CEO --> |ADOPT| ACCEPTED["ADR ACCEPTED\\n(canonical)"]
    CEO --> |REJECT| REVISED["ADR REVISED\\nor SUPERSEDED"]
    REJ --> REVISED
```
""",
}

def gen_mermaid_maps():
    for name, content in MERMAID_MAPS.items():
        path = MAPS_DIR / f"{name}.md"
        path.write_text(content, encoding="utf-8")
        print(f"  ✅ {name}.md")

# ─── Excalidraw Assessment ────────────────────────────────────────────────────

EXCALIDRAW_ASSESSMENT = """---
title: Excalidraw Generation Assessment
type: technical_report
date: '2026-06-14'
tags: ['#visual', '#excalidraw', '#yos', '#assessment']
---

# Excalidraw Generation Assessment — MISSION-015

## Verdict: PARTIAL — Mermaid/Canvas Preferred

### Technical Analysis

Excalidraw files use a JSON format (`*.excalidraw`) that is technically generatable programmatically. However, several constraints make it suboptimal for this mission:

| Factor | Canvas | Mermaid | Excalidraw |
| :--- | :--- | :--- | :--- |
| Obsidian native support | ✅ Built-in | ✅ Built-in | ⚠️ Plugin required |
| Programmatic generation | ✅ Simple JSON | ✅ Text DSL | ⚠️ Complex schema |
| Wikilink support | ✅ file links | ✅ text links | ❌ No native links |
| Drill-down navigation | ✅ file nodes | ❌ static | ❌ static |
| Visual quality | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Maintenance | ✅ Easy | ✅ Easy | ❌ Hard |

### Decision

**Canvas maps are the primary visual layer for MISSION-015.**

Reasons:
1. Canvas maps support `file` node type → direct wikilink drill-down to source Markdown
2. Canvas is Obsidian-native (no plugin required)
3. Canvas JSON is simple and maintainable
4. Excalidraw requires the Excalidraw plugin and does not support file-linked nodes

### Excalidraw Future Path

Excalidraw maps can be generated in MISSION-016 as aesthetic overlays (not navigational) using:
- `excalidraw-utils` Python library
- Manual export from Canvas → Excalidraw via Obsidian plugin
- AI-generated visual layouts for presentation purposes

### Fallback Delivered

All 8 visual maps have been delivered as:
- ✅ Canvas maps (`.canvas`) — primary, navigable, drill-down capable
- ✅ Mermaid maps (`.md`) — fallback, readable without Obsidian

### Recommendation

Install Obsidian plugins: **Dataview** + **Breadcrumbs** + **Canvas** (built-in)
Excalidraw plugin optional for aesthetic exports only.
"""

if __name__ == "__main__":
    print("Generating Canvas maps...")
    gen_organizational_digital_twin()
    gen_constitutional_stack()
    gen_runtime_flow()
    gen_context_architecture()
    gen_living_memory_pipeline()
    gen_mission_evolution()
    gen_adr_dependency_map()
    gen_governance_flow()

    print("\nGenerating Mermaid fallback maps...")
    gen_mermaid_maps()

    print("\nWriting Excalidraw assessment...")
    exc_path = MAPS_DIR / "Excalidraw_Assessment.md"
    exc_path.write_text(EXCALIDRAW_ASSESSMENT, encoding="utf-8")
    print("  ✅ Excalidraw_Assessment.md")

    print(f"\nTotal files in 08_Visual_Maps/: {len(list(MAPS_DIR.iterdir()))}")
    print("Done.")
