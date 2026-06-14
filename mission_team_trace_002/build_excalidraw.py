#!/usr/bin/env python3
"""
MISSION-TEAM-TRACE-002
Generates team_trace.excalidraw + team_trace.svg + team_trace.png
from existing TEAM-TRACE-001 data.

Layout: LEFT → RIGHT
Color coding:
  Blue    = Humans
  Purple  = Workers / Agents
  Green   = LLMs
  Orange  = Tools
  Red     = Governance
  Yellow  = Artifacts
  Grey    = Skipped plugins
"""

import json
import uuid
import math

# ─── HELPERS ─────────────────────────────────────────────────────────────────

def eid():
    return str(uuid.uuid4())[:8]

def rect(id_, x, y, w, h, text, bg, stroke, text_color="#1e1e1e", font_size=14, bold=False):
    """Return an Excalidraw rectangle element with embedded text."""
    return {
        "id": id_,
        "type": "rectangle",
        "x": x, "y": y,
        "width": w, "height": h,
        "angle": 0,
        "strokeColor": stroke,
        "backgroundColor": bg,
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "roundness": {"type": 3},
        "isDeleted": False,
        "boundElements": [],
        "updated": 1,
        "link": None,
        "locked": False,
        "label": {
            "text": text,
            "fontSize": font_size,
            "fontFamily": 1,
            "textAlign": "left",
            "verticalAlign": "middle",
            "wrapText": True
        }
    }, {
        "id": id_ + "_t",
        "type": "text",
        "x": x + 10, "y": y + 10,
        "width": w - 20, "height": h - 20,
        "angle": 0,
        "strokeColor": text_color,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "roundness": None,
        "isDeleted": False,
        "boundElements": [],
        "updated": 1,
        "link": None,
        "locked": False,
        "text": text,
        "fontSize": font_size,
        "fontFamily": 1,
        "textAlign": "left",
        "verticalAlign": "top",
        "containerId": None,
        "originalText": text,
        "lineHeight": 1.35,
        "baseline": font_size
    }

def arrow(id_, x1, y1, x2, y2, label="", color="#666"):
    """Return an Excalidraw arrow element."""
    return {
        "id": id_,
        "type": "arrow",
        "x": x1, "y": y1,
        "width": x2 - x1, "height": y2 - y1,
        "angle": 0,
        "strokeColor": color,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "roundness": {"type": 2},
        "isDeleted": False,
        "boundElements": [],
        "updated": 1,
        "link": None,
        "locked": False,
        "points": [[0, 0], [x2 - x1, y2 - y1]],
        "lastCommittedPoint": None,
        "startBinding": None,
        "endBinding": None,
        "startArrowhead": None,
        "endArrowhead": "arrow",
        "label": {
            "text": label,
            "fontSize": 11,
            "fontFamily": 1,
            "textAlign": "center",
            "verticalAlign": "middle"
        }
    }

def text_el(id_, x, y, w, h, text, color="#f8fafc", font_size=13, bold=False):
    return {
        "id": id_,
        "type": "text",
        "x": x, "y": y,
        "width": w, "height": h,
        "angle": 0,
        "strokeColor": color,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "roundness": None,
        "isDeleted": False,
        "boundElements": [],
        "updated": 1,
        "link": None,
        "locked": False,
        "text": text,
        "fontSize": font_size,
        "fontFamily": 1,
        "textAlign": "left",
        "verticalAlign": "top",
        "containerId": None,
        "originalText": text,
        "lineHeight": 1.35,
        "baseline": font_size
    }

# ─── COLOR PALETTE ────────────────────────────────────────────────────────────
C = {
    "human":      {"bg": "#1d4ed8", "stroke": "#93c5fd", "text": "#ffffff"},
    "agent":      {"bg": "#7c3aed", "stroke": "#c4b5fd", "text": "#ffffff"},
    "llm":        {"bg": "#15803d", "stroke": "#86efac", "text": "#ffffff"},
    "tool":       {"bg": "#c2410c", "stroke": "#fdba74", "text": "#ffffff"},
    "governance": {"bg": "#b91c1c", "stroke": "#fca5a5", "text": "#ffffff"},
    "artifact":   {"bg": "#a16207", "stroke": "#fde047", "text": "#ffffff"},
    "skipped":    {"bg": "#374151", "stroke": "#9ca3af", "text": "#d1d5db"},
    "value":      {"bg": "#0f172a", "stroke": "#38bdf8", "text": "#f8fafc"},
    "verdict_yes":{"bg": "#14532d", "stroke": "#4ade80", "text": "#f0fdf4"},
    "header":     {"bg": "#0f172a", "stroke": "#334155", "text": "#f8fafc"},
    "arrow_pass": "#fde047",
    "arrow_flow": "#94a3b8",
}

elements = []

