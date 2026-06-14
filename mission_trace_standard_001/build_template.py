#!/usr/bin/env python3
"""
Generates value_trace_template.excalidraw
A blank, reusable template with the correct layout and color coding.
No mission-specific content.
"""
import json
import uuid

def eid(): return str(uuid.uuid4())[:8]

C = {
    "human":      ("#1d4ed8", "#93c5fd"),
    "agent":      ("#7c3aed", "#c4b5fd"),
    "llm":        ("#15803d", "#86efac"),
    "tool":       ("#c2410c", "#fdba74"),
    "governance": ("#991b1b", "#fca5a5"),
    "artifact":   ("#92400e", "#fde047"),
    "skipped":    ("#1f2937", "#6b7280"),
    "value":      ("#0c1a2e", "#38bdf8"),
    "verdict":    ("#14532d", "#4ade80"),
    "header":     ("#0f172a", "#334155"),
    "bg":         "#0f172a",
}

def rect_el(id_, x, y, w, h, bg, stroke, label="", text_color="#f8fafc", font_size=13):
    return {
        "id": id_, "type": "rectangle",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": bg,
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [],
        "roundness": {"type": 3}, "isDeleted": False, "boundElements": [],
        "updated": 1, "link": None, "locked": False
    }

def text_el(id_, x, y, w, h, text, color="#f8fafc", font_size=13):
    return {
        "id": id_, "type": "text",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [],
        "roundness": None, "isDeleted": False, "boundElements": [],
        "updated": 1, "link": None, "locked": False,
        "text": text, "fontSize": font_size, "fontFamily": 1,
        "textAlign": "left", "verticalAlign": "top",
        "containerId": None, "originalText": text,
        "lineHeight": 1.35, "baseline": font_size
    }

def arrow_el(id_, x1, y1, x2, y2, label="", color="#fde047"):
    return {
        "id": id_, "type": "arrow",
        "x": x1, "y": y1,
        "width": x2 - x1, "height": y2 - y1,
        "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [],
        "roundness": {"type": 2}, "isDeleted": False, "boundElements": [],
        "updated": 1, "link": None, "locked": False,
        "points": [[0, 0], [x2 - x1, y2 - y1]],
        "lastCommittedPoint": None, "startBinding": None, "endBinding": None,
        "startArrowhead": None, "endArrowhead": "arrow"
    }

elements = []

# ─── TITLE ────────────────────────────────────────────────────────────────────
elements.append(rect_el("title_bg", 20, 20, 2600, 80, C["header"][0], C["header"][1]))
elements.append(text_el("title_t", 40, 35, 2560, 50,
    "Y-OS VALUE TRACE TEMPLATE  |  [MISSION_ID]  |  [DATE]\n[EXACT REQUEST]",
    "#f8fafc", 16))

# ─── LEGEND ───────────────────────────────────────────────────────────────────
legend = [
    ("Human", "human"), ("Agent", "agent"), ("LLM", "llm"),
    ("Tool", "tool"), ("Governance", "governance"),
    ("Artifact", "artifact"), ("Skipped", "skipped"),
]
for i, (label, key) in enumerate(legend):
    lx = 20 + i * 240
    elements.append(rect_el(f"leg_{i}_bg", lx, 115, 220, 44, C[key][0], C[key][1]))
    elements.append(text_el(f"leg_{i}_t", lx + 10, 128, 200, 20, label, "#f8fafc", 12))

# ─── MAIN FLOW — 7 COLUMNS ────────────────────────────────────────────────────
COL_W = 340
COL_H = 520
COL_GAP = 30
START_X = 20
START_Y = 180

