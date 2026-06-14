#!/usr/bin/env python3
"""
render_value_trace.py  —  Y-OS Team Trace Renderer v3.0 (SKETCH EDITION)
=========================================================================
Reads one JSON file, produces the canonical sketch/consulting trace:
  - White background, hand-drawn feel
  - 9 numbered team columns with icon circles
  - Artifact handoffs row
  - Plugins NOT ACTIVATED panel (left)
  - 3 synchronized views (Architecture / Team / Value)
  - Runtime Metrics panel (right)
  - DID Y-OS CREATE VALUE? verdict box (bottom right)
  - WITHOUT vs WITH Y-OS comparison (bottom)

Usage:
    python3 render_value_trace.py <schema.json> <output_base>

Example:
    python3 render_value_trace.py value_trace_schema.json ./out/my_mission

Produces:
    my_mission.png
    my_mission.svg
    my_mission.excalidraw
"""
import sys, json, uuid
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

# ─── FONT ─────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.spines.left": False, "axes.spines.bottom": False,
})

# ─── PALETTE ──────────────────────────────────────────────────────────────────
WHITE  = "#ffffff"; CREAM = "#fafaf8"; LIGHT = "#f5f5f0"
BORDER = "#333333"; DARK  = "#111111"; MID   = "#444444"; DIM = "#888888"
LIGHT_BORDER = "#aaaaaa"

BLUE   = "#1a4fa0"   # human / Yannick
PURPLE = "#6b3fa0"   # architect / Ganesha
TEAL   = "#1a7a6e"   # worker
ORANGE = "#c85a00"   # validator / Lakshmi
AMBER  = "#b87800"   # deliverable / artifact
GREEN  = "#1a6e2e"   # value / YES
RED    = "#c0392b"   # plugins skipped / WITHOUT

ROLE_HEX = {
    "human":       BLUE,
    "orchestrator":MID,
    "architect":   PURPLE,
    "worker":      TEAL,
    "validator":   ORANGE,
    "memory":      MID,
    "deliverable": AMBER,
    "skipped":     DIM,
}
VERDICT_STYLE = {
    "YES":   (GREEN, "#f0fff4"),
    "NO":    (RED,   "#fff5f5"),
    "AMBER": (AMBER, "#fffbf0"),
}

def rc(role): return ROLE_HEX.get(role, DARK)

# ─── CANVAS ───────────────────────────────────────────────────────────────────
FIG_W, FIG_H = 38, 26
DPI = 130

def make_fig():
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    ax.set_xlim(0, FIG_W); ax.set_ylim(0, FIG_H)
    ax.set_aspect("equal"); ax.axis("off")
    fig.patch.set_facecolor(WHITE); ax.set_facecolor(WHITE)
    return fig, ax

# ─── DRAW HELPERS ─────────────────────────────────────────────────────────────
def rbox(ax, x, y, w, h, fc=WHITE, ec=BORDER, lw=1.2, alpha=1.0, zorder=2):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06",
                       lw=lw, edgecolor=ec, facecolor=fc, alpha=alpha, zorder=zorder)
    ax.add_patch(p)

def t(ax, x, y, s, c=DARK, sz=9, w="normal", ha="left", va="top", z=5):
    ax.text(x, y, s, color=c, fontsize=sz, fontweight=w, ha=ha, va=va, zorder=z)

def arrow(ax, x1, x2, y, color=BLUE, lw=1.8, label="", lc=None):
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=14), zorder=6)
    if label:
        mx = (x1+x2)/2
        lc = lc or color
        ax.text(mx, y+0.13, label, ha="center", va="bottom", color=lc,
                fontsize=7.5, fontweight="bold", zorder=7,
                bbox=dict(boxstyle="round,pad=0.12", fc=WHITE, ec=lc, lw=0.8))

def hline(ax, x1, x2, y, c=BORDER, lw=0.7):
    ax.plot([x1, x2], [y, y], color=c, lw=lw, zorder=3)

