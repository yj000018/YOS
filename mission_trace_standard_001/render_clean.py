#!/usr/bin/env python3
"""
Generates:
  value_trace_template_clean.png
  value_trace_template_clean.svg
  value_trace_template_clean.excalidraw (JSON)

Design: clean, sparse, dark background, large readable blocks,
        minimal text, no icons, no narrative. Reusable blank template.
"""
import json, uuid
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# ─── PALETTE ──────────────────────────────────────────────────────────────────
BG       = "#0f172a"
COLORS = {
    "human":      ("#1e3a8a", "#3b82f6"),
    "agent":      ("#4c1d95", "#8b5cf6"),
    "llm":        ("#14532d", "#22c55e"),
    "tool":       ("#7c2d12", "#f97316"),
    "governance": ("#7f1d1d", "#ef4444"),
    "artifact":   ("#713f12", "#eab308"),
    "skipped":    ("#1e293b", "#475569"),
    "metrics":    ("#0c1a2e", "#0ea5e9"),
    "value":      ("#0c1a2e", "#0ea5e9"),
    "verdict":    ("#052e16", "#4ade80"),
    "without":    ("#1c1917", "#57534e"),
    "with":       ("#052e16", "#4ade80"),
}
TEXT_BRIGHT = "#f8fafc"
TEXT_DIM    = "#94a3b8"
ARROW_COL   = "#fbbf24"

# ─── CANVAS ───────────────────────────────────────────────────────────────────
FIG_W, FIG_H, DPI = 32, 22, 130
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
ax.set_xlim(0, FIG_W); ax.set_ylim(0, FIG_H)
ax.set_aspect("equal"); ax.axis("off")
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)

def box(x, y, w, h, key, title, body_lines, title_size=11, body_size=9.5):
    bg, border = COLORS[key]
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.07",
                       lw=1.6, edgecolor=border, facecolor=bg, zorder=2)
    ax.add_patch(p)
    # title
    ax.text(x + w/2, y + h - 0.22, title, ha="center", va="top",
            color=TEXT_BRIGHT, fontsize=title_size, fontweight="bold", zorder=3)
    # thin divider
    ax.plot([x+0.12, x+w-0.12], [y+h-0.46, y+h-0.46],
            color=border, lw=0.8, alpha=0.5, zorder=3)
    # body
    for i, line in enumerate(body_lines):
        ax.text(x + 0.18, y + h - 0.62 - i*0.28, line,
                ha="left", va="top", color=TEXT_DIM,
                fontsize=body_size, zorder=3)

def arrow_h(x1, x2, y, label=""):
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="-|>", color=ARROW_COL, lw=1.6), zorder=4)
    if label:
        ax.text((x1+x2)/2, y+0.14, label, ha="center", va="bottom",
                color=ARROW_COL, fontsize=8, zorder=5,
                bbox=dict(boxstyle="round,pad=0.12", fc=BG, ec=ARROW_COL, lw=0.8))

# ══════════════════════════════════════════════════════════════════════════════
# TITLE
# ══════════════════════════════════════════════════════════════════════════════
ax.text(FIG_W/2, FIG_H - 0.28, "Y-OS  VALUE TRACE  —  TEMPLATE",
        ha="center", va="top", color=TEXT_BRIGHT, fontsize=20, fontweight="bold")
ax.text(FIG_W/2, FIG_H - 0.72, "MISSION-TRACE-STANDARD-001  |  Blank reusable template",
        ha="center", va="top", color=TEXT_DIM, fontsize=11)

# ══════════════════════════════════════════════════════════════════════════════
# LEGEND ROW
# ══════════════════════════════════════════════════════════════════════════════
LEGEND_Y = FIG_H - 1.25
legend_items = [
    ("Human",      "human"),
    ("Agent",      "agent"),
    ("LLM",        "llm"),
    ("Tool",       "tool"),
    ("Governance", "governance"),
    ("Artifact",   "artifact"),
    ("Skipped",    "skipped"),
]
LEG_W = (FIG_W - 0.4) / len(legend_items) - 0.15
for i, (label, key) in enumerate(legend_items):
    lx = 0.2 + i * (LEG_W + 0.15)
    bg, border = COLORS[key]
    p = FancyBboxPatch((lx, LEGEND_Y - 0.48), LEG_W, 0.44,
                       boxstyle="round,pad=0.05", lw=1.2,
                       edgecolor=border, facecolor=bg, zorder=3)
    ax.add_patch(p)
    ax.text(lx + LEG_W/2, LEGEND_Y - 0.26, label,
            ha="center", va="center", color=TEXT_BRIGHT,
            fontsize=10, fontweight="bold", zorder=4)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN FLOW — 7 columns