team_cols = [
    ("A. REQUEST\n\nUser: [NAME]\nRequest: [EXACT REQUEST]\nIntent: [analysis/creation/...]\nExpected: [OUTPUT]",
     "human", "request"),
    ("B1. ORCHESTRATOR\n\nWorker: Manus\nProvider: Y-OS Runtime\nModel: [model]\nTools: [list]\nInput: [raw request]\nOutput: [routing decision]\nLatency: [X]ms\nCost: $0.00\nArtifact: SESSION-[ID]",
     "agent", "orch"),
    ("B2. WORKER\n\nRole: [Architect/Researcher/...]\nWorker: [Name]\nProvider: [Anthropic/...]\nModel: [model]\nTools: [list]\nInput: [input]\nOutput: [output]\nLatency: [X]ms\nCost: $[X]\nArtifact: [ARTIFACT-ID]",
     "llm", "worker"),
    ("B3. VALIDATOR\n\nWorker: Lakshmi\nProvider: Y-OS Runtime\nModel: lakshmi_review_v1\nTools: output_validator\nInput: [ARTIFACT-ID]\nOutput: APPROVED\nRisk: [X]/100\nLatency: [X]ms\nCost: $0.00",
     "governance", "val"),
    ("B4. ARCHIVIST\n\nWorker: Registry\nProvider: Y-OS Runtime\nModel: artifact_registry_v2\nTools: artifact_registry\nInput: Validated artifact\nOutput: Registered\nLineage: → [PARENT]\nLatency: [X]ms\nCost: $0.00",
     "tool", "reg"),
    ("B5. MEMORY\n\nProvider: External\nTools: git push\n      notion API\n      obsidian wikilink\nInput: [ARTIFACT-ID]\nOutput: Commit [HASH]\nStatus: [ACTUAL/SIMULATED]",
     "tool", "mem"),
    ("DELIVERABLE\n\n[One-sentence description\nof what Yannick received]\n\nTime: [X]s\nCost: $[X]\nTokens: [X]",
     "artifact", "deliv"),
]

col_right_edges = []
for i, (label, key, id_) in enumerate(team_cols):
    bx = START_X + i * (COL_W + COL_GAP)
    elements.append(rect_el(f"{id_}_bg", bx, START_Y, COL_W, COL_H, C[key][0], C[key][1]))
    elements.append(text_el(f"{id_}_t", bx + 12, START_Y + 12, COL_W - 24, COL_H - 24, label, "#f8fafc", 12))
    col_right_edges.append(bx + COL_W)

# Artifact handoff arrows
for i in range(len(team_cols) - 1):
    x1 = col_right_edges[i]
    x2 = START_X + (i + 1) * (COL_W + COL_GAP)
    y_mid = START_Y + COL_H // 2
    elements.append(arrow_el(f"arr_{i}", x1, y_mid, x2, y_mid,
                              "[ARTIFACT]\n[X] tokens / $[X] / [X]ms", "#fde047"))
    elements.append(text_el(f"arr_{i}_t",
                             (x1 + x2) // 2 - 80, y_mid - 40, 160, 36,
                             "[ARTIFACT-ID]\n[X] tokens / $[X] / [X]ms",
                             "#fde047", 10))

# ─── PLUGINS SKIPPED ──────────────────────────────────────────────────────────
SKIP_Y = START_Y + COL_H + 40
elements.append(rect_el("skip_hdr", 20, SKIP_Y, 2600, 44, C["skipped"][0], C["skipped"][1]))
elements.append(text_el("skip_hdr_t", 40, SKIP_Y + 12, 2560, 20,
    "D. PLUGINS SKIPPED — [GOVERNANCE MODE] Active", "#9ca3af", 13))

skip_w = 600
for i, (name, desc) in enumerate([
    ("ODT", "Organizational Digital Twin\nNOT ACTIVATED"),
    ("STRATEGIC INTEL", "Strategic Intelligence\nNOT ACTIVATED"),
    ("SIMULATION", "Time Machine / Counterfactual\nNOT ACTIVATED"),
    ("OBSERVABILITY", "Advanced Observability Dashboard\nNOT ACTIVATED"),
]):
    sx = 20 + i * (skip_w + 20)
    elements.append(rect_el(f"skip_{i}", sx, SKIP_Y + 54, skip_w, 100, C["skipped"][0], C["skipped"][1]))
    elements.append(text_el(f"skip_{i}_t", sx + 12, SKIP_Y + 66, skip_w - 24, 76,
                             f"{name}\n{desc}", "#9ca3af", 12))