def section_header(ax, x, y, w, label, color):
    rbox(ax, x, y-0.32, w, 0.32, fc=color, ec=color, lw=0, zorder=4)
    t(ax, x+w/2, y-0.02, label, c=WHITE, sz=9, w="bold", ha="center", va="top", z=5)

def icon_circle(ax, cx, cy, r, color, symbol, sz=12):
    circ = plt.Circle((cx, cy), r, fc=color, ec=color, lw=0, zorder=6)
    ax.add_patch(circ)
    t(ax, cx, cy+0.02, symbol, c=WHITE, sz=sz, w="bold", ha="center", va="center", z=7)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN RENDER
# ══════════════════════════════════════════════════════════════════════════════
def render(schema_path, out_base):
    with open(schema_path) as f:
        d = json.load(f)

    fig, ax = make_fig()

    m        = d["mission"]
    req      = d["request"]
    cols_d   = d["team_columns"]
    handoffs = d["handoffs"]
    plugins  = d["plugins_skipped"]
    arch     = d["architecture_view"]
    team_v   = d["team_view"]
    val_v    = d["value_view"]
    metrics  = d["metrics"]
    verdict  = d["verdict"]
    without  = d["without_yos"]
    with_y   = d["with_yos"]

    # ── TITLE ──────────────────────────────────────────────────────────────────
    t(ax, FIG_W/2, FIG_H-0.25, "Y-OS TEAM TRACE — EXECUTION TRACE",
      c=DARK, sz=20, w="bold", ha="center")
    t(ax, FIG_W/2, FIG_H-0.75,
      f"Mission: {m['id']}  •  Date: {m['date']}  •  {m['title']}",
      c=DIM, sz=10, ha="center")
    t(ax, FIG_W-0.3, FIG_H-0.25, f"TRACE ID: {m['trace_id']}",
      c=BLUE, sz=9, w="bold", ha="right")

    # ── YANNICK REQUEST BOX ────────────────────────────────────────────────────
    REQ_X, REQ_Y = 0.25, FIG_H - 1.2
    REQ_W, REQ_H = 2.8, 3.2
    rbox(ax, REQ_X, REQ_Y - REQ_H, REQ_W, REQ_H, fc=CREAM, ec=BLUE, lw=2, zorder=3)
    t(ax, REQ_X+REQ_W/2, REQ_Y-0.18, req["user"].upper(), c=BLUE, sz=11, w="bold", ha="center")
    t(ax, REQ_X+REQ_W/2, REQ_Y-0.45, "REQUEST", c=BLUE, sz=9, ha="center")
    icon_circle(ax, REQ_X+REQ_W/2, REQ_Y-0.9, 0.28, BLUE, req.get("user_icon","Y"), sz=13)
    hline(ax, REQ_X+0.15, REQ_X+REQ_W-0.15, REQ_Y-1.25, BLUE, 0.8)
    t(ax, REQ_X+0.15, REQ_Y-1.35, f'"{req["quote"]}"', c=MID, sz=8.5, va="top")

    # ── TEAM VIEW HEADER ───────────────────────────────────────────────────────
    TEAM_HEADER_Y = FIG_H - 1.1
    TEAM_X_START  = REQ_X + REQ_W + 0.35
    TEAM_AREA_W   = FIG_W - TEAM_X_START - 5.8

    rbox(ax, TEAM_X_START, TEAM_HEADER_Y - 0.38, TEAM_AREA_W, 0.38,
         fc="#e8eef8", ec=BLUE, lw=1.2, zorder=3)
    t(ax, TEAM_X_START + TEAM_AREA_W/2, TEAM_HEADER_Y - 0.04,
      "TEAM VIEW — WHO WORKED", c=BLUE, sz=11, w="bold", ha="center")

    # ── TEAM COLUMNS ───────────────────────────────────────────────────────────
    N_COLS = len(cols_d)
    COL_GAP = 0.18
    COL_W = (TEAM_AREA_W - COL_GAP * (N_COLS-1)) / N_COLS
    COL_TOP = TEAM_HEADER_Y - 0.38
    COL_H = 7.8
    COL_BODY_Y = COL_TOP - COL_H

    for i, col in enumerate(cols_d):
        cx = TEAM_X_START + i * (COL_W + COL_GAP)
        c_ = rc(col["color_role"])

        # Card body
        rbox(ax, cx, COL_BODY_Y, COL_W, COL_H, fc=WHITE, ec=c_, lw=1.5, zorder=3)

        # Numbered header bar
        rbox(ax, cx, COL_BODY_Y + COL_H - 0.55, COL_W, 0.55,
             fc=c_, ec=c_, lw=0, zorder=4)
        t(ax, cx + COL_W/2, COL_BODY_Y + COL_H - 0.04,
          f"{col['num']}  {col['title']}", c=WHITE, sz=8.5, w="bold",
          ha="center", va="top", z=5)

        # Icon circle
        icon_circle(ax, cx + COL_W/2, COL_BODY_Y + COL_H - 1.05, 0.28, c_, col["icon"], sz=11)

        # Fields — support both dict and list-of-tuples
        fields = col["fields"]
        if isinstance(fields, dict):
            field_items = list(fields.items())
        else:
            field_items = [(f["label"], f["value"]) for f in fields]

        fy = COL_BODY_Y + COL_H - 1.55
        for label, val in field_items:
            t(ax, cx + 0.12, fy, label, c=c_, sz=7.5, w="bold", va="top")
            t(ax, cx + 0.12, fy - 0.22, str(val), c=MID, sz=7.5, va="top")
            lines = str(val).count("\n") + 1
            fy -= 0.22 + lines * 0.22 + 0.12
            if fy < COL_BODY_Y + 0.12:
                break

    # Arrows between columns
    for i in range(N_COLS - 1):
        x1 = TEAM_X_START + (i+1) * (COL_W + COL_GAP) - COL_GAP
        x2 = TEAM_X_START + (i+1) * (COL_W + COL_GAP)
        arrow(ax, x1, x2, COL_BODY_Y + COL_H * 0.62, color=BLUE, lw=1.5)

    # Arrow from request box to col 1
    arrow(ax, REQ_X + REQ_W, TEAM_X_START, COL_BODY_Y + COL_H * 0.62, color=BLUE, lw=2)

    # ── ARTIFACT HANDOFFS ROW ──────────────────────────────────────────────────
    HO_Y = COL_BODY_Y - 0.25
    HO_H = 1.6
    rbox(ax, TEAM_X_START, HO_Y - HO_H, TEAM_AREA_W, HO_H,
         fc="#fffbf0", ec=AMBER, lw=1.2, zorder=3)
    t(ax, TEAM_X_START + TEAM_AREA_W/2, HO_Y - 0.18,
      "HAND-OFFS  (ARTIFACTS PASSED BETWEEN TEAM MEMBERS)",
      c=AMBER, sz=9, w="bold", ha="center")

    for i, ho in enumerate(handoffs):
        col_i = i + 1
        if col_i >= N_COLS:
            break
        x1 = TEAM_X_START + col_i * (COL_W + COL_GAP) + COL_W * 0.1
        x2 = TEAM_X_START + (col_i+1) * (COL_W + COL_GAP) - COL_W * 0.1
        if x2 > TEAM_X_START + TEAM_AREA_W:
            break
        y_ho = HO_Y - HO_H/2 - 0.1
        arrow(ax, x1, x2, y_ho, color=AMBER, lw=1.5, label=ho["name"], lc=AMBER)
        t(ax, (x1+x2)/2, y_ho - 0.22, ho.get("detail",""), c=DIM, sz=7, ha="center", va="top")

    # ── PLUGINS NOT ACTIVATED ──────────────────────────────────────────────────
    PL_X = 0.25
    PL_Y = COL_BODY_Y - 0.1
    PL_W = REQ_W
    PL_H = HO_H + COL_H - REQ_H - 0.1

    rbox(ax, PL_X, PL_Y - PL_H, PL_W, PL_H, fc="#fff5f5", ec=RED, lw=1.5, zorder=3)
    t(ax, PL_X + PL_W/2, PL_Y - 0.2, "PLUGINS", c=RED, sz=9, w="bold", ha="center")
    t(ax, PL_X + PL_W/2, PL_Y - 0.48, "NOT ACTIVATED", c=RED, sz=8.5, w="bold", ha="center")
    t(ax, PL_X + PL_W/2, PL_Y - 0.72, "(Core-Only Mode)", c=DIM, sz=8, ha="center")
    hline(ax, PL_X+0.15, PL_X+PL_W-0.15, PL_Y-0.85, RED, 0.8)

    py = PL_Y - 1.05
    for p in plugins:
        t(ax, PL_X + 0.18, py, "✕", c=RED, sz=10, w="bold", va="top")
        t(ax, PL_X + 0.45, py, p["name"], c=RED, sz=8.5, w="bold", va="top")
        if p.get("desc"):
            t(ax, PL_X + 0.45, py - 0.28, p["desc"], c=DIM, sz=7.5, va="top")
        t(ax, PL_X + 0.45, py - 0.55, "✕ SKIPPED", c=RED, sz=7.5, va="top")
        py -= 1.1

    reason = d.get("plugins_skipped_reason", "Core-Only Mode")
    t(ax, PL_X + 0.15, PL_Y - PL_H + 0.55, "Reason:", c=MID, sz=8, w="bold")
    t(ax, PL_X + 0.15, PL_Y - PL_H + 0.32, reason, c=DIM, sz=7.5)

    # ── 3 SYNCHRONIZED VIEWS ──────────────────────────────────────────────────
    VIEWS_Y = HO_Y - HO_H - 0.3
    VIEWS_H = 3.8
    VIEWS_X = 0.25
    VIEWS_W = FIG_W - 0.25 - 5.8
    VIEW_W  = (VIEWS_W - 0.6) / 3

    # View 1 — Architecture
    V1_X = VIEWS_X
    rbox(ax, V1_X, VIEWS_Y - VIEWS_H, VIEW_W, VIEWS_H, fc=CREAM, ec=BLUE, lw=1.5, zorder=3)
    section_header(ax, V1_X, VIEWS_Y, VIEW_W, "View 1 — ARCHITECTURE VIEW (Validation)", BLUE)

    arch_steps = arch["steps"]
    step_w = (VIEW_W - 0.4) / len(arch_steps) - 0.12
    step_y = VIEWS_Y - VIEWS_H + 1.8
    for j, step in enumerate(arch_steps):
        sx = V1_X + 0.2 + j * (step_w + 0.12)
        sc = rc(step["color_role"])
        rbox(ax, sx, step_y, step_w, 0.8, fc=sc, ec=sc, lw=0, zorder=4)
        t(ax, sx + step_w/2, step_y + 0.75,
          f"{step['label']}\n{step['sub']}", c=WHITE, sz=7.5, w="bold",
          ha="center", va="top", z=5)
        if j < len(arch_steps)-1:
            arrow(ax, sx + step_w, sx + step_w + 0.12, step_y + 0.4, color=BLUE, lw=1.2)

    t(ax, V1_X + VIEW_W/2, VIEWS_Y - VIEWS_H + 1.4,
      arch.get("summary",""), c=DARK, sz=8.5, w="bold", ha="center")
    t(ax, V1_X + VIEW_W/2, VIEWS_Y - VIEWS_H + 1.0,
      arch.get("plugins_note",""), c=RED, sz=8.5, w="bold", ha="center")
    t(ax, V1_X + VIEW_W/2, VIEWS_Y - VIEWS_H + 0.6,
      arch.get("task_type_note",""), c=GREEN, sz=8, ha="center")

    # View 2 — Team
    V2_X = V1_X + VIEW_W + 0.3
    rbox(ax, V2_X, VIEWS_Y - VIEWS_H, VIEW_W, VIEWS_H, fc=CREAM, ec=PURPLE, lw=1.5, zorder=3)
    section_header(ax, V2_X, VIEWS_Y, VIEW_W, "View 2 — TEAM VIEW (Who Worked)", PURPLE)

    icons_per_row = 4
    for j, ic in enumerate(team_v["icons"]):
        row = j // icons_per_row
        col_j = j % icons_per_row
        ix = V2_X + 0.5 + col_j * (VIEW_W - 0.6) / icons_per_row
        iy = VIEWS_Y - 1.1 - row * 1.1
        icon_circle(ax, ix, iy, 0.22, rc(ic["color_role"]), ic["sym"], sz=9)
        t(ax, ix, iy - 0.28, ic["name"], c=MID, sz=7, ha="center", va="top")

    t(ax, V2_X + VIEW_W/2, VIEWS_Y - VIEWS_H + 0.85,
      team_v.get("tagline",""), c=DARK, sz=8, w="bold", ha="center")
    t(ax, V2_X + VIEW_W/2, VIEWS_Y - VIEWS_H + 0.5,
      team_v.get("tagline2",""), c=DIM, sz=7.5, ha="center")

    # View 3 — Value
    V3_X = V2_X + VIEW_W + 0.3
    rbox(ax, V3_X, VIEWS_Y - VIEWS_H, VIEW_W, VIEWS_H, fc="#fffef0", ec=AMBER, lw=1.5, zorder=3)
    section_header(ax, V3_X, VIEWS_Y, VIEW_W, "View 3 — VALUE VIEW (What Was Created)", AMBER)

    kpis = val_v["kpis"]
    vbox_w = (VIEW_W - 0.5) / len(kpis) - 0.1
    vbox_y = VIEWS_Y - 1.0
    for j, kpi in enumerate(kpis):
        vx = V3_X + 0.25 + j * (vbox_w + 0.1)
        rbox(ax, vx, vbox_y - 1.2, vbox_w, 1.2, fc=WHITE, ec=AMBER, lw=1.2, zorder=4)
        t(ax, vx + vbox_w/2, vbox_y - 0.18, kpi["num"],
          c=AMBER, sz=18, w="bold", ha="center", va="top", z=5)
        t(ax, vx + vbox_w/2, vbox_y - 0.75, kpi["label"],
          c=MID, sz=7, ha="center", va="top", z=5)

    t(ax, V3_X + VIEW_W/2, VIEWS_Y - VIEWS_H + 0.65,
      val_v.get("summary",""), c=GREEN, sz=9, w="bold", ha="center")
    t(ax, V3_X + VIEW_W/2, VIEWS_Y - VIEWS_H + 0.32,
      val_v.get("note",""), c=DIM, sz=7.5, ha="center")

    # ── WITHOUT vs WITH Y-OS ────────────────────────────────────────────────────
    CMP_Y = VIEWS_Y - VIEWS_H - 0.3
    CMP_H = 3.2
    CMP_W = (VIEWS_W - 0.5) / 2

    # WITHOUT
    rbox(ax, VIEWS_X, CMP_Y - CMP_H, CMP_W, CMP_H, fc="#fff5f5", ec=RED, lw=1.5, zorder=3)
    section_header(ax, VIEWS_X, CMP_Y, CMP_W, "WITHOUT Y-OS  (MANUAL PROCESS)", RED)

    steps_w = without["steps"]
    step_bw = (CMP_W - 0.4) / len(steps_w) - 0.08
    for j, step in enumerate(steps_w):
        sx = VIEWS_X + 0.2 + j * (step_bw + 0.08)
        rbox(ax, sx, CMP_Y - CMP_H + 1.2, step_bw, 1.0, fc=WHITE, ec=LIGHT_BORDER, lw=0.8, zorder=4)
        t(ax, sx + step_bw/2, CMP_Y - CMP_H + 2.1, step, c=MID, sz=7.5, ha="center", va="top", z=5)
        if j < len(steps_w)-1:
            t(ax, sx + step_bw + 0.01, CMP_Y - CMP_H + 1.72, "→", c=RED, sz=9, ha="center", z=5)

    rbox(ax, VIEWS_X + CMP_W/2 - 1.2, CMP_Y - CMP_H + 0.15, 2.4, 0.9,
         fc="#fde8e8", ec=RED, lw=1, zorder=4)
    t(ax, VIEWS_X + CMP_W/2, CMP_Y - CMP_H + 0.95,
      without.get("time_estimate",""), c=RED, sz=11, w="bold", ha="center")
    t(ax, VIEWS_X + CMP_W/2, CMP_Y - CMP_H + 0.55,
      without.get("note",""), c=RED, sz=8, ha="center")

    t(ax, VIEWS_X + CMP_W + 0.25, CMP_Y - CMP_H/2,
      "VS", c=DARK, sz=16, w="bold", ha="center", va="center")

    # WITH
    WITH_X = VIEWS_X + CMP_W + 0.5
    rbox(ax, WITH_X, CMP_Y - CMP_H, CMP_W, CMP_H, fc="#f0fff4", ec=GREEN, lw=2, zorder=3)
    section_header(ax, WITH_X, CMP_Y, CMP_W, "WITH Y-OS  (AUTOMATED WITH GOVERNANCE)", GREEN)

    steps_y = with_y["steps"]
    step_bw2 = (CMP_W - 0.4) / len(steps_y) - 0.1
    for j, step in enumerate(steps_y):
        sx = WITH_X + 0.2 + j * (step_bw2 + 0.1)
        rbox(ax, sx, CMP_Y - CMP_H + 1.2, step_bw2, 1.0, fc=WHITE, ec=GREEN, lw=1, zorder=4)
        icon_circle(ax, sx + step_bw2/2, CMP_Y - CMP_H + 1.95, 0.2, GREEN, str(j+1), sz=8)
        t(ax, sx + step_bw2/2, CMP_Y - CMP_H + 1.65, step, c=MID, sz=7.5, ha="center", va="top", z=5)
        if j < len(steps_y)-1:
            t(ax, sx + step_bw2 + 0.02, CMP_Y - CMP_H + 1.72, "→", c=GREEN, sz=9, ha="center", z=5)

    rbox(ax, WITH_X + CMP_W/2 - 1.2, CMP_Y - CMP_H + 0.15, 2.4, 0.9,
         fc="#d1fae5", ec=GREEN, lw=1, zorder=4)
    t(ax, WITH_X + CMP_W/2, CMP_Y - CMP_H + 0.95,
      with_y.get("time_estimate",""), c=GREEN, sz=14, w="bold", ha="center")
    t(ax, WITH_X + CMP_W/2, CMP_Y - CMP_H + 0.55,
      with_y.get("note",""), c=GREEN, sz=8, ha="center")

    # ── RUNTIME METRICS PANEL ──────────────────────────────────────────────────
    MP_X = FIG_W - 5.5
    MP_Y = FIG_H - 1.1
    MP_W = 5.2
    MP_H = FIG_H - 1.4

    rbox(ax, MP_X, MP_Y - MP_H, MP_W, MP_H, fc=CREAM, ec=DARK, lw=2, zorder=3)
    rbox(ax, MP_X, MP_Y - 0.42, MP_W, 0.42, fc=DARK, ec=DARK, lw=0, zorder=4)
    t(ax, MP_X + MP_W/2, MP_Y - 0.06, "RUNTIME METRICS",
      c=WHITE, sz=10, w="bold", ha="center", z=5)

    met_items = [
        ("⏱", "Total Time",       metrics["total_time"]),
        ("$", "Total Cost",        metrics["total_cost"]),
        ("#", "Total Tokens",      metrics["total_tokens"]),
        ("M", "Models Used",       metrics["models_used"]),
        ("T", "Tools Used",        metrics["tools_used"]),
        ("A", "Artifacts Created", metrics["artifacts_created"]),
        ("✕", "Plugins Skipped",   metrics["plugins_skipped"]),
    ]
    my = MP_Y - 0.65
    for icon_s, label, val in met_items:
        t(ax, MP_X + 0.25, my, icon_s, c=BLUE, sz=12, va="top")
        t(ax, MP_X + 0.65, my, label, c=DARK, sz=9, w="bold", va="top")
        lines = str(val).count("\n") + 1
        t(ax, MP_X + 0.65, my - 0.28, str(val), c=MID, sz=8.5, va="top")
        hline(ax, MP_X + 0.2, MP_X + MP_W - 0.2,
              my - 0.28 - lines * 0.26 - 0.1, LIGHT_BORDER, 0.6)
        my -= 0.28 + lines * 0.26 + 0.28

    # ── VERDICT BOX ───────────────────────────────────────────────────────────
    ans = verdict["answer"]
    vd_fg, vd_bg = VERDICT_STYLE.get(ans, (GREEN, "#f0fff4"))

    VD_X = MP_X
    VD_Y = CMP_Y
    VD_W = MP_W
    VD_H = CMP_H

    rbox(ax, VD_X, VD_Y - VD_H, VD_W, VD_H, fc=vd_bg, ec=vd_fg, lw=2, zorder=3)
    section_header(ax, VD_X, VD_Y, VD_W, "DID Y-OS CREATE VALUE?", vd_fg)

    rbox(ax, VD_X + 0.3, VD_Y - 1.5, VD_W - 0.6, 0.9, fc=vd_fg, ec=vd_fg, lw=0, zorder=4)
    t(ax, VD_X + VD_W/2, VD_Y - 0.72, ans, c=WHITE, sz=22, w="bold", ha="center", z=5)

    cy = VD_Y - 1.75
    for reason in verdict.get("reasons", []):
        t(ax, VD_X + 0.25, cy, reason, c=vd_fg, sz=8, va="top")
        cy -= 0.38

    # ── SAVE PNG + SVG ────────────────────────────────────────────────────────
    plt.tight_layout(pad=0)
    plt.savefig(out_base + ".png", format="png", dpi=DPI, bbox_inches="tight",
                facecolor=WHITE, edgecolor="none")
    plt.savefig(out_base + ".svg", format="svg", dpi=DPI, bbox_inches="tight",
                facecolor=WHITE, edgecolor="none")
    plt.close()
    print(f"PNG: {out_base}.png")
    print(f"SVG: {out_base}.svg")

    # ── EXCALIDRAW ────────────────────────────────────────────────────────────
    _build_excalidraw(d, out_base + ".excalidraw")
    print(f"Excalidraw: {out_base}.excalidraw")