# ══════════════════════════════════════════════════════════════════════════════
FLOW_TOP = LEGEND_Y - 0.65
FLOW_H   = 6.8
COL_W    = (FIG_W - 0.4) / 7 - 0.18
COL_GAP  = 0.18

PLACEHOLDER = [
    "Role:",
    "Worker:",
    "Provider:",
    "Model:",
    "Tools:",
    "Input:",
    "Output:",
    "Artifact:",
    "Latency:",
    "Cost:",
]

flow_cols = [
    ("A. REQUEST",      "human"),
    ("B. ORCHESTRATOR", "agent"),
    ("C. WORKER",       "llm"),
    ("D. VALIDATOR",    "governance"),
    ("E. ARCHIVIST",    "tool"),
    ("F. MEMORY",       "tool"),
    ("G. DELIVERABLE",  "artifact"),
]

col_rights = []
for i, (title, key) in enumerate(flow_cols):
    bx = 0.2 + i * (COL_W + COL_GAP)
    by = FLOW_TOP - FLOW_H
    box(bx, by, COL_W, FLOW_H, key, title, PLACEHOLDER, title_size=11, body_size=9)
    col_rights.append(bx + COL_W)

# Arrows + handoff labels
handoff_labels = [
    "Request",
    "Context Pack",
    "Artifact",
    "Approved",
    "Registered",
    "Persisted",
]
for i in range(len(flow_cols) - 1):
    x1 = col_rights[i]
    x2 = 0.2 + (i+1) * (COL_W + COL_GAP)
    y_mid = FLOW_TOP - FLOW_H / 2
    arrow_h(x1, x2, y_mid, handoff_labels[i])

# ══════════════════════════════════════════════════════════════════════════════
# PLUGINS SKIPPED ROW
# ══════════════════════════════════════════════════════════════════════════════
SKIP_TOP = FLOW_TOP - FLOW_H - 0.35
SKIP_H   = 1.5
SKIP_W   = (FIG_W - 0.4) / 4 - 0.15

ax.text(FIG_W/2, SKIP_TOP - 0.05,
        "PLUGINS SKIPPED", ha="center", va="top",
        color=TEXT_DIM, fontsize=10, fontweight="bold")

skip_plugins = [
    ("ODT",             "Organizational Digital Twin"),
    ("STRATEGIC INTEL", "Strategic Intelligence"),
    ("SIMULATION",      "Time Machine / Counterfactual"),
    ("OBSERVABILITY",   "Advanced Observability"),
]
for i, (name, desc) in enumerate(skip_plugins):
    sx = 0.2 + i * (SKIP_W + 0.15)
    sy = SKIP_TOP - 0.35 - SKIP_H
    box(sx, sy, SKIP_W, SKIP_H, "skipped", name,
        [desc, "", "NOT ACTIVATED"], title_size=10, body_size=9)

# ══════════════════════════════════════════════════════════════════════════════
# RUNTIME METRICS PANEL
# ══════════════════════════════════════════════════════════════════════════════
METRICS_TOP = SKIP_TOP - 0.35 - SKIP_H - 0.25
METRICS_H   = 1.6
box(0.2, METRICS_TOP - METRICS_H, FIG_W - 0.4, METRICS_H,
    "metrics", "E. RUNTIME METRICS",
    [
        "Total Time:          ___",
        "Total Cost:          ___",
        "Total Tokens:        ___",
        "Models Used:         ___",
        "Tools Used:          ___",
        "Artifacts Created:   ___",
        "Plugins Skipped:     ___",
    ],
    title_size=11, body_size=9.5)

