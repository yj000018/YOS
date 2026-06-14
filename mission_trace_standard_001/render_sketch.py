#!/usr/bin/env python3
"""
Y-OS TEAM TRACE — Sketch/Consulting Edition
Matches the reference image exactly:
- White background, hand-drawn sketch feel (xkcd style)
- 9 team member columns with numbered headers + role icons
- Artifact handoffs row below columns
- 3 synchronized views (Architecture / Team / Value)
- Right-side Runtime Metrics panel
- "DID Y-OS CREATE VALUE?" verdict box
- WITHOUT vs WITH Y-OS comparison at bottom
- Plugins NOT ACTIVATED panel on left
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as pe
import numpy as np

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.spines.left": False, "axes.spines.bottom": False,
})

# ─── PALETTE ──────────────────────────────────────────────────────────────────
WHITE   = "#ffffff"
CREAM   = "#fafaf8"
LIGHT   = "#f5f5f0"
BORDER  = "#333333"
DARK    = "#111111"
MID     = "#444444"
DIM     = "#888888"
LIGHT_BORDER = "#aaaaaa"

# Accent colors matching reference
BLUE    = "#1a4fa0"   # Yannick / human
PURPLE  = "#6b3fa0"   # Architect / Ganesha
TEAL    = "#1a7a6e"   # Researcher / Builder
ORANGE  = "#c85a00"   # Validator / Lakshmi
AMBER   = "#b87800"   # Deliverable / Artifact
GREEN   = "#1a6e2e"   # Value / YES verdict
RED     = "#c0392b"   # Plugins skipped / WITHOUT
GREY    = "#666666"   # Inactive

# Column accent colors (matching reference)
COL_ACCENTS = [BLUE, MID, PURPLE, TEAL, TEAL, TEAL, ORANGE, MID, AMBER]

# ─── CANVAS ───────────────────────────────────────────────────────────────────
FIG_W, FIG_H = 38, 26
DPI = 130
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
ax.set_xlim(0, FIG_W); ax.set_ylim(0, FIG_H)
ax.set_aspect("equal"); ax.axis("off")
fig.patch.set_facecolor(WHITE); ax.set_facecolor(WHITE)

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def rbox(x, y, w, h, fc=WHITE, ec=BORDER, lw=1.2, alpha=1.0, zorder=2, radius=0.15):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0.06",
                       lw=lw, edgecolor=ec, facecolor=fc, alpha=alpha, zorder=zorder)
    ax.add_patch(p)

def t(x, y, s, c=DARK, sz=9, w="normal", ha="left", va="top", z=5, wrap=False):
    ax.text(x, y, s, color=c, fontsize=sz, fontweight=w,
            ha=ha, va=va, zorder=z, wrap=wrap)

def arrow(x1, x2, y, color=BLUE, lw=1.8, label="", label_color=None):
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                mutation_scale=14), zorder=6)
    if label:
        mx = (x1+x2)/2
        lc = label_color or color
        ax.text(mx, y+0.13, label, ha="center", va="bottom",
                color=lc, fontsize=7.5, fontweight="bold", zorder=7,
                bbox=dict(boxstyle="round,pad=0.12", fc=WHITE, ec=lc, lw=0.8))

def hline(x1, x2, y, c=BORDER, lw=0.7):
    ax.plot([x1, x2], [y, y], color=c, lw=lw, zorder=3)

def section_header(x, y, w, label, color):
    rbox(x, y-0.32, w, 0.32, fc=color, ec=color, lw=0, zorder=4)
    t(x+w/2, y-0.02, label, c=WHITE, sz=9, w="bold", ha="center", va="top", z=5)

def icon_circle(cx, cy, r, color, symbol, sz=12):
    circ = plt.Circle((cx, cy), r, fc=color, ec=color, lw=0, zorder=6)
    ax.add_patch(circ)
    t(cx, cy+0.02, symbol, c=WHITE, sz=sz, w="bold", ha="center", va="center", z=7)

# ══════════════════════════════════════════════════════════════════════════════
# TITLE AREA
# ══════════════════════════════════════════════════════════════════════════════
t(FIG_W/2, FIG_H-0.25, "Y-OS TEAM TRACE — EXECUTION TRACE",
  c=DARK, sz=20, w="bold", ha="center")
t(FIG_W/2, FIG_H-0.75, "Mission: WORK-TRACE-001  •  Date: 2026-06-14",
  c=DIM, sz=10, ha="center")
t(FIG_W-0.3, FIG_H-0.25, "TRACE ID: TRACE-001-EXAMPLE",
  c=BLUE, sz=9, w="bold", ha="right")

# ══════════════════════════════════════════════════════════════════════════════
# YANNICK REQUEST BOX (left of columns)
# ══════════════════════════════════════════════════════════════════════════════
REQ_X, REQ_Y = 0.25, FIG_H - 1.2
REQ_W, REQ_H = 2.8, 3.2
rbox(REQ_X, REQ_Y - REQ_H, REQ_W, REQ_H, fc=CREAM, ec=BLUE, lw=2, zorder=3)
t(REQ_X+REQ_W/2, REQ_Y-0.18, "YANNICK", c=BLUE, sz=11, w="bold", ha="center")
t(REQ_X+REQ_W/2, REQ_Y-0.45, "REQUEST", c=BLUE, sz=9, ha="center")
icon_circle(REQ_X+REQ_W/2, REQ_Y-0.9, 0.28, BLUE, "Y", sz=13)
hline(REQ_X+0.15, REQ_X+REQ_W-0.15, REQ_Y-1.25, BLUE, 0.8)
t(REQ_X+0.15, REQ_Y-1.35,
  '"Summarize the Y-OS\noperational value audit\nand tell me what to\nsimplify next."',
  c=MID, sz=8.5, va="top")

# ══════════════════════════════════════════════════════════════════════════════
# TEAM VIEW HEADER
# ══════════════════════════════════════════════════════════════════════════════
TEAM_HEADER_Y = FIG_H - 1.1
TEAM_X_START  = REQ_X + REQ_W + 0.35
TEAM_AREA_W   = FIG_W - TEAM_X_START - 5.8  # leave room for metrics panel

rbox(TEAM_X_START, TEAM_HEADER_Y - 0.38, TEAM_AREA_W, 0.38,
     fc="#e8eef8", ec=BLUE, lw=1.2, zorder=3)
t(TEAM_X_START + TEAM_AREA_W/2, TEAM_HEADER_Y - 0.04,
  "TEAM VIEW — WHO WORKED", c=BLUE, sz=11, w="bold", ha="center")

# ══════════════════════════════════════════════════════════════════════════════
# 9 TEAM COLUMNS
# ══════════════════════════════════════════════════════════════════════════════
N_COLS = 9
COL_GAP = 0.18
COL_W = (TEAM_AREA_W - COL_GAP * (N_COLS-1)) / N_COLS
COL_TOP = TEAM_HEADER_Y - 0.38
COL_H = 7.8
COL_BODY_Y = COL_TOP - COL_H

COLS = [
    {
        "num": "1", "title": "Yannick", "icon": "Y", "color": BLUE,
        "fields": [
            ("Role", "User / CEO"),
            ("Worker", "—"),
            ("Input", "Business question\n+ context"),
            ("Output", "Request captured"),
            ("Latency", "0s"),
            ("Cost", "$0"),
            ("Artifact", "—"),
        ]
    },
    {
        "num": "2", "title": "Manus\nOrchestrator", "icon": "M", "color": MID,
        "fields": [
            ("Role", "Orchestrator"),
            ("Worker", "Manus"),
            ("Input", "User request"),
            ("Output", "Mission created\nRouting decided\nRules loaded"),
            ("Latency", "20 ms"),
            ("Cost", "$0.000"),
            ("Artifact", "SESSION-2026-06-14"),
        ]
    },
    {
        "num": "3", "title": "Architect\n(Ganesha)", "icon": "G", "color": PURPLE,
        "fields": [
            ("Role", "Architect / Strategy"),
            ("Worker", "Ganesha"),
            ("Provider", "Anthropic"),
            ("Model", "Claude Opus 4"),
            ("Tools", "artifact_registry\ncontext_cache"),
            ("Input", "Operational audit\nCSO rules\nConstitution"),
            ("Output", "Simplification\nrecommendation"),
            ("Latency", "2.8 sec"),
            ("Cost", "$0.044"),
            ("Artifact", "ARTIFACT-TRACE-001"),
        ]
    },
    {
        "num": "4", "title": "Researcher", "icon": "R", "color": TEAL,
        "fields": [
            ("Role", "Researcher"),
            ("Worker", "Saraswati"),
            ("Provider", "OpenAI"),
            ("Model", "o3"),
            ("Tools", "web_search\nartifact_registry"),
            ("Input", "Context pack\nResearch need"),
            ("Output", "Evidence pack\n+ insights"),
            ("Latency", "0.9 sec"),
            ("Cost", "$0.008"),
            ("Artifact", "EVIDENCE-001"),
        ]
    },
    {
        "num": "5", "title": "Builder", "icon": "B", "color": TEAL,
        "fields": [
            ("Role", "Builder"),
            ("Worker", "Vishvakarma"),
            ("Provider", "Anthropic"),
            ("Model", "Claude Opus 4"),
            ("Tools", "file_writer\ncode_interpreter"),
            ("Input", "Evidence pack\nRequirements"),
            ("Output", "Structured draft\n+ analysis"),
            ("Latency", "0.7 sec"),
            ("Cost", "$0.012"),
            ("Artifact", "DRAFT-001"),
        ]
    },
    {
        "num": "6", "title": "Writer", "icon": "W", "color": TEAL,
        "fields": [
            ("Role", "Writer"),
            ("Worker", "Saraswati"),
            ("Provider", "Google"),
            ("Model", "Gemini 1.5 Pro"),
            ("Tools", "markdown_tools\nstyle_enforcer"),
            ("Input", "Draft\nContext pack"),
            ("Output", "Final text\n(structured)"),
            ("Latency", "0.4 sec"),
            ("Cost", "$0.004"),
            ("Artifact", "CONTENT-001"),
        ]
    },
    {
        "num": "7", "title": "Validator\n(Lakshmi)", "icon": "L", "color": ORANGE,
        "fields": [
            ("Role", "Validator / Gov."),
            ("Worker", "Lakshmi"),
            ("Provider", "Internal"),
            ("Model", "Rules + Constitution"),
            ("Tools", "constitution_checker\nrisk_scorer"),
            ("Input", "Final content\nRisk context"),
            ("Output", "APPROVED ✓\nRisk: 8/100"),
            ("Latency", "0.2 sec"),
            ("Cost", "$0.001"),
            ("Artifact", "APPROVAL-001"),
        ]
    },
    {
        "num": "8", "title": "Git / Notion /\nObsidian", "icon": "S", "color": MID,
        "fields": [
            ("Role", "Memory & Persistence"),
            ("Worker", "Living Memory Pipeline"),
            ("Tools", "git_pusher\nnotion_updater\nobsidian_linker"),
            ("Input", "Approved content\nArtifacts"),
            ("Output", "Stored in Git\nNotion updated\nObsidian linked"),
            ("Latency", "SIMULATED"),
            ("Cost", "$0"),
            ("Artifact", "MEMORY-001"),
        ]
    },
    {
        "num": "9", "title": "Deliverable", "icon": "D", "color": AMBER,
        "fields": [
            ("Role", "Final Output"),
            ("Worker", "Manus"),
            ("Input", "Approved artifact"),
            ("Output", "Delivered to\nYannick"),
            ("Latency", "~3.0 sec TOTAL"),
            ("Cost", "$0.044 TOTAL"),
            ("Artifact", "ARTIFACT-TRACE-001"),
        ]
    },
]

col_centers = []
for i, col in enumerate(COLS):
    cx = TEAM_X_START + i * (COL_W + COL_GAP)
    col_centers.append(cx + COL_W/2)

    # Main card
    rbox(cx, COL_BODY_Y, COL_W, COL_H, fc=WHITE, ec=col["color"], lw=1.5, zorder=3)

    # Numbered header bar
    rbox(cx, COL_BODY_Y + COL_H - 0.55, COL_W, 0.55,
         fc=col["color"], ec=col["color"], lw=0, zorder=4)
    t(cx + COL_W/2, COL_BODY_Y + COL_H - 0.04,
      f"{col['num']}  {col['title']}", c=WHITE, sz=8.5, w="bold",
      ha="center", va="top", z=5)

    # Icon circle
    icon_circle(cx + COL_W/2, COL_BODY_Y + COL_H - 1.05,
                0.28, col["color"], col["icon"], sz=11)

    # Fields
    fy = COL_BODY_Y + COL_H - 1.55
    for label, val in col["fields"]:
        t(cx + 0.12, fy, label, c=col["color"], sz=7.5, w="bold", va="top")
        t(cx + 0.12, fy - 0.22, val, c=MID, sz=7.5, va="top")
        lines = val.count("\n") + 1
        fy -= 0.22 + lines * 0.22 + 0.12
        if fy < COL_BODY_Y + 0.12:
            break

# Arrows between columns
for i in range(N_COLS - 1):
    x1 = TEAM_X_START + (i+1) * (COL_W + COL_GAP) - COL_GAP
    x2 = TEAM_X_START + (i+1) * (COL_W + COL_GAP)
    y_a = COL_BODY_Y + COL_H * 0.62
    arrow(x1, x2, y_a, color=BLUE, lw=1.5)

# Arrow from Yannick request box to column 1
arrow(REQ_X + REQ_W, TEAM_X_START, COL_BODY_Y + COL_H * 0.62, color=BLUE, lw=2)

# ══════════════════════════════════════════════════════════════════════════════
# ARTIFACT HANDOFFS ROW
# ══════════════════════════════════════════════════════════════════════════════
HO_Y = COL_BODY_Y - 0.25
HO_H = 1.6
rbox(TEAM_X_START, HO_Y - HO_H, TEAM_AREA_W, HO_H,
     fc="#fffbf0", ec=AMBER, lw=1.2, zorder=3)
t(TEAM_X_START + TEAM_AREA_W/2, HO_Y - 0.18,
  "HAND-OFFS  (ARTIFACTS PASSED BETWEEN TEAM MEMBERS)",
  c=AMBER, sz=9, w="bold", ha="center")

handoffs = [
    ("CTX-TRACE-001", "3,840 tokens\n0.05 sec"),
    ("EVIDENCE-001",  "1,120 tokens\n0.9 sec"),
    ("DRAFT-001",     "1,980 tokens\n0.7 sec"),
    ("CONTENT-001",   "612 tokens\n0.4 sec"),
    ("APPROVAL-001",  "80 tokens\n8 rules checked\n0.2 sec"),
    ("MEMORY-001",    "3 systems updated\n(simulated)"),
]

# Place handoff arrows between columns 2-8
for i, (name, detail) in enumerate(handoffs):
    col_i = i + 1  # between col i+1 and col i+2
    x1 = TEAM_X_START + col_i * (COL_W + COL_GAP) + COL_W * 0.1
    x2 = TEAM_X_START + (col_i+1) * (COL_W + COL_GAP) - COL_W * 0.1
    y_ho = HO_Y - HO_H/2 - 0.1
    arrow(x1, x2, y_ho, color=AMBER, lw=1.5, label=name, label_color=AMBER)
    t((x1+x2)/2, y_ho - 0.22, detail, c=DIM, sz=7, ha="center", va="top")

# ══════════════════════════════════════════════════════════════════════════════
# PLUGINS NOT ACTIVATED (left panel)
# ══════════════════════════════════════════════════════════════════════════════
PL_X = 0.25
PL_Y = COL_BODY_Y - 0.1
PL_W = REQ_W
PL_H = HO_H + COL_H - REQ_H - 0.1

rbox(PL_X, PL_Y - PL_H, PL_W, PL_H, fc="#fff5f5", ec=RED, lw=1.5, zorder=3)
t(PL_X + PL_W/2, PL_Y - 0.2, "PLUGINS", c=RED, sz=9, w="bold", ha="center")
t(PL_X + PL_W/2, PL_Y - 0.48, "NOT ACTIVATED", c=RED, sz=8.5, w="bold", ha="center")
t(PL_X + PL_W/2, PL_Y - 0.72, "(Core-Only Mode)", c=DIM, sz=8, ha="center")
hline(PL_X+0.15, PL_X+PL_W-0.15, PL_Y-0.85, RED, 0.8)

plugins = [
    ("ODT", "Organizational\nDigital Twin"),
    ("Strategic\nIntelligence", "SRE, gap analysis,\nroadmap"),
    ("Simulation /\nTime Machine", ""),
    ("Advanced\nObservability", "EIS, governance\ndashboard"),
]
py = PL_Y - 1.05
for pname, pdesc in plugins:
    t(PL_X + 0.18, py, "✕", c=RED, sz=10, w="bold", va="top")
    t(PL_X + 0.45, py, pname, c=RED, sz=8.5, w="bold", va="top")
    if pdesc:
        t(PL_X + 0.45, py - 0.28, pdesc, c=DIM, sz=7.5, va="top")
    t(PL_X + 0.45, py - 0.55, "✕ SKIPPED", c=RED, sz=7.5, va="top")
    py -= 1.1

t(PL_X + 0.15, PL_Y - PL_H + 0.55, "Reason:", c=MID, sz=8, w="bold")
t(PL_X + 0.15, PL_Y - PL_H + 0.32, "Core-Only Mode\nADR-SIMP-002\nArchitecture Frozen",
  c=DIM, sz=7.5)

# ══════════════════════════════════════════════════════════════════════════════
# 3 SYNCHRONIZED VIEWS
# ══════════════════════════════════════════════════════════════════════════════
VIEWS_Y = HO_Y - HO_H - 0.3
VIEWS_H = 3.8
VIEWS_X = 0.25
VIEWS_W = FIG_W - 0.25 - 5.8  # leave room for metrics
VIEW_W  = (VIEWS_W - 0.6) / 3

# View 1 — Architecture
V1_X = VIEWS_X
rbox(V1_X, VIEWS_Y - VIEWS_H, VIEW_W, VIEWS_H, fc=CREAM, ec=BLUE, lw=1.5, zorder=3)
section_header(V1_X, VIEWS_Y, VIEW_W, "View 1 — ARCHITECTURE VIEW (Validation)", BLUE)

arch_steps = ["CAPTURE\n(1-2)", "CONTEXT\n(3-5)", "EXECUTION\n(6-8)", "REVIEW\n(9-11)", "MEMORY\n(12)"]
arch_colors = [BLUE, PURPLE, TEAL, ORANGE, MID]
step_w = (VIEW_W - 0.4) / len(arch_steps) - 0.12
step_y = VIEWS_Y - VIEWS_H + 1.8
for j, (step, sc) in enumerate(zip(arch_steps, arch_colors)):
    sx = V1_X + 0.2 + j * (step_w + 0.12)
    rbox(sx, step_y, step_w, 0.8, fc=sc, ec=sc, lw=0, zorder=4)
    t(sx + step_w/2, step_y + 0.75, step, c=WHITE, sz=7.5, w="bold", ha="center", va="top", z=5)
    if j < len(arch_steps)-1:
        arrow(sx + step_w, sx + step_w + 0.12, step_y + 0.4, color=BLUE, lw=1.2)

t(V1_X + VIEW_W/2, VIEWS_Y - VIEWS_H + 1.4,
  "13 STEPS — 10 CORE MODULES USED", c=DARK, sz=8.5, w="bold", ha="center")
t(V1_X + VIEW_W/2, VIEWS_Y - VIEWS_H + 1.0,
  "4 PLUGINS SKIPPED", c=RED, sz=8.5, w="bold", ha="center")

# View 2 — Team
V2_X = V1_X + VIEW_W + 0.3
rbox(V2_X, VIEWS_Y - VIEWS_H, VIEW_W, VIEWS_H, fc=CREAM, ec=PURPLE, lw=1.5, zorder=3)
section_header(V2_X, VIEWS_Y, VIEW_W, "View 2 — TEAM VIEW (Who Worked)", PURPLE)

team_icons = [
    ("YOU", BLUE, "Y"), ("MANUS", MID, "M"), ("GANESHA", PURPLE, "G"),
    ("SARASWATI", TEAL, "S"), ("VISHVAKARMA", TEAL, "V"),
    ("SARASWATI", TEAL, "S"), ("LAKSHMI", ORANGE, "L"),
    ("GIT /\nNOTION", MID, "S"),
]
icon_r = 0.22
icons_per_row = 4
for j, (name, ic, sym) in enumerate(team_icons):
    row = j // icons_per_row
    col_j = j % icons_per_row
    ix = V2_X + 0.5 + col_j * (VIEW_W - 0.6) / icons_per_row
    iy = VIEWS_Y - 1.1 - row * 1.1
    icon_circle(ix, iy, icon_r, ic, sym, sz=9)
    t(ix, iy - icon_r - 0.05, name, c=MID, sz=7, ha="center", va="top")

t(V2_X + VIEW_W/2, VIEWS_Y - VIEWS_H + 0.85,
  "A MULTI-DISCIPLINARY TEAM WORKED TOGETHER", c=DARK, sz=8, w="bold", ha="center")
t(V2_X + VIEW_W/2, VIEWS_Y - VIEWS_H + 0.5,
  "PASSING CONTEXT, EVIDENCE, DRAFTS AND APPROVAL",
  c=DIM, sz=7.5, ha="center")

# View 3 — Value
V3_X = V2_X + VIEW_W + 0.3
rbox(V3_X, VIEWS_Y - VIEWS_H, VIEW_W, VIEWS_H, fc="#fffef0", ec=AMBER, lw=1.5, zorder=3)
section_header(V3_X, VIEWS_Y, VIEW_W, "View 3 — VALUE VIEW (What Was Created)", AMBER)

value_items = [
    ("ARTIFACTS\nCREATED", "6", AMBER),
    ("DECISIONS\nPRODUCED", "1", TEAL),
    ("KNOWLEDGE\nADDED", "1", BLUE),
    ("REPOS\nUPDATED", "3", MID),
    ("FINAL\nDELIVERABLES", "1", GREEN),
]
vbox_w = (VIEW_W - 0.5) / len(value_items) - 0.1
vbox_y = VIEWS_Y - 1.0
for j, (label, val, vc) in enumerate(value_items):
    vx = V3_X + 0.25 + j * (vbox_w + 0.1)
    rbox(vx, vbox_y - 1.2, vbox_w, 1.2, fc=WHITE, ec=vc, lw=1.2, zorder=4)
    t(vx + vbox_w/2, vbox_y - 0.18, val, c=vc, sz=18, w="bold", ha="center", va="top", z=5)
    t(vx + vbox_w/2, vbox_y - 0.75, label, c=MID, sz=7, ha="center", va="top", z=5)

t(V3_X + VIEW_W/2, VIEWS_Y - VIEWS_H + 0.65,
  "Y-OS CREATED OPERATIONAL VALUE", c=GREEN, sz=9, w="bold", ha="center")

# ══════════════════════════════════════════════════════════════════════════════
# WITHOUT vs WITH Y-OS (bottom)
# ══════════════════════════════════════════════════════════════════════════════
CMP_Y = VIEWS_Y - VIEWS_H - 0.3
CMP_H = 3.2
CMP_W = (VIEWS_W - 0.5) / 2

# WITHOUT
rbox(VIEWS_X, CMP_Y - CMP_H, CMP_W, CMP_H, fc="#fff5f5", ec=RED, lw=1.5, zorder=3)
section_header(VIEWS_X, CMP_Y, CMP_W, "WITHOUT Y-OS  (MANUAL PROCESS)", RED)

without_steps = [
    ("Find audit", "→"), ("Copy", "→"), ("Find ADR", "→"), ("Copy", "→"),
    ("Find rules", "→"), ("Copy", "→"), ("Paste all\nin LLM", "→"),
    ("Ask\nquestion", "→"), ("Copy\nresult", "→"), ("Save\nmanually", ""),
]
step_bw = (CMP_W - 0.4) / len(without_steps) - 0.08
for j, (step, arr) in enumerate(without_steps):
    sx = VIEWS_X + 0.2 + j * (step_bw + 0.08)
    rbox(sx, CMP_Y - CMP_H + 1.2, step_bw, 1.0, fc=WHITE, ec=LIGHT_BORDER, lw=0.8, zorder=4)
    t(sx + step_bw/2, CMP_Y - CMP_H + 2.1, step, c=MID, sz=7.5, ha="center", va="top", z=5)
    if arr:
        t(sx + step_bw + 0.01, CMP_Y - CMP_H + 1.72, "→", c=RED, sz=9, ha="center", z=5)

rbox(VIEWS_X + CMP_W/2 - 1.2, CMP_Y - CMP_H + 0.15, 2.4, 0.9,
     fc="#fde8e8", ec=RED, lw=1, zorder=4)
t(VIEWS_X + CMP_W/2, CMP_Y - CMP_H + 0.95,
  "≈ 5 – 10 min", c=RED, sz=11, w="bold", ha="center")
t(VIEWS_X + CMP_W/2, CMP_Y - CMP_H + 0.55,
  "High cognitive load\nManual, error-prone", c=RED, sz=8, ha="center")

# VS label
t(VIEWS_X + CMP_W + 0.25, CMP_Y - CMP_H/2,
  "VS", c=DARK, sz=16, w="bold", ha="center", va="center")

# WITH
WITH_X = VIEWS_X + CMP_W + 0.5
rbox(WITH_X, CMP_Y - CMP_H, CMP_W, CMP_H, fc="#f0fff4", ec=GREEN, lw=2, zorder=3)
section_header(WITH_X, CMP_Y, CMP_W, "WITH Y-OS  (AUTOMATED WITH GOVERNANCE)", GREEN)

with_steps = [
    ("Ask\nquestion", "Y-OS retrieves\nautomatically"),
    ("Team works\nin seconds", ""),
    ("Governance\napplied", ""),
    ("Artifact\nregistered", ""),
    ("Memory\nupdated", ""),
    ("Answer\ndelivered", ""),
]
step_bw2 = (CMP_W - 0.4) / len(with_steps) - 0.1
for j, (step, sub) in enumerate(with_steps):
    sx = WITH_X + 0.2 + j * (step_bw2 + 0.1)
    rbox(sx, CMP_Y - CMP_H + 1.2, step_bw2, 1.0, fc=WHITE, ec=GREEN, lw=1, zorder=4)
    icon_circle(sx + step_bw2/2, CMP_Y - CMP_H + 1.95, 0.2, GREEN, str(j+1), sz=8)
    t(sx + step_bw2/2, CMP_Y - CMP_H + 1.65, step, c=MID, sz=7.5, ha="center", va="top", z=5)
    if j < len(with_steps)-1:
        t(sx + step_bw2 + 0.02, CMP_Y - CMP_H + 1.72, "→", c=GREEN, sz=9, ha="center", z=5)

rbox(WITH_X + CMP_W/2 - 1.2, CMP_Y - CMP_H + 0.15, 2.4, 0.9,
     fc="#d1fae5", ec=GREEN, lw=1, zorder=4)
t(WITH_X + CMP_W/2, CMP_Y - CMP_H + 0.95,
  "≈ 3 sec", c=GREEN, sz=14, w="bold", ha="center")
t(WITH_X + CMP_W/2, CMP_Y - CMP_H + 0.55,
  "Low cognitive load\nAutomated & reliable", c=GREEN, sz=8, ha="center")

# ══════════════════════════════════════════════════════════════════════════════
# RIGHT PANEL — RUNTIME METRICS
# ══════════════════════════════════════════════════════════════════════════════
MP_X = FIG_W - 5.5
MP_Y = FIG_H - 1.1
MP_W = 5.2
MP_H = FIG_H - 1.4

rbox(MP_X, MP_Y - MP_H, MP_W, MP_H, fc=CREAM, ec=DARK, lw=2, zorder=3)
rbox(MP_X, MP_Y - 0.42, MP_W, 0.42, fc=DARK, ec=DARK, lw=0, zorder=4)
t(MP_X + MP_W/2, MP_Y - 0.06, "RUNTIME METRICS",
  c=WHITE, sz=10, w="bold", ha="center", z=5)

metrics = [
    ("⏱", "Total Time", "3.021 sec"),
    ("$", "Total Cost", "$0.044"),
    ("#", "Total Tokens", "4,452"),
    ("⚙", "Models Used", "• Claude Opus 4\n  (Anthropic)"),
    ("🔧", "Tools Used", "• artifact_registry\n• context_cache\n• constitution_checker\n• file_writer\n• markdown_tools\n• web_search"),
    ("📦", "Artifacts Created", "• ARTIFACT-TRACE-001\n• EVIDENCE-001\n• DRAFT-001\n• CONTENT-001\n• APPROVAL-001\n• MEMORY-001"),
    ("✕", "Plugins Skipped", "4 / 4"),
]

my = MP_Y - 0.65
for icon, label, val in metrics:
    t(MP_X + 0.25, my, icon, c=BLUE, sz=12, va="top")
    t(MP_X + 0.65, my, label, c=DARK, sz=9, w="bold", va="top")
    lines = val.count("\n") + 1
    t(MP_X + 0.65, my - 0.28, val, c=MID, sz=8.5, va="top")
    hline(MP_X + 0.2, MP_X + MP_W - 0.2, my - 0.28 - lines * 0.26 - 0.1,
          LIGHT_BORDER, 0.6)
    my -= 0.28 + lines * 0.26 + 0.28

# ══════════════════════════════════════════════════════════════════════════════
# DID Y-OS CREATE VALUE? — verdict box (bottom right)
# ══════════════════════════════════════════════════════════════════════════════
VD_X = MP_X
VD_Y = VIEWS_Y - VIEWS_H - 0.3
VD_W = MP_W
VD_H = CMP_H

rbox(VD_X, VD_Y - VD_H, VD_W, VD_H, fc="#f0fff4", ec=GREEN, lw=2, zorder=3)
section_header(VD_X, VD_Y, VD_W, "DID Y-OS CREATE VALUE?", GREEN)

# Big YES
rbox(VD_X + 0.3, VD_Y - 1.5, VD_W - 0.6, 0.9, fc=GREEN, ec=GREEN, lw=0, zorder=4)
t(VD_X + VD_W/2, VD_Y - 0.72, "YES", c=WHITE, sz=22, w="bold", ha="center", z=5)

checkmarks = [
    "Context automatically retrieved",
    "Governance applied (Lakshmi)",
    "Artifact registered with lineage",
    "Memory updated (simulated)",
    "Delivered actionable recommendation",
    "Time saved vs manual process: ~5-10 min",
]
cy = VD_Y - 1.75
for ck in checkmarks:
    t(VD_X + 0.25, cy, "✓", c=GREEN, sz=10, w="bold", va="top")
    t(VD_X + 0.55, cy, ck, c=MID, sz=8, va="top")
    cy -= 0.38

# ─── SAVE ─────────────────────────────────────────────────────────────────────
base = "/home/ubuntu/yreg/mission_trace_standard_001/value_trace_template_sketch"
plt.tight_layout(pad=0)
plt.savefig(base + ".png", format="png", dpi=DPI, bbox_inches="tight",
            facecolor=fig.get_facecolor())
plt.savefig(base + ".svg", format="svg", dpi=DPI, bbox_inches="tight",
            facecolor=fig.get_facecolor())
plt.close()
print(f"PNG: {base}.png")
print(f"SVG: {base}.svg")
print("Done.")