# ══════════════════════════════════════════════════════════════════════════════
# EXCALIDRAW BUILDER (lightweight — main visual is the PNG/SVG)
# ══════════════════════════════════════════════════════════════════════════════
def _uid(): return str(uuid.uuid4())[:8]

def _ex_rect(x, y, w, h, bg="#ffffff", stroke="#333333", lw=1, label="", sz=14, bold=False, color="#000000"):
    els = [{"id": _uid(), "type": "rectangle", "x": x, "y": y, "width": w, "height": h,
            "backgroundColor": bg, "strokeColor": stroke, "strokeWidth": lw,
            "fillStyle": "solid", "roughness": 1, "opacity": 100,
            "roundness": {"type": 3, "value": 8}}]
    if label:
        els.append({"id": _uid(), "type": "text", "x": x+w/2, "y": y+h/2,
                    "text": label, "fontSize": sz, "fontFamily": 1,
                    "textAlign": "center", "verticalAlign": "middle",
                    "strokeColor": color, "backgroundColor": "transparent",
                    "fillStyle": "solid", "roughness": 1, "opacity": 100,
                    "width": len(label)*sz*0.6, "height": sz*1.4,
                    "fontWeight": "bold" if bold else "normal"})
    return els

SCALE = 28

def _m2e(x, y): return x * SCALE, (FIG_H - y) * SCALE

