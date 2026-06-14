"""
Y-OS TEAM TRACE — MISSION-WORK-REAL-001
Y Travel Discovery Brick — Haute-Nendaz & Valais
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.spines.left": False, "axes.spines.bottom": False,
})

WHITE  = "#ffffff"; CREAM = "#fafaf8"; LIGHT = "#f5f5f0"
BORDER = "#333333"; DARK  = "#111111"; MID   = "#444444"; DIM = "#888888"
LIGHT_BORDER = "#aaaaaa"
BLUE   = "#1a4fa0"; PURPLE = "#6b3fa0"; TEAL  = "#1a7a6e"
ORANGE = "#c85a00"; AMBER  = "#b87800"; GREEN = "#1a6e2e"
RED    = "#c0392b"; GREY   = "#666666"
COL_ACCENTS = [BLUE, MID, PURPLE, TEAL, TEAL, ORANGE, MID, AMBER]

FIG_W, FIG_H = 38, 26
DPI = 130
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
ax.set_xlim(0, FIG_W); ax.set_ylim(0, FIG_H)
ax.set_aspect("equal"); ax.axis("off")
fig.patch.set_facecolor(WHITE); ax.set_facecolor(WHITE)

def rbox(x, y, w, h, fc=WHITE, ec=BORDER, lw=1.2, alpha=1.0, zorder=2):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06",
                       lw=lw, edgecolor=ec, facecolor=fc, alpha=alpha, zorder=zorder)
    ax.add_patch(p)

def t(x, y, s, c=DARK, sz=9, w="normal", ha="left", va="top", z=5):
    ax.text(x, y, s, color=c, fontsize=sz, fontweight=w, ha=ha, va=va, zorder=z)

def arrow(x1, x2, y, color=BLUE, lw=1.8, label="", label_color=None):
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=14), zorder=6)
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
    t(x+w/2, y-0.04, label, c=WHITE, sz=9, w="bold", ha="center", va="top", z=5)

def icon_circle(cx, cy, r, color, symbol, sz=12):
    circ = plt.Circle((cx, cy), r, fc=color, ec=color, lw=0, zorder=6)
    ax.add_patch(circ)
    t(cx, cy+0.02, symbol, c=WHITE, sz=sz, w="bold", ha="center", va="center", z=7)

# ══════════════════════════════════════════════════════════════════════════════
# TITLE
# ══════════════════════════════════════════════════════════════════════════════
t(FIG_W/2, FIG_H-0.25, "Y-OS TEAM TRACE — EXECUTION TRACE",
  c=DARK, sz=20, w="bold", ha="center")
t(FIG_W/2, FIG_H-0.75, "Mission: WORK-REAL-001  •  Date: 2026-06-14  •  Y Travel Discovery Brick",
  c=DIM, sz=10, ha="center")
t(FIG_W-0.3, FIG_H-0.25, "TRACE ID: TRACE-REAL-001",
  c=BLUE, sz=9, w="bold", ha="right")

# ══════════════════════════════════════════════════════════════════════════════
# YANNICK REQUEST BOX
# ══════════════════════════════════════════════════════════════════════════════
REQ_X, REQ_Y = 0.25, FIG_H - 1.2
REQ_W, REQ_H = 2.8, 3.2
rbox(REQ_X, REQ_Y - REQ_H, REQ_W, REQ_H, fc=CREAM, ec=BLUE, lw=2, zorder=3)
t(REQ_X+REQ_W/2, REQ_Y-0.18, "YANNICK", c=BLUE, sz=11, w="bold", ha="center")
t(REQ_X+REQ_W/2, REQ_Y-0.45, "REQUEST", c=BLUE, sz=9, ha="center")
icon_circle(REQ_X+REQ_W/2, REQ_Y-0.9, 0.28, BLUE, "Y", sz=13)
hline(REQ_X+0.15, REQ_X+REQ_W-0.15, REQ_Y-1.25, BLUE, 0.8)
t(REQ_X+0.15, REQ_Y-1.35,
  '"Find 10 premium\noutings near\nHaute-Nendaz\nfor next weekend."',
  c=MID, sz=8.5, va="top")

# ══════════════════════════════════════════════════════════════════════════════
# TEAM VIEW HEADER
# ══════════════════════════════════════════════════════════════════════════════
TEAM_HEADER_Y = FIG_H - 1.1
TEAM_X_START  = REQ_X + REQ_W + 0.35
TEAM_AREA_W   = FIG_W - TEAM_X_START - 5.8

rbox(TEAM_X_START, TEAM_HEADER_Y - 0.38, TEAM_AREA_W, 0.38,
     fc="#e8eef8", ec=BLUE, lw=1.2, zorder=3)
t(TEAM_X_START + TEAM_AREA_W/2, TEAM_HEADER_Y - 0.04,
  "TEAM VIEW — WHO WORKED", c=BLUE, sz=11, w="bold", ha="center")

# ══════════════════════════════════════════════════════════════════════════════
# 8 TEAM COLUMNS (no separate Writer — Researcher does it all)
# ══════════════════════════════════════════════════════════════════════════════
N_COLS = 8
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
            ("Input", "Real-world\ntravel need"),
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
            ("Output", "Mission created\nRouting decided\nContext loaded"),
            ("Latency", "20 ms"),
            ("Cost", "$0.000"),
            ("Artifact", "SESSION-REAL-001"),
        ]
    },
    {
        "num": "3", "title": "Architect\n(Ganesha)", "icon": "G", "color": PURPLE,
        "fields": [
            ("Role", "Architect / Strategy"),
            ("Worker", "Ganesha"),
            ("Provider", "Anthropic"),
            ("Model", "Claude Opus 4"),
            ("Tools", "context_cache\nartifact_registry"),
            ("Input", "Travel request\nUser profile\n(Nendaz, premium)"),
            ("Output", "Search strategy\n+ category map"),
            ("Latency", "1.2 sec"),
            ("Cost", "$0.018"),
            ("Artifact", "STRATEGY-REAL-001"),
        ]
    },
    {
        "num": "4", "title": "Researcher\n(Saraswati)", "icon": "R", "color": TEAL,
        "fields": [
            ("Role", "Researcher"),
            ("Worker", "Saraswati"),
            ("Provider", "Anthropic"),
            ("Model", "Claude Opus 4"),
            ("Tools", "web_search\nwebpage_extract"),
            ("Input", "Strategy pack\n3 search queries\n× 3 categories"),
            ("Output", "10 verified outings\nwith live data"),
            ("Latency", "8.4 sec"),
            ("Cost", "$0.031"),
            ("Artifact", "RESEARCH-REAL-001"),
        ]
    },
    {
        "num": "5", "title": "Builder\n(Vishvakarma)", "icon": "B", "color": TEAL,
        "fields": [
            ("Role", "Builder / Formatter"),
            ("Worker", "Vishvakarma"),
            ("Provider", "Anthropic"),
            ("Model", "Claude Opus 4"),
            ("Tools", "file_writer"),
            ("Input", "Research pack\n10 outings data"),
            ("Output", "MD + JSON\nformatted files"),
            ("Latency", "1.1 sec"),
            ("Cost", "$0.009"),
            ("Artifact", "DISCOVERY-BRICK-001"),
        ]
    },
    {
        "num": "6", "title": "Validator\n(Lakshmi)", "icon": "L", "color": ORANGE,
        "fields": [
            ("Role", "Validator / Gov."),
            ("Worker", "Lakshmi"),
            ("Provider", "Internal"),
            ("Model", "Rules + Profile"),
            ("Tools", "constitution_checker"),
            ("Input", "Discovery brick\nUser preferences"),
            ("Output", "APPROVED ✓\nRisk: 2/100"),
            ("Latency", "0.1 sec"),
            ("Cost", "$0.001"),
            ("Artifact", "APPROVAL-REAL-001"),
        ]
    },
    {
        "num": "7", "title": "Git /\nNotion", "icon": "S", "color": MID,
        "fields": [
            ("Role", "Memory & Persistence"),
            ("Worker", "Living Memory Pipeline"),
            ("Tools", "git_pusher\nnotion_updater"),
            ("Input", "Approved files"),
            ("Output", "Stored in Git\ny-os-doctrine\ncommit f85732d"),
            ("Latency", "2.1 sec"),
            ("Cost", "$0"),
            ("Artifact", "MEMORY-REAL-001"),
        ]
    },
    {
        "num": "8", "title": "Deliverable", "icon": "D", "color": AMBER,
        "fields": [
            ("Role", "Final Output"),
            ("Worker", "Manus"),
            ("Input", "Approved artifact"),
            ("Output", "10 outings\ndelivered to\nYannick"),
            ("Latency", "~13 sec TOTAL"),
            ("Cost", "$0.059 TOTAL"),
            ("Artifact", "DISCOVERY-BRICK-001"),
        ]
    },
]

col_centers = []
for i, col in enumerate(COLS):
    cx = TEAM_X_START + i * (COL_W + COL_GAP)
    col_centers.append(cx + COL_W/2)
    rbox(cx, COL_BODY_Y, COL_W, COL_H, fc=WHITE, ec=col["color"], lw=1.5, zorder=3)
    rbox(cx, COL_BODY_Y + COL_H - 0.55, COL_W, 0.55,
         fc=col["color"], ec=col["color"], lw=0, zorder=4)
    t(cx + COL_W/2, COL_BODY_Y + COL_H - 0.04,
      f"{col['num']}  {col['title']}", c=WHITE, sz=8.5, w="bold", ha="center", va="top", z=5)
    icon_circle(cx + COL_W/2, COL_BODY_Y + COL_H - 1.05, 0.28, col["color"], col["icon"], sz=11)
    fy = COL_BODY_Y + COL_H - 1.55
    for label, val in col["fields"]:
        t(cx + 0.12, fy, label, c=col["color"], sz=7.5, w="bold", va="top")
        t(cx + 0.12, fy - 0.22, val, c=MID, sz=7.5, va="top")
        lines = val.count("\n") + 1
        fy -= 0.22 + lines * 0.22 + 0.12
        if fy < COL_BODY_Y + 0.12:
            break

for i in range(N_COLS - 1):
    x1 = TEAM_X_START + (i+1) * (COL_W + COL_GAP) - COL_GAP
    x2 = TEAM_X_START + (i+1) * (COL_W + COL_GAP)
    arrow(x1, x2, COL_BODY_Y + COL_H * 0.62, color=BLUE, lw=1.5)

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
    ("CTX-REAL-001",      "2,100 tokens\n0.02 sec"),
    ("STRATEGY-REAL-001", "890 tokens\n1.2 sec"),
    ("RESEARCH-REAL-001", "4,200 tokens\n8.4 sec"),
    ("DISCOVERY-BRICK",   "1,850 tokens\n1.1 sec"),
    ("APPROVAL-REAL-001", "120 tokens\n0.1 sec"),
    ("MEMORY-REAL-001",   "2 systems updated\n2.1 sec"),
]

for i, (name, detail) in enumerate(handoffs):
    col_i = i + 1
    x1 = TEAM_X_START + col_i * (COL_W + COL_GAP) + COL_W * 0.1
    x2 = TEAM_X_START + (col_i+1) * (COL_W + COL_GAP) - COL_W * 0.1
    y_ho = HO_Y - HO_H/2 - 0.1
    arrow(x1, x2, y_ho, color=AMBER, lw=1.5, label=name, label_color=AMBER)
    t((x1+x2)/2, y_ho - 0.22, detail, c=DIM, sz=7, ha="center", va="top")

# ══════════════════════════════════════════════════════════════════════════════
# PLUGINS NOT ACTIVATED
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
    ("Strategic\nIntelligence", "SRE, gap analysis"),
    ("Simulation /\nTime Machine", ""),
    ("Observability", "EIS dashboard"),
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
VIEWS_W = FIG_W - 0.25 - 5.8
VIEW_W  = (VIEWS_W - 0.6) / 3

# View 1 — Architecture
V1_X = VIEWS_X
rbox(V1_X, VIEWS_Y - VIEWS_H, VIEW_W, VIEWS_H, fc=CREAM, ec=BLUE, lw=1.5, zorder=3)
section_header(V1_X, VIEWS_Y, VIEW_W, "View 1 — ARCHITECTURE VIEW (Validation)", BLUE)

arch_steps = [
    ("CAPTURE", "(1-2)", BLUE),
    ("CONTEXT", "(3)", PURPLE),
    ("EXECUTION", "(4-5)", TEAL),
    ("REVIEW", "(6)", ORANGE),
    ("MEMORY", "(7)", MID),
]
aw = (VIEW_W - 0.4) / len(arch_steps)
for j, (lbl, sub, clr) in enumerate(arch_steps):
    ax_ = V1_X + 0.2 + j * aw
    rbox(ax_, VIEWS_Y - 1.5, aw - 0.1, 0.7, fc=clr, ec=clr, lw=0, zorder=4)
    t(ax_ + (aw-0.1)/2, VIEWS_Y - 1.12, lbl, c=WHITE, sz=8, w="bold", ha="center", va="top", z=5)
    t(ax_ + (aw-0.1)/2, VIEWS_Y - 1.42, sub, c=WHITE, sz=7, ha="center", va="top", z=5)
    if j < len(arch_steps)-1:
        arrow(ax_ + aw - 0.1, ax_ + aw, VIEWS_Y - 1.15, color=BORDER, lw=1.2)

t(V1_X + VIEW_W/2, VIEWS_Y - 2.1, "8 STEPS — 7 CORE MODULES USED",
  c=DARK, sz=8.5, w="bold", ha="center")
t(V1_X + VIEW_W/2, VIEWS_Y - 2.45, "4 PLUGINS SKIPPED",
  c=RED, sz=8.5, w="bold", ha="center")
t(V1_X + VIEW_W/2, VIEWS_Y - 2.8, "REAL-WORLD TASK — NON-Y-OS PROJECT",
  c=GREEN, sz=8, ha="center")

# View 2 — Team
V2_X = V1_X + VIEW_W + 0.3
rbox(V2_X, VIEWS_Y - VIEWS_H, VIEW_W, VIEWS_H, fc=CREAM, ec=PURPLE, lw=1.5, zorder=3)
section_header(V2_X, VIEWS_Y, VIEW_W, "View 2 — TEAM VIEW (Who Worked)", PURPLE)

team_icons = [
    ("Y", BLUE, "YOU"),
    ("M", MID, "MANUS"),
    ("G", PURPLE, "GANESHA"),
    ("R", TEAL, "SARASWATI"),
    ("B", TEAL, "VISHVAKARMA"),
    ("L", ORANGE, "LAKSHMI"),
    ("S", MID, "GIT/NOTION"),
]
icon_r = 0.22
icons_per_row = 4
for j, (sym, clr, name) in enumerate(team_icons):
    row = j // icons_per_row
    col_j = j % icons_per_row
    ix = V2_X + 0.5 + col_j * (VIEW_W - 0.6) / icons_per_row
    iy = VIEWS_Y - 1.1 - row * 1.1
    icon_circle(ix, iy, icon_r, clr, sym, sz=10)
    t(ix, iy - icon_r - 0.08, name, c=MID, sz=6.5, ha="center", va="top", z=5)

t(V2_X + VIEW_W/2, VIEWS_Y - 3.1,
  "A MULTI-DISCIPLINARY TEAM WORKED TOGETHER",
  c=DARK, sz=8, w="bold", ha="center")
t(V2_X + VIEW_W/2, VIEWS_Y - 3.4,
  "SEARCHING, STRUCTURING, VALIDATING & ARCHIVING",
  c=DIM, sz=7.5, ha="center")

# View 3 — Value
V3_X = V2_X + VIEW_W + 0.3
rbox(V3_X, VIEWS_Y - VIEWS_H, VIEW_W, VIEWS_H, fc="#fffbf0", ec=AMBER, lw=1.5, zorder=3)
section_header(V3_X, VIEWS_Y, VIEW_W, "View 3 — VALUE VIEW (What Was Created)", AMBER)

value_items = [
    ("10", "OUTINGS\nFOUND"),
    ("3", "FORMATS\nDELIVERED"),
    ("1", "GIT\nCOMMIT"),
    ("2", "FILES\nARCHIVED"),
    ("0", "MANUAL\nPROMPTS"),
]
vw = (VIEW_W - 0.4) / len(value_items)
for j, (num, lbl) in enumerate(value_items):
    vx = V3_X + 0.2 + j * vw
    rbox(vx, VIEWS_Y - 2.2, vw - 0.1, 1.1, fc=WHITE, ec=AMBER, lw=1.2, zorder=4)
    t(vx + (vw-0.1)/2, VIEWS_Y - 1.25, num, c=AMBER, sz=18, w="bold", ha="center", va="top", z=5)
    t(vx + (vw-0.1)/2, VIEWS_Y - 1.9, lbl, c=MID, sz=7, ha="center", va="top", z=5)

t(V3_X + VIEW_W/2, VIEWS_Y - 2.55, "Y-OS CREATED REAL OPERATIONAL VALUE",
  c=GREEN, sz=8.5, w="bold", ha="center")
t(V3_X + VIEW_W/2, VIEWS_Y - 2.9, "NON-SELF-REFERENTIAL TASK — EXTERNAL PROJECT",
  c=DIM, sz=7.5, ha="center")

# ══════════════════════════════════════════════════════════════════════════════
# WITHOUT / WITH Y-OS COMPARISON
# ══════════════════════════════════════════════════════════════════════════════
CMP_Y = VIEWS_Y - VIEWS_H - 0.3
CMP_H = 3.2
CMP_W = VIEWS_W
CMP_X = 0.25

# WITHOUT
W1_W = (CMP_W - 0.5) / 2
rbox(CMP_X, CMP_Y - CMP_H, W1_W, CMP_H, fc="#fff5f5", ec=RED, lw=1.5, zorder=3)
section_header(CMP_X, CMP_Y, W1_W, "WITHOUT Y-OS  (MANUAL PROCESS)", RED)

manual_steps = ["Search Google", "Copy snippets", "Open 10 tabs", "Copy/paste",
                "Ask ChatGPT", "Format manually", "Save manually"]
ms_w = (W1_W - 0.4) / len(manual_steps)
for j, step in enumerate(manual_steps):
    sx = CMP_X + 0.2 + j * ms_w
    rbox(sx, CMP_Y - 1.5, ms_w - 0.08, 0.65, fc=WHITE, ec=RED, lw=1, zorder=4)
    t(sx + (ms_w-0.08)/2, CMP_Y - 1.12, step, c=RED, sz=7, ha="center", va="top", z=5)
    if j < len(manual_steps)-1:
        arrow(sx + ms_w - 0.08, sx + ms_w, CMP_Y - 1.18, color=RED, lw=1)

rbox(CMP_X + W1_W/2 - 1.1, CMP_Y - 2.3, 2.2, 0.65,
     fc="#fde8e8", ec=RED, lw=1.2, zorder=4)
t(CMP_X + W1_W/2, CMP_Y - 1.95, "≈ 20 – 40 min", c=RED, sz=12, w="bold", ha="center")
t(CMP_X + W1_W/2, CMP_Y - 2.25, "High cognitive load — no lineage — no memory",
  c=RED, sz=8, ha="center")

# VS label
t(CMP_X + W1_W + 0.25, CMP_Y - CMP_H/2, "VS", c=DARK, sz=14, w="bold", ha="center", va="center")

# WITH
W2_X = CMP_X + W1_W + 0.5
W2_W = W1_W
rbox(W2_X, CMP_Y - CMP_H, W2_W, CMP_H, fc="#f0fff4", ec=GREEN, lw=1.5, zorder=3)
section_header(W2_X, CMP_Y, W2_W, "WITH Y-OS  (AUTOMATED WITH GOVERNANCE)", GREEN)

yos_steps = ["Ask question", "Team works\nautomatically", "Live web\nsearch",
             "Governance\napplied", "Artifact\nregistered", "Memory\nupdated", "Answer\ndelivered"]
ys_w = (W2_W - 0.4) / len(yos_steps)
for j, step in enumerate(yos_steps):
    yx = W2_X + 0.2 + j * ys_w
    icon_circle(yx + (ys_w-0.08)/2, CMP_Y - 1.18, 0.22, GREEN, str(j+1), sz=9)
    t(yx + (ys_w-0.08)/2, CMP_Y - 1.52, step, c=MID, sz=7, ha="center", va="top", z=5)
    if j < len(yos_steps)-1:
        arrow(yx + ys_w - 0.08, yx + ys_w, CMP_Y - 1.18, color=GREEN, lw=1)

rbox(W2_X + W2_W/2 - 1.1, CMP_Y - 2.3, 2.2, 0.65,
     fc="#e8f5e9", ec=GREEN, lw=1.2, zorder=4)
t(W2_X + W2_W/2, CMP_Y - 1.95, "≈ 13 sec", c=GREEN, sz=12, w="bold", ha="center")
t(W2_X + W2_W/2, CMP_Y - 2.25, "Low cognitive load — lineage — memory — governance",
  c=GREEN, sz=8, ha="center")

# ══════════════════════════════════════════════════════════════════════════════
# RUNTIME METRICS PANEL (right)
# ══════════════════════════════════════════════════════════════════════════════
MET_X = FIG_W - 5.5
MET_Y = FIG_H - 1.1
MET_W = 5.25
MET_H = FIG_H - CMP_Y + CMP_H - 0.5

rbox(MET_X, MET_Y - MET_H, MET_W, MET_H, fc=CREAM, ec=BORDER, lw=1.5, zorder=3)
rbox(MET_X, MET_Y - 0.4, MET_W, 0.4, fc=DARK, ec=DARK, lw=0, zorder=4)
t(MET_X + MET_W/2, MET_Y - 0.05, "RUNTIME METRICS", c=WHITE, sz=10, w="bold", ha="center")

metrics = [
    ("⏱", "Total Time", "~13 sec"),
    ("$", "Total Cost", "$0.059"),
    ("#", "Total Tokens", "9,160"),
    ("🤖", "Models Used", "Claude Opus 4\n(Anthropic)"),
    ("🔧", "Tools Used", "web_search\nwebpage_extract\nfile_writer\nartifact_registry"),
    ("📦", "Artifacts Created", "• STRATEGY-REAL-001\n• RESEARCH-REAL-001\n• DISCOVERY-BRICK-001\n• APPROVAL-REAL-001\n• MEMORY-REAL-001"),
    ("✕", "Plugins Skipped", "4 / 4"),
]
my = MET_Y - 0.65
for icon_s, label, val in metrics:
    t(MET_X + 0.25, my, icon_s, c=BLUE, sz=10, w="bold", va="top")
    t(MET_X + 0.65, my, label, c=DARK, sz=8.5, w="bold", va="top")
    lines = val.count("\n") + 1
    t(MET_X + 0.65, my - 0.26, val, c=MID, sz=8, va="top")
    my -= 0.26 + lines * 0.22 + 0.22
    hline(MET_X + 0.2, MET_X + MET_W - 0.2, my + 0.1, LIGHT_BORDER, 0.5)

# ══════════════════════════════════════════════════════════════════════════════
# VERDICT BOX (bottom right)
# ══════════════════════════════════════════════════════════════════════════════
VD_X = MET_X
VD_Y = CMP_Y
VD_W = MET_W
VD_H = CMP_H

rbox(VD_X, VD_Y - VD_H, VD_W, VD_H, fc="#f0fff4", ec=GREEN, lw=2, zorder=3)
section_header(VD_X, VD_Y, VD_W, "DID Y-OS CREATE VALUE?", GREEN)

rbox(VD_X + 0.3, VD_Y - 1.4, VD_W - 0.6, 0.75,
     fc=GREEN, ec=GREEN, lw=0, zorder=4)
t(VD_X + VD_W/2, VD_Y - 0.85, "YES", c=WHITE, sz=22, w="bold", ha="center", va="top", z=5)

checkmarks = [
    "✓ Live web search — 2025/2026 data",
    "✓ Profile context auto-loaded",
    "✓ Governance applied (Lakshmi)",
    "✓ Artifact registered with lineage",
    "✓ Memory updated (Git commit)",
    "✓ Zero iterative prompting needed",
    "✓ Non-self-referential task — real work",
]
cy = VD_Y - 1.65
for chk in checkmarks:
    t(VD_X + 0.25, cy, chk, c=GREEN, sz=8, va="top")
    cy -= 0.28

# ══════════════════════════════════════════════════════════════════════════════
# SAVE
# ══════════════════════════════════════════════════════════════════════════════
base = "/home/ubuntu/yreg/mission_work_real_001/team_trace_real_001"
plt.savefig(base + ".png", format="png", dpi=DPI, bbox_inches="tight",
            facecolor=WHITE, edgecolor="none")
plt.savefig(base + ".svg", format="svg", dpi=DPI, bbox_inches="tight",
            facecolor=WHITE, edgecolor="none")
print(f"PNG: {base}.png")
print(f"SVG: {base}.svg")
plt.close()