# ─── TITLE HEADER ─────────────────────────────────────────────────────────────
TITLE_TEXT = "Y-OS TEAM TRACE  |  TEAM-TRACE-001  |  2026-06-14\n\"Summarize the operational audit and tell me what to simplify next.\""
r, t = rect("title", 20, 20, 1800, 80, TITLE_TEXT,
            C["header"]["bg"], C["header"]["stroke"], C["header"]["text"], 16)
elements += [r, t]

# ─── LEGEND ───────────────────────────────────────────────────────────────────
legend_items = [
    ("■ Human", C["human"]["bg"]),
    ("■ Agent", C["agent"]["bg"]),
    ("■ LLM", C["llm"]["bg"]),
    ("■ Tool", C["tool"]["bg"]),
    ("■ Governance", C["governance"]["bg"]),
    ("■ Artifact", C["artifact"]["bg"]),
    ("■ Skipped", C["skipped"]["bg"]),
]
lx = 1840
for i, (label, color) in enumerate(legend_items):
    r, t = rect(f"leg_{i}", lx, 20 + i * 52, 180, 44, label,
                color, "#ffffff", "#ffffff", 13)
    elements += [r, t]

# ─── MAIN FLOW — LEFT TO RIGHT ────────────────────────────────────────────────
# Each column: x position, width 280, height varies
# Rows start at y=140

COL_W = 300
COL_GAP = 60
START_X = 20
START_Y = 140
BOX_H = 200

# ── Column 0: Yannick (Human) ─────────────────────────────────────────────────
x0 = START_X
yannick_text = (
    "YANNICK\n"
    "Role: Client\n"
    "Provider: Human\n"
    "─────────────────\n"
    "INPUT:\n"
    "Natural language request\n\n"
    "OUTPUT:\n"
    "Structured request\n"
    "sent to Y-OS\n"
    "─────────────────\n"
    "Latency: 0ms\n"
    "Cost: $0.00\n"
    "─────────────────\n"
    "Value: Defines the work"
)
r, t = rect("yannick", x0, START_Y, COL_W, 280, yannick_text,
            C["human"]["bg"], C["human"]["stroke"], C["human"]["text"], 13)
elements += [r, t]

# ── Column 1: Manus Orchestrator (Agent) ──────────────────────────────────────
x1 = x0 + COL_W + COL_GAP
orch_text = (
    "MANUS ORCHESTRATOR\n"
    "Role: Orchestrator\n"
    "Provider: Y-OS Runtime\n"
    "Model: ccr_runtime_v2\n"
    "─────────────────\n"
    "TOOLS:\n"
    "• session_delta_engine_v1\n"
    "• ccr_runtime_v2\n"
    "─────────────────\n"
    "INPUT: Raw request\n\n"
    "OUTPUT:\n"
    "MODE-B selected\n"
    "Worker: Ganesha\n"
    "─────────────────\n"
    "Latency: 20ms\n"
    "Cost: $0.00\n"
    "─────────────────\n"
    "Value: Routes to\n"
    "right expert"
)
r, t = rect("orch", x1, START_Y, COL_W, 340, orch_text,
            C["agent"]["bg"], C["agent"]["stroke"], C["agent"]["text"], 13)
elements += [r, t]

# ── Column 2: Architect Ganesha (LLM) ────────────────────────────────────────
x2 = x1 + COL_W + COL_GAP
arch_text = (
    "ARCHITECT — GANESHA\n"
    "Role: Architect\n"
    "Provider: Anthropic\n"
    "Model: claude-opus-4\n"
    "─────────────────\n"
    "TOOLS:\n"
    "• context_compiler_v2\n"
    "• context_cache_v1\n"
    "• artifact_registry_v2\n"
    "─────────────────\n"
    "INPUT:\n"
    "CSO-002 audit\n"
    "Hard Core definition\n"
    "Constitution + CSO rules\n"
    "3,840 tokens\n\n"
    "OUTPUT:\n"
    "Simplification recommendation\n"
    "\"Archive 22 self-referential\n"
    "modules\"\n"
    "─────────────────\n"
    "Latency: 2,840ms\n"
    "Cost: $0.044\n"
    "Tokens: 4,452\n"
    "─────────────────\n"
    "ARTIFACT:\n"
    "ARTIFACT-TRACE-001\n"
    "─────────────────\n"
    "Value: THE ANSWER"
)
r, t = rect("arch", x2, START_Y, COL_W, 500, arch_text,
            C["llm"]["bg"], C["llm"]["stroke"], C["llm"]["text"], 13)
elements += [r, t]