# ══════════════════════════════════════════════════════════════════════════════
# VALUE PANEL
# ══════════════════════════════════════════════════════════════════════════════
VALUE_TOP = METRICS_TOP - METRICS_H - 0.25
VALUE_H   = 1.8
box(0.2, VALUE_TOP - VALUE_H, FIG_W - 0.4, VALUE_H,
    "value", "F. VALUE PANEL",
    [
        "Artifacts Created:    ___",
        "Decisions Produced:   ___",
        "Knowledge Added:      ___",
        "Repos Updated:        ___",
        "Final Deliverable:    ___",
    ],
    title_size=11, body_size=9.5)

# ══════════════════════════════════════════════════════════════════════════════
# FINAL VERDICT
# ══════════════════════════════════════════════════════════════════════════════
VERDICT_TOP = VALUE_TOP - VALUE_H - 0.25
VERDICT_H   = 1.8
box(0.2, VERDICT_TOP - VERDICT_H, FIG_W - 0.4, VERDICT_H,
    "verdict", "G. DID Y-OS CREATE VALUE?",
    [
        "Verdict:   YES  /  NO  /  AMBER",
        "Reason:    ___",
        "",
        "Value produced at:   ___",
        "Time saved:          ___     Cost saved:   ___",
    ],
    title_size=12, body_size=9.5)

# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM COMPARISON
# ══════════════════════════════════════════════════════════════════════════════
COMP_TOP = VERDICT_TOP - VERDICT_H - 0.25
COMP_H   = 2.2
half_w   = (FIG_W - 0.55) / 2

box(0.2, COMP_TOP - COMP_H, half_w, COMP_H,
    "without", "H. WITHOUT Y-OS",
    [
        "1. Manual search for context",
        "2. Copy / paste into LLM",
        "3. Ask LLM",
        "4. Manually save result",
        "5. No audit trail",
        "6. No governance",
        "",
        "Time: ~__ min    Cost: ~$__",
    ],
    title_size=11, body_size=9.5)

box(0.35 + half_w, COMP_TOP - COMP_H, half_w, COMP_H,
    "with", "H. WITH Y-OS",
    [
        "1. Automatic context compilation",
        "2. Team routing to right expert",
        "3. Constitutional governance",
        "4. Artifact registration + lineage",
        "5. Memory update",
        "6. Final answer returned",
        "",
        "Time: __s    Cost: $__",
    ],
    title_size=11, body_size=9.5)

# ─── SAVE ─────────────────────────────────────────────────────────────────────
base = "/home/ubuntu/yreg/mission_trace_standard_001/value_trace_template_clean"
plt.tight_layout(pad=0)
plt.savefig(base + ".png", format="png", dpi=DPI, bbox_inches="tight",
            facecolor=fig.get_facecolor())
plt.savefig(base + ".svg", format="svg", dpi=DPI, bbox_inches="tight",
            facecolor=fig.get_facecolor())
plt.close()
print(f"PNG: {base}.png")
print(f"SVG: {base}.svg")

# ─── EXCALIDRAW JSON ──────────────────────────────────────────────────────────
# Build a clean Excalidraw JSON matching the same layout
def eid(): return str(uuid.uuid4())[:8]

def ex_rect(id_, x, y, w, h, bg, stroke):
    return {"id": id_, "type": "rectangle",
            "x": x, "y": y, "width": w, "height": h,
            "angle": 0, "strokeColor": stroke, "backgroundColor": bg,
            "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
            "roughness": 0, "opacity": 100, "groupIds": [],
            "roundness": {"type": 3}, "isDeleted": False,
            "boundElements": [], "updated": 1, "link": None, "locked": False}

def ex_text(id_, x, y, w, h, text, color="#f8fafc", size=14):
    return {"id": id_, "type": "text",
            "x": x, "y": y, "width": w, "height": h,
            "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
            "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
            "roughness": 0, "opacity": 100, "groupIds": [],
            "roundness": None, "isDeleted": False,
            "boundElements": [], "updated": 1, "link": None, "locked": False,
            "text": text, "fontSize": size, "fontFamily": 1,
            "textAlign": "left", "verticalAlign": "top",
            "containerId": None, "originalText": text,
            "lineHeight": 1.4, "baseline": size}