# ─── METRICS PANEL ────────────────────────────────────────────────────────────
METRICS_Y = SKIP_Y + 174
elements.append(rect_el("metrics_bg", 20, METRICS_Y, 2600, 120, C["value"][0], C["value"][1]))
elements.append(text_el("metrics_t", 40, METRICS_Y + 10, 2560, 100,
    "E. RUNTIME METRICS\n"
    "Total Time: [X]s     Total Cost: $[X]     Total Tokens: [X]     "
    "Models: [list]     Tools: [X] modules     Artifacts: [X]     Plugins Skipped: [X]",
    "#f8fafc", 13))

# ─── VALUE PANEL ──────────────────────────────────────────────────────────────
VALUE_Y = METRICS_Y + 140
elements.append(rect_el("value_bg", 20, VALUE_Y, 2600, 180, C["value"][0], C["value"][1]))
elements.append(text_el("value_t", 40, VALUE_Y + 10, 2560, 160,
    "F. VALUE PANEL\n"
    "Artifacts Created: [list]     Decisions Produced: [list]     "
    "Knowledge Added: [list]     Repos Updated: [list]     "
    "Final Deliverable: [one sentence]",
    "#f8fafc", 13))

# ─── VERDICT ──────────────────────────────────────────────────────────────────
VERDICT_Y = VALUE_Y + 200
elements.append(rect_el("verdict_bg", 20, VERDICT_Y, 2600, 200, C["verdict"][0], C["verdict"][1]))
elements.append(text_el("verdict_t", 40, VERDICT_Y + 10, 2560, 180,
    "G. DID Y-OS CREATE VALUE?\n\n"
    "[YES / NO / AMBER]\n\n"
    "Explanation: [one paragraph]\n"
    "Where value was produced: [list]\n"
    "Time saved: [X] min vs manual     Cost saved: $[X] vs manual",
    "#f0fdf4", 14))

# ─── WITHOUT / WITH ───────────────────────────────────────────────────────────
COMP_Y = VERDICT_Y + 220
elements.append(rect_el("without_bg", 20, COMP_Y, 1270, 200, "#1c1917", "#78716c"))
elements.append(text_el("without_t", 40, COMP_Y + 10, 1230, 180,
    "H. WITHOUT Y-OS\n\n"
    "1. Manual search for context\n"
    "2. Copy/paste into LLM\n"
    "3. Ask LLM\n"
    "4. Manually save result\n"
    "5. No audit trail / No governance\n"
    "Time: ~[X] min     Cost: ~$[X]",
    "#d1d5db", 12))

elements.append(rect_el("with_bg", 1310, COMP_Y, 1310, 200, C["verdict"][0], C["verdict"][1]))
elements.append(text_el("with_t", 1330, COMP_Y + 10, 1270, 180,
    "H. WITH Y-OS\n\n"
    "1. Automatic context compilation\n"
    "2. Team routing to right expert\n"
    "3. Constitutional governance\n"
    "4. Artifact registration with lineage\n"
    "5. Memory update / Final answer\n"
    "Time: [X]s     Cost: $[X]",
    "#f0fdf4", 12))

# ─── ASSEMBLE ─────────────────────────────────────────────────────────────────
excalidraw = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": elements,
    "appState": {
        "gridSize": None,
        "viewBackgroundColor": C["bg"],
        "theme": "dark"
    },
    "files": {}
}

out = "/home/ubuntu/yreg/mission_trace_standard_001/value_trace_template.excalidraw"
with open(out, "w", encoding="utf-8") as f:
    json.dump(excalidraw, f, indent=2, ensure_ascii=False)

print(f"Template written: {out}")
print(f"Elements: {len(elements)}")