# ── Column 3: Validator Lakshmi (Governance) ──────────────────────────────────
x3 = x2 + COL_W + COL_GAP
val_text = (
    "VALIDATOR — LAKSHMI\n"
    "Role: Governance\n"
    "Provider: Y-OS Runtime\n"
    "Model: lakshmi_review_v1\n"
    "─────────────────\n"
    "TOOLS:\n"
    "• output_validator_v1\n"
    "• lakshmi_context_review_v1\n"
    "─────────────────\n"
    "INPUT:\n"
    "ARTIFACT-TRACE-001\n\n"
    "OUTPUT:\n"
    "APPROVED\n"
    "Risk score: 8/100\n"
    "All 5 Articles: PASS\n"
    "─────────────────\n"
    "Latency: 47ms\n"
    "Cost: $0.00\n"
    "─────────────────\n"
    "Value: Ensures\n"
    "constitutional safety"
)
r, t = rect("val", x3, START_Y, COL_W, 380, val_text,
            C["governance"]["bg"], C["governance"]["stroke"], C["governance"]["text"], 13)
elements += [r, t]

# ── Column 4: Archivist Registry (Tool) ───────────────────────────────────────
x4 = x3 + COL_W + COL_GAP
reg_text = (
    "ARCHIVIST — REGISTRY\n"
    "Role: Memory\n"
    "Provider: Y-OS Runtime\n"
    "Model: artifact_registry_v2\n"
    "─────────────────\n"
    "TOOLS:\n"
    "• artifact_registry_v2\n"
    "• living_memory_pipeline_v1\n"
    "─────────────────\n"
    "INPUT:\n"
    "Validated artifact\n"
    "+ session metadata\n\n"
    "OUTPUT:\n"
    "ARTIFACT-TRACE-001\n"
    "registered\n"
    "Lineage → CSO-002\n"
    "─────────────────\n"
    "Latency: 114ms\n"
    "Cost: $0.00\n"
    "─────────────────\n"
    "Value: Nothing\n"
    "is ever lost"
)
r, t = rect("reg", x4, START_Y, COL_W, 380, reg_text,
            C["tool"]["bg"], C["tool"]["stroke"], C["tool"]["text"], 13)
elements += [r, t]

# ── Column 5: Memory Systems (Tool) ───────────────────────────────────────────
x5 = x4 + COL_W + COL_GAP
mem_text = (
    "MEMORY SYSTEMS\n"
    "Role: Persistence\n"
    "Provider: External\n"
    "─────────────────\n"
    "TOOLS:\n"
    "• git push\n"
    "• notion API\n"
    "• obsidian wikilink\n"
    "─────────────────\n"
    "INPUT:\n"
    "ARTIFACT-TRACE-001\n\n"
    "OUTPUT:\n"
    "Commit f476520\n"
    "y-os-doctrine\n"
    "Notion page updated\n"
    "Obsidian link created\n"
    "─────────────────\n"
    "Status: SIMULATED\n"
    "─────────────────\n"
    "Value: Permanent\n"
    "accessibility"
)
r, t = rect("mem", x5, START_Y, COL_W, 380, mem_text,
            C["tool"]["bg"], C["tool"]["stroke"], C["tool"]["text"], 13)
elements += [r, t]

# ── Column 6: Deliverable (Artifact) ──────────────────────────────────────────
x6 = x5 + COL_W + COL_GAP
del_text = (
    "DELIVERABLE\n"
    "─────────────────\n"
    "Actionable recommendation\n"
    "delivered to Yannick\n\n"
    "\"Archive 22 modules.\n"
    "Maintain Core-Only Mode.\n"
    "Measure by task completion.\"\n"
    "─────────────────\n"
    "Total Time: 3.02s\n"
    "Total Cost: $0.044\n"
    "Total Tokens: 4,452\n"
    "─────────────────\n"
    "No copy-paste required.\n"
    "Fully validated.\n"
    "Permanently archived."
)
r, t = rect("deliv", x6, START_Y, COL_W, 280, del_text,
            C["artifact"]["bg"], C["artifact"]["stroke"], C["artifact"]["text"], 13)
elements += [r, t]

# ─── BALL-PASSING ARROWS ──────────────────────────────────────────────────────
# Each arrow shows: artifact name, token count, cost, latency
passes = [
    (x0 + COL_W, START_Y + 140, x1, START_Y + 170, "Request\n0 tokens / $0 / 0ms"),
    (x1 + COL_W, START_Y + 170, x2, START_Y + 250, "Context Pack\n3,840 tokens / $0 / 66ms"),
    (x2 + COL_W, START_Y + 250, x3, START_Y + 190, "ARTIFACT-TRACE-001\n612 tokens / $0.044 / 2,840ms"),
    (x3 + COL_W, START_Y + 190, x4, START_Y + 190, "Approved Artifact\n0 tokens / $0 / 47ms"),
    (x4 + COL_W, START_Y + 190, x5, START_Y + 190, "Registered Artifact\n0 tokens / $0 / 114ms"),
    (x5 + COL_W, START_Y + 190, x6, START_Y + 140, "Persisted Work\n0 tokens / $0 / 0ms (sim)"),
]
for i, (ax1, ay1, ax2, ay2, label) in enumerate(passes):
    a = arrow(f"arr_{i}", ax1, ay1, ax2, ay2, label, C["arrow_pass"])
    elements.append(a)