def ex_arrow(id_, x1, y1, x2, y2, label=""):
    return {"id": id_, "type": "arrow",
            "x": x1, "y": y1, "width": x2-x1, "height": 0,
            "angle": 0, "strokeColor": "#fbbf24", "backgroundColor": "transparent",
            "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
            "roughness": 0, "opacity": 100, "groupIds": [],
            "roundness": {"type": 2}, "isDeleted": False,
            "boundElements": [], "updated": 1, "link": None, "locked": False,
            "points": [[0, 0], [x2-x1, 0]],
            "lastCommittedPoint": None, "startBinding": None, "endBinding": None,
            "startArrowhead": None, "endArrowhead": "arrow"}

els = []

# Scale: 1 matplotlib unit ≈ 60 excalidraw units
S = 60
OX, OY = 20, 20   # offset

def m2e(x, y, w, h):
    """Convert matplotlib coords to Excalidraw (flip y)."""
    return (int(x*S)+OX, int((FIG_H-y-h)*S)+OY, int(w*S), int(h*S))

# Title
ex_x, ex_y, ex_w, ex_h = m2e(0.2, FIG_H-0.9, FIG_W-0.4, 0.7)
els.append(ex_rect(eid(), ex_x, ex_y, ex_w, ex_h, "#0f172a", "#334155"))
els.append(ex_text(eid(), ex_x+10, ex_y+10, ex_w-20, ex_h-20,
    "Y-OS  VALUE TRACE  —  TEMPLATE\nMISSION-TRACE-STANDARD-001  |  Blank reusable template",
    "#f8fafc", 18))

# Legend
LEG_H_m = 0.48
LEG_Y_m = FIG_H - 1.25
for i, (label, key) in enumerate(legend_items):
    lx_m = 0.2 + i * (LEG_W + 0.15)
    bg, border = COLORS[key]
    ex_x, ex_y, ex_w, ex_h = m2e(lx_m, LEG_Y_m - LEG_H_m, LEG_W, LEG_H_m)
    els.append(ex_rect(eid(), ex_x, ex_y, ex_w, ex_h, bg, border))
    els.append(ex_text(eid(), ex_x+10, ex_y+8, ex_w-20, ex_h-16, label, "#f8fafc", 13))

# Main flow columns
for i, (title, key) in enumerate(flow_cols):
    bx_m = 0.2 + i * (COL_W + COL_GAP)
    by_m = FLOW_TOP - FLOW_H
    bg, border = COLORS[key]
    ex_x, ex_y, ex_w, ex_h = m2e(bx_m, by_m, COL_W, FLOW_H)
    els.append(ex_rect(eid(), ex_x, ex_y, ex_w, ex_h, bg, border))
    body = "\n".join([title, "─"*20] + PLACEHOLDER)
    els.append(ex_text(eid(), ex_x+12, ex_y+12, ex_w-24, ex_h-24, body, "#f8fafc", 13))

# Arrows
for i in range(len(flow_cols)-1):
    x1_m = 0.2 + (i+1) * (COL_W + COL_GAP) - COL_GAP
    x2_m = 0.2 + (i+1) * (COL_W + COL_GAP)
    y_m  = FLOW_TOP - FLOW_H/2
    ex_x1 = int(x1_m*S)+OX
    ex_x2 = int(x2_m*S)+OX
    ex_y_a = int((FIG_H - y_m)*S)+OY
    els.append(ex_arrow(eid(), ex_x1, ex_y_a, ex_x2, ex_y_a, handoff_labels[i]))

# Plugins skipped
for i, (name, desc) in enumerate(skip_plugins):
    sx_m = 0.2 + i * (SKIP_W + 0.15)
    sy_m = SKIP_TOP - 0.35 - SKIP_H
    bg, border = COLORS["skipped"]
    ex_x, ex_y, ex_w, ex_h = m2e(sx_m, sy_m, SKIP_W, SKIP_H)
    els.append(ex_rect(eid(), ex_x, ex_y, ex_w, ex_h, bg, border))
    els.append(ex_text(eid(), ex_x+12, ex_y+12, ex_w-24, ex_h-24,
                       f"{name}\n{desc}\n\nNOT ACTIVATED", "#94a3b8", 13))