def _build_excalidraw(d, out_path):
    elements = []
    m = d["mission"]; req = d["request"]

    # Title
    tx, ty = _m2e(FIG_W/2, FIG_H-0.25)
    elements.append({"id": _uid(), "type": "text", "x": tx, "y": ty,
                     "text": "Y-OS TEAM TRACE — EXECUTION TRACE",
                     "fontSize": 22, "fontFamily": 1, "textAlign": "center",
                     "verticalAlign": "middle", "strokeColor": "#111111",
                     "backgroundColor": "transparent", "fillStyle": "solid",
                     "roughness": 1, "opacity": 100, "width": 600, "height": 30})

    # Request box
    REQ_X, REQ_Y = 0.25, FIG_H - 1.2
    REQ_W, REQ_H = 2.8, 3.2
    rx, ry = _m2e(REQ_X, REQ_Y - REQ_H)
    elements += _ex_rect(rx, ry - REQ_H*SCALE, REQ_W*SCALE, REQ_H*SCALE,
                         bg="#fafaf8", stroke=BLUE, lw=2,
                         label=f"{req['user']}\nREQUEST\n{req['quote']}", sz=11, color=BLUE)

    # Team columns
    TEAM_X_START = REQ_X + REQ_W + 0.35
    TEAM_AREA_W  = FIG_W - TEAM_X_START - 5.8
    cols_d = d["team_columns"]
    N_COLS = len(cols_d)
    COL_GAP = 0.18
    COL_W = (TEAM_AREA_W - COL_GAP * (N_COLS-1)) / N_COLS
    COL_H = 7.8
    TEAM_HEADER_Y = FIG_H - 1.1
    COL_BODY_Y = TEAM_HEADER_Y - 0.38 - COL_H

    for i, col in enumerate(cols_d):
        cx = TEAM_X_START + i * (COL_W + COL_GAP)
        c_ = ROLE_HEX.get(col["color_role"], DARK)
        ecx, ecy = _m2e(cx, COL_BODY_Y + COL_H)
        elements += _ex_rect(ecx, ecy - COL_H*SCALE, COL_W*SCALE, COL_H*SCALE,
                              bg="#ffffff", stroke=c_, lw=2,
                              label=f"{col['num']} {col['title']}", sz=9, bold=True, color=c_)

    # Verdict
    verdict = d["verdict"]
    ans = verdict["answer"]
    vd_fg, vd_bg = VERDICT_STYLE.get(ans, (GREEN, "#f0fff4"))
    CMP_Y = TEAM_HEADER_Y - 0.38 - COL_H - 1.6 - 0.3 - 3.8 - 0.3
    VD_H = 3.2
    MP_X = FIG_W - 5.5
    MP_W = 5.2
    vdx, vdy = _m2e(MP_X, CMP_Y)
    elements += _ex_rect(vdx, vdy - VD_H*SCALE, MP_W*SCALE, VD_H*SCALE,
                          bg=vd_bg, stroke=vd_fg, lw=2,
                          label=f"DID Y-OS CREATE VALUE?\n{ans}", sz=20, bold=True, color=vd_fg)

    obj = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
           "elements": elements, "appState": {"viewBackgroundColor": "#ffffff"}, "files": {}}
    with open(out_path, "w") as f:
        json.dump(obj, f, indent=2)


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 render_value_trace.py <schema.json> <output_base>")
        sys.exit(1)
    render(sys.argv[1], sys.argv[2])