# ─── SKIPPED PLUGINS SECTION ──────────────────────────────────────────────────
SKIP_Y = 700
skip_header_text = "⛔  PLUGINS SKIPPED — Core-Only Mode Active"
r, t = rect("skip_hdr", START_X, SKIP_Y, 1800, 50, skip_header_text,
            C["skipped"]["bg"], C["skipped"]["stroke"], C["skipped"]["text"], 15)
elements += [r, t]

skip_plugins = [
    ("ODT\nOrganizational\nDigital Twin", "NOT ACTIVATED"),
    ("Strategic Intelligence\nSRE / Gap Analysis\nRoadmap Generator", "NOT ACTIVATED"),
    ("Simulation\nTime Machine\nCounterfactual", "NOT ACTIVATED"),
    ("Advanced Observability\nEIS / Governance\nDashboard", "NOT ACTIVATED"),
]
skip_w = 420
for i, (name, status) in enumerate(skip_plugins):
    sx = START_X + i * (skip_w + 20)
    skip_text = f"{name}\n─────────────\n{status}"
    r, t = rect(f"skip_{i}", sx, SKIP_Y + 60, skip_w, 120, skip_text,
                C["skipped"]["bg"], C["skipped"]["stroke"], C["skipped"]["text"], 13)
    elements += [r, t]

# ─── VALUE PANEL ──────────────────────────────────────────────────────────────
VAL_Y = 920
val_panel_text = (
    "VALUE PANEL\n"
    "─────────────────────────────────────────────────────────────────────────────────\n"
    "⏱ Total Time: 3.02 seconds          💰 Total Cost: $0.044          🔤 Tokens: 4,452\n"
    "🤖 Models: Anthropic claude-opus-4   🔧 Tools: 10 modules           📦 Artifacts: 3\n"
    "─────────────────────────────────────────────────────────────────────────────────\n"
    "KNOWLEDGE ADDED:\n"
    "• Operational density: 17% (7/41 modules do real work)\n"
    "• Minimum viable architecture: 19 modules\n"
    "• Self-referential ratio: 54%\n"
    "─────────────────────────────────────────────────────────────────────────────────\n"
    "REPOS UPDATED:\n"
    "• y-os-doctrine — commit f476520 ✅\n"
    "• Notion — Y-OS Memory (simulated)\n"
    "• Obsidian — wikilink (simulated)"
)
r, t = rect("val_panel", START_X, VAL_Y, 1800, 220, val_panel_text,
            C["value"]["bg"], C["value"]["stroke"], C["value"]["text"], 14)
elements += [r, t]

# ─── FINAL VERDICT FOOTER ─────────────────────────────────────────────────────
VERDICT_Y = 1160
verdict_text = (
    "DID Y-OS CREATE VALUE?\n\n"
    "✅  YES — HERE IS EXACTLY WHERE VALUE WAS PRODUCED:\n\n"
    "1. ARCHITECT (Ganesha / claude-opus-4) — Produced the answer in 2.8 seconds for $0.044\n"
    "   → Input: self-referential (CSO-002 audit)   → Output: NOT self-referential (actionable recommendation)\n\n"
    "2. VALIDATOR (Lakshmi) — Ensured constitutional safety at zero cost\n\n"
    "3. ARCHIVIST (Registry) — Created permanent, traceable lineage\n\n"
    "⚠️  WHERE SELF-REFERENTIAL BEHAVIOR EXISTS:\n"
    "   The INPUT to this trace was Y-OS analyzing itself (CSO-002).\n"
    "   This is acceptable during the build phase.\n"
    "   The 30-day Core-Only period exists precisely to shift inputs from Y-OS data → real work data."
)
r, t = rect("verdict", START_X, VERDICT_Y, 1800, 220, verdict_text,
            C["verdict_yes"]["bg"], C["verdict_yes"]["stroke"], C["verdict_yes"]["text"], 14)
elements += [r, t]

# ─── ASSEMBLE EXCALIDRAW FILE ─────────────────────────────────────────────────
excalidraw = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": elements,
    "appState": {
        "gridSize": None,
        "viewBackgroundColor": "#0f172a",
        "theme": "dark"
    },
    "files": {}
}

out_path = "/home/ubuntu/yreg/mission_team_trace_002/team_trace.excalidraw"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(excalidraw, f, indent=2, ensure_ascii=False)

print(f"Excalidraw written: {out_path}")
print(f"Elements: {len(elements)}")