# Metrics
bg, border = COLORS["metrics"]
ex_x, ex_y, ex_w, ex_h = m2e(0.2, METRICS_TOP-METRICS_H, FIG_W-0.4, METRICS_H)
els.append(ex_rect(eid(), ex_x, ex_y, ex_w, ex_h, bg, border))
els.append(ex_text(eid(), ex_x+12, ex_y+12, ex_w-24, ex_h-24,
    "E. RUNTIME METRICS\n" + "─"*40 + "\n"
    "Total Time: ___     Total Cost: ___     Total Tokens: ___\n"
    "Models Used: ___     Tools Used: ___     Artifacts Created: ___     Plugins Skipped: ___",
    "#f8fafc", 13))

# Value panel
ex_x, ex_y, ex_w, ex_h = m2e(0.2, VALUE_TOP-VALUE_H, FIG_W-0.4, VALUE_H)
els.append(ex_rect(eid(), ex_x, ex_y, ex_w, ex_h, bg, border))
els.append(ex_text(eid(), ex_x+12, ex_y+12, ex_w-24, ex_h-24,
    "F. VALUE PANEL\n" + "─"*40 + "\n"
    "Artifacts Created: ___\nDecisions Produced: ___\n"
    "Knowledge Added: ___\nRepos Updated: ___\nFinal Deliverable: ___",
    "#f8fafc", 13))

# Verdict
bg_v, border_v = COLORS["verdict"]
ex_x, ex_y, ex_w, ex_h = m2e(0.2, VERDICT_TOP-VERDICT_H, FIG_W-0.4, VERDICT_H)
els.append(ex_rect(eid(), ex_x, ex_y, ex_w, ex_h, bg_v, border_v))
els.append(ex_text(eid(), ex_x+12, ex_y+12, ex_w-24, ex_h-24,
    "G. DID Y-OS CREATE VALUE?\n" + "─"*40 + "\n"
    "Verdict:  YES  /  NO  /  AMBER\n"
    "Reason: ___\n"
    "Value produced at: ___     Time saved: ___     Cost saved: ___",
    "#f0fdf4", 14))

# Without / With
bg_wo, border_wo = COLORS["without"]
bg_wi, border_wi = COLORS["with"]
ex_x, ex_y, ex_w, ex_h = m2e(0.2, COMP_TOP-COMP_H, half_w, COMP_H)
els.append(ex_rect(eid(), ex_x, ex_y, ex_w, ex_h, bg_wo, border_wo))
els.append(ex_text(eid(), ex_x+12, ex_y+12, ex_w-24, ex_h-24,
    "H. WITHOUT Y-OS\n" + "─"*30 + "\n"
    "1. Manual search for context\n2. Copy / paste into LLM\n3. Ask LLM\n"
    "4. Manually save result\n5. No audit trail\n6. No governance\n\n"
    "Time: ~__ min     Cost: ~$__",
    "#d1d5db", 13))
ex_x2, ex_y2, ex_w2, ex_h2 = m2e(0.35+half_w, COMP_TOP-COMP_H, half_w, COMP_H)
els.append(ex_rect(eid(), ex_x2, ex_y2, ex_w2, ex_h2, bg_wi, border_wi))
els.append(ex_text(eid(), ex_x2+12, ex_y2+12, ex_w2-24, ex_h2-24,
    "H. WITH Y-OS\n" + "─"*30 + "\n"
    "1. Automatic context compilation\n2. Team routing to right expert\n"
    "3. Constitutional governance\n4. Artifact registration + lineage\n"
    "5. Memory update\n6. Final answer returned\n\n"
    "Time: __s     Cost: $__",
    "#f0fdf4", 13))

excalidraw = {
    "type": "excalidraw", "version": 2,
    "source": "https://excalidraw.com",
    "elements": els,
    "appState": {"gridSize": None, "viewBackgroundColor": BG, "theme": "dark"},
    "files": {}
}
out_ex = base + ".excalidraw"
with open(out_ex, "w", encoding="utf-8") as f:
    json.dump(excalidraw, f, indent=2, ensure_ascii=False)
print(f"Excalidraw: {out_ex}  ({len(els)} elements)")
