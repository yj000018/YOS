#!/usr/bin/env python3
"""
render_value_trace.py
Y-OS Value Trace Renderer v2.0

Usage:
    python3 render_value_trace.py <schema.json> <output_base>

Example:
    python3 render_value_trace.py value_trace_schema.json ./output/my_mission

Produces:
    my_mission.png
    my_mission.svg
    my_mission.excalidraw
"""
import sys
import json
import math
import uuid
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

# ─── COLOR PALETTE ────────────────────────────────────────────────────────────
WHITE  = "#ffffff"; CREAM = "#fafaf8"
BORDER = "#333333"; DARK  = "#111111"; MID   = "#444444"; DIM = "#888888"
LIGHT_BORDER = "#cccccc"

ROLE_COLORS = {
    "human":       "#1a4fa0",
    "orchestrator":"#444444",
    "architect":   "#6b3fa0",
    "worker":      "#1a7a6e",
    "validator":   "#c85a00",
    "memory":      "#444444",
    "deliverable": "#b87800",
    "skipped":     "#888888",
}
VERDICT_COLORS = {
    "YES":   ("#1a6e2e", "#f0fff4"),
    "NO":    ("#c0392b", "#fff5f5"),
    "AMBER": ("#b87800", "#fffbf0"),
}
RED   = "#c0392b"
GREEN = "#1a6e2e"
AMBER = "#b87800"

def col(role):
    return ROLE_COLORS.get(role, DARK)

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
def rbox(ax, x, y, w, h, fc=WHITE, ec=BORDER, lw=1.2, zorder=2):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06",
                       lw=lw, edgecolor=ec, facecolor=fc, zorder=zorder)
    ax.add_patch(p)

def t(ax, x, y, s, c=DARK, sz=9, w="normal", ha="left", va="top", z=5):
    ax.text(x, y, s, color=c, fontsize=sz, fontweight=w, ha=ha, va=va, zorder=z)

def arrow(ax, x1, x2, y, color=BORDER, lw=1.5, label="", lc=None):
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=13), zorder=6)
    if label:
        mx = (x1+x2)/2
        lc = lc or color
        ax.text(mx, y+0.13, label, ha="center", va="bottom", color=lc,
                fontsize=7.5, fontweight="bold", zorder=7,
                bbox=dict(boxstyle="round,pad=0.12", fc=WHITE, ec=lc, lw=0.8))

def hline(ax, x1, x2, y, c=BORDER, lw=0.7):
    ax.plot([x1, x2], [y, y], color=c, lw=lw, zorder=3)

def icon_circle(ax, cx, cy, r, color, symbol, sz=11):
    circ = plt.Circle((cx, cy), r, fc=color, ec=color, lw=0, zorder=6)
    ax.add_patch(circ)
    t(ax, cx, cy+0.02, symbol, c=WHITE, sz=sz, w="bold", ha="center", va="center", z=7)

def section_header(ax, x, y, w, label, color):
    rbox(ax, x, y-0.32, w, 0.32, fc=color, ec=color, lw=0, zorder=4)
    t(ax, x+w/2, y-0.04, label, c=WHITE, sz=9, w="bold", ha="center", va="top", z=5)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN RENDER FUNCTION
# ══════════════════════════════════════════════════════════════════════════════
def render(schema_path, out_base):
    with open(schema_path) as f:
        d = json.load(f)

    fig, ax = make_fig()
    m = d["mission"]
    req = d["request"]
    cols_data = d["team_columns"]
    handoffs = d["handoffs"]
    plugins = d["plugins_skipped"]
    arch = d["architecture_view"]
    team_v = d["team_view"]
    val_v = d["value_view"]
    metrics = d["metrics"]
    verdict = d["verdict"]
    without = d["without_yos"]
    with_yos = d["with_yos"]

    # ── TITLE ──────────────────────────────────────────────────────────────────
    t(ax, FIG_W/2, FIG_H-0.25, "Y-OS TEAM TRACE — EXECUTION TRACE",
      c=DARK, sz=20, w="bold", ha="center")
    t(ax, FIG_W/2, FIG_H-0.75,
      f"Mission: {m['id']}  •  Date: {m['date']}  •  {m['title']}",
      c=DIM, sz=10, ha="center")
    t(ax, FIG_W-0.3, FIG_H-0.25, f"TRACE ID: {m['trace_id']}",
      c=col("human"), sz=9, w="bold", ha="right")

    # ── YANNICK REQUEST BOX ────────────────────────────────────────────────────
    REQ_X, REQ_Y = 0.25, FIG_H - 1.2
    REQ_W, REQ_H = 2.8, 3.2
    rbox(ax, REQ_X, REQ_Y - REQ_H, REQ_W, REQ_H, fc=CREAM, ec=col("human"), lw=2, zorder=3)
    t(ax, REQ_X+REQ_W/2, REQ_Y-0.18, req["user"], c=col("human"), sz=11, w="bold", ha="center")
    t(ax, REQ_X+REQ_W/2, REQ_Y-0.45, "REQUEST", c=col("human"), sz=9, ha="center")
    icon_circle(ax, REQ_X+REQ_W/2, REQ_Y-0.9, 0.28, col("human"), req["user_icon"], sz=13)
    hline(ax, REQ_X+0.15, REQ_X+REQ_W-0.15, REQ_Y-1.25, col("human"), 0.8)
    t(ax, REQ_X+0.15, REQ_Y-1.35, f'"{req["quote"]}"', c=MID, sz=8.5, va="top")

    # ── TEAM VIEW HEADER ───────────────────────────────────────────────────────
    TEAM_HEADER_Y = FIG_H - 1.1
    TEAM_X_START  = REQ_X + REQ_W + 0.35
    TEAM_AREA_W   = FIG_W - TEAM_X_START - 5.8

    rbox(ax, TEAM_X_START, TEAM_HEADER_Y - 0.38, TEAM_AREA_W, 0.38,
         fc="#e8eef8", ec=col("human"), lw=1.2, zorder=3)
    t(ax, TEAM_X_START + TEAM_AREA_W/2, TEAM_HEADER_Y - 0.04,
      "TEAM VIEW — WHO WORKED", c=col("human"), sz=11, w="bold", ha="center")

    # ── TEAM COLUMNS ───────────────────────────────────────────────────────────
    N_COLS = len(cols_data)
    COL_GAP = 0.18
    COL_W = (TEAM_AREA_W - COL_GAP * (N_COLS-1)) / N_COLS
    COL_TOP = TEAM_HEADER_Y - 0.38
    COL_H = 7.8
    COL_BODY_Y = COL_TOP - COL_H

    for i, cd in enumerate(cols_data):
        cx = TEAM_X_START + i * (COL_W + COL_GAP)
        c_ = col(cd["color_role"])
        rbox(ax, cx, COL_BODY_Y, COL_W, COL_H, fc=WHITE, ec=c_, lw=1.5, zorder=3)
        rbox(ax, cx, COL_BODY_Y + COL_H - 0.55, COL_W, 0.55, fc=c_, ec=c_, lw=0, zorder=4)
        t(ax, cx + COL_W/2, COL_BODY_Y + COL_H - 0.04,
          f"{cd['num']}  {cd['title']}", c=WHITE, sz=8.5, w="bold", ha="center", va="top", z=5)
        icon_circle(ax, cx + COL_W/2, COL_BODY_Y + COL_H - 1.05, 0.28, c_, cd["icon"], sz=11)
        fy = COL_BODY_Y + COL_H - 1.55
        for label, val in cd["fields"].items():
            t(ax, cx + 0.12, fy, label, c=c_, sz=7.5, w="bold", va="top")
            t(ax, cx + 0.12, fy - 0.22, val, c=MID, sz=7.5, va="top")
            lines = val.count("\n") + 1
            fy -= 0.22 + lines * 0.22 + 0.12
            if fy < COL_BODY_Y + 0.12:
                break

    # Arrows between columns
    for i in range(N_COLS - 1):
        x1 = TEAM_X_START + (i+1) * (COL_W + COL_GAP) - COL_GAP
        x2 = TEAM_X_START + (i+1) * (COL_W + COL_GAP)
        arrow(ax, x1, x2, COL_BODY_Y + COL_H * 0.62, color=col("human"), lw=1.5)
    arrow(ax, REQ_X + REQ_W, TEAM_X_START, COL_BODY_Y + COL_H * 0.62, color=col("human"), lw=2)

    # ── ARTIFACT HANDOFFS ROW ──────────────────────────────────────────────────
    HO_Y = COL_BODY_Y - 0.25
    HO_H = 1.6
    rbox(ax, TEAM_X_START, HO_Y - HO_H, TEAM_AREA_W, HO_H, fc="#fffbf0", ec=AMBER, lw=1.2, zorder=3)
    t(ax, TEAM_X_START + TEAM_AREA_W/2, HO_Y - 0.18,
      "HAND-OFFS  (ARTIFACTS PASSED BETWEEN TEAM MEMBERS)",
      c=AMBER, sz=9, w="bold", ha="center")

    for i, ho in enumerate(handoffs):
        col_i = i + 1
        x1 = TEAM_X_START + col_i * (COL_W + COL_GAP) + COL_W * 0.1
        x2 = TEAM_X_START + (col_i+1) * (COL_W + COL_GAP) - COL_W * 0.1
        y_ho = HO_Y - HO_H/2 - 0.1
        arrow(ax, x1, x2, y_ho, color=AMBER, lw=1.5, label=ho["name"], lc=AMBER)
        t(ax, (x1+x2)/2, y_ho - 0.22, ho["detail"], c=DIM, sz=7, ha="center", va="top")

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

    t(ax, PL_X + 0.15, PL_Y - PL_H + 0.55, "Reason:", c=MID, sz=8, w="bold")
    t(ax, PL_X + 0.15, PL_Y - PL_H + 0.32, d["plugins_skipped_reason"], c=DIM, sz=7.5)

    # ── 3 SYNCHRONIZED VIEWS ──────────────────────────────────────────────────
    VIEWS_Y = HO_Y - HO_H - 0.3
    VIEWS_H = 3.8
    VIEWS_X = 0.25
    VIEWS_W = FIG_W - 0.25 - 5.8
    VIEW_W  = (VIEWS_W - 0.6) / 3

    # View 1 — Architecture
    V1_X = VIEWS_X
    rbox(ax, V1_X, VIEWS_Y - VIEWS_H, VIEW_W, VIEWS_H, fc=CREAM, ec=col("human"), lw=1.5, zorder=3)
    section_header(ax, V1_X, VIEWS_Y, VIEW_W, "View 1 — ARCHITECTURE VIEW (Validation)", col("human"))

    arch_steps = arch["steps"]
    aw = (VIEW_W - 0.4) / len(arch_steps)
    for j, step in enumerate(arch_steps):
        ax_ = V1_X + 0.2 + j * aw
        c_ = col(step["color_role"])
        rbox(ax, ax_, VIEWS_Y - 1.5, aw - 0.1, 0.7, fc=c_, ec=c_, lw=0, zorder=4)
        t(ax, ax_ + (aw-0.1)/2, VIEWS_Y - 1.12, step["label"], c=WHITE, sz=8, w="bold", ha="center", va="top", z=5)
        t(ax, ax_ + (aw-0.1)/2, VIEWS_Y - 1.42, step["sub"], c=WHITE, sz=7, ha="center", va="top", z=5)
        if j < len(arch_steps)-1:
            arrow(ax, ax_ + aw - 0.1, ax_ + aw, VIEWS_Y - 1.15, color=BORDER, lw=1.2)

    t(ax, V1_X + VIEW_W/2, VIEWS_Y - 2.1, arch["summary"], c=DARK, sz=8.5, w="bold", ha="center")
    t(ax, V1_X + VIEW_W/2, VIEWS_Y - 2.45, arch["plugins_note"], c=RED, sz=8.5, w="bold", ha="center")
    t(ax, V1_X + VIEW_W/2, VIEWS_Y - 2.8, arch["task_type_note"], c=GREEN, sz=8, ha="center")

    # View 2 — Team
    V2_X = V1_X + VIEW_W + 0.3
    rbox(ax, V2_X, VIEWS_Y - VIEWS_H, VIEW_W, VIEWS_H, fc=CREAM, ec=col("architect"), lw=1.5, zorder=3)
    section_header(ax, V2_X, VIEWS_Y, VIEW_W, "View 2 — TEAM VIEW (Who Worked)", col("architect"))

    icons_per_row = 4
    for j, ic in enumerate(team_v["icons"]):
        row = j // icons_per_row
        col_j = j % icons_per_row
        ix = V2_X + 0.5 + col_j * (VIEW_W - 0.6) / icons_per_row
        iy = VIEWS_Y - 1.1 - row * 1.1
        icon_circle(ax, ix, iy, 0.22, col(ic["color_role"]), ic["sym"], sz=10)
        t(ax, ix, iy - 0.3, ic["name"], c=MID, sz=6.5, ha="center", va="top", z=5)

    t(ax, V2_X + VIEW_W/2, VIEWS_Y - 3.1, team_v["tagline"], c=DARK, sz=8, w="bold", ha="center")
    t(ax, V2_X + VIEW_W/2, VIEWS_Y - 3.4, team_v["tagline2"], c=DIM, sz=7.5, ha="center")

    # View 3 — Value
    V3_X = V2_X + VIEW_W + 0.3
    rbox(ax, V3_X, VIEWS_Y - VIEWS_H, VIEW_W, VIEWS_H, fc="#fffbf0", ec=AMBER, lw=1.5, zorder=3)
    section_header(ax, V3_X, VIEWS_Y, VIEW_W, "View 3 — VALUE VIEW (What Was Created)", AMBER)

    kpis = val_v["kpis"]
    vw = (VIEW_W - 0.4) / len(kpis)
    for j, kpi in enumerate(kpis):
        vx = V3_X + 0.2 + j * vw
        rbox(ax, vx, VIEWS_Y - 2.2, vw - 0.1, 1.1, fc=WHITE, ec=AMBER, lw=1.2, zorder=4)
        t(ax, vx + (vw-0.1)/2, VIEWS_Y - 1.25, kpi["num"], c=AMBER, sz=18, w="bold", ha="center", va="top", z=5)
        t(ax, vx + (vw-0.1)/2, VIEWS_Y - 1.9, kpi["label"], c=MID, sz=7, ha="center", va="top", z=5)

    t(ax, V3_X + VIEW_W/2, VIEWS_Y - 2.55, val_v["summary"], c=GREEN, sz=8.5, w="bold", ha="center")
    t(ax, V3_X + VIEW_W/2, VIEWS_Y - 2.9, val_v["note"], c=DIM, sz=7.5, ha="center")

    # ── WITHOUT / WITH Y-OS ────────────────────────────────────────────────────
    CMP_Y = VIEWS_Y - VIEWS_H - 0.3
    CMP_H = 3.2
    CMP_W = VIEWS_W
    CMP_X = 0.25
    W1_W = (CMP_W - 0.5) / 2

    # WITHOUT
    rbox(ax, CMP_X, CMP_Y - CMP_H, W1_W, CMP_H, fc="#fff5f5", ec=RED, lw=1.5, zorder=3)
    section_header(ax, CMP_X, CMP_Y, W1_W, "WITHOUT Y-OS  (MANUAL PROCESS)", RED)

    steps_w = without["steps"]
    ms_w = (W1_W - 0.4) / len(steps_w)
    for j, step in enumerate(steps_w):
        sx = CMP_X + 0.2 + j * ms_w
        rbox(ax, sx, CMP_Y - 1.5, ms_w - 0.08, 0.65, fc=WHITE, ec=RED, lw=1, zorder=4)
        t(ax, sx + (ms_w-0.08)/2, CMP_Y - 1.12, step, c=RED, sz=7, ha="center", va="top", z=5)
        if j < len(steps_w)-1:
            arrow(ax, sx + ms_w - 0.08, sx + ms_w, CMP_Y - 1.18, color=RED, lw=1)

    rbox(ax, CMP_X + W1_W/2 - 1.1, CMP_Y - 2.3, 2.2, 0.65, fc="#fde8e8", ec=RED, lw=1.2, zorder=4)
    t(ax, CMP_X + W1_W/2, CMP_Y - 1.95, without["time_estimate"], c=RED, sz=12, w="bold", ha="center")
    t(ax, CMP_X + W1_W/2, CMP_Y - 2.25, without["note"], c=RED, sz=8, ha="center")

    t(ax, CMP_X + W1_W + 0.25, CMP_Y - CMP_H/2, "VS", c=DARK, sz=14, w="bold", ha="center", va="center")

    # WITH
    W2_X = CMP_X + W1_W + 0.5
    W2_W = W1_W
    rbox(ax, W2_X, CMP_Y - CMP_H, W2_W, CMP_H, fc="#f0fff4", ec=GREEN, lw=1.5, zorder=3)
    section_header(ax, W2_X, CMP_Y, W2_W, "WITH Y-OS  (AUTOMATED WITH GOVERNANCE)", GREEN)

    steps_y = with_yos["steps"]
    ys_w = (W2_W - 0.4) / len(steps_y)
    for j, step in enumerate(steps_y):
        yx = W2_X + 0.2 + j * ys_w
        icon_circle(ax, yx + (ys_w-0.08)/2, CMP_Y - 1.18, 0.22, GREEN, str(j+1), sz=9)
        t(ax, yx + (ys_w-0.08)/2, CMP_Y - 1.52, step, c=MID, sz=7, ha="center", va="top", z=5)
        if j < len(steps_y)-1:
            arrow(ax, yx + ys_w - 0.08, yx + ys_w, CMP_Y - 1.18, color=GREEN, lw=1)

    rbox(ax, W2_X + W2_W/2 - 1.1, CMP_Y - 2.3, 2.2, 0.65, fc="#e8f5e9", ec=GREEN, lw=1.2, zorder=4)
    t(ax, W2_X + W2_W/2, CMP_Y - 1.95, with_yos["time_estimate"], c=GREEN, sz=12, w="bold", ha="center")
    t(ax, W2_X + W2_W/2, CMP_Y - 2.25, with_yos["note"], c=GREEN, sz=8, ha="center")

    # ── RUNTIME METRICS PANEL ──────────────────────────────────────────────────
    MET_X = FIG_W - 5.5
    MET_Y = FIG_H - 1.1
    MET_W = 5.25
    MET_H = FIG_H - CMP_Y + CMP_H - 0.5

    rbox(ax, MET_X, MET_Y - MET_H, MET_W, MET_H, fc=CREAM, ec=BORDER, lw=1.5, zorder=3)
    rbox(ax, MET_X, MET_Y - 0.4, MET_W, 0.4, fc=DARK, ec=DARK, lw=0, zorder=4)
    t(ax, MET_X + MET_W/2, MET_Y - 0.05, "RUNTIME METRICS", c=WHITE, sz=10, w="bold", ha="center")

    met_items = [
        ("⏱", "Total Time",       metrics["total_time"]),
        ("$", "Total Cost",        metrics["total_cost"]),
        ("#", "Total Tokens",      metrics["total_tokens"]),
        ("M", "Models Used",       metrics["models_used"]),
        ("T", "Tools Used",        metrics["tools_used"]),
        ("A", "Artifacts Created", metrics["artifacts_created"]),
        ("✕", "Plugins Skipped",   metrics["plugins_skipped"]),
    ]
    my = MET_Y - 0.65
    for icon_s, label, val in met_items:
        t(ax, MET_X + 0.25, my, icon_s, c=col("human"), sz=10, w="bold", va="top")
        t(ax, MET_X + 0.65, my, label, c=DARK, sz=8.5, w="bold", va="top")
        lines = val.count("\n") + 1
        t(ax, MET_X + 0.65, my - 0.26, val, c=MID, sz=8, va="top")
        my -= 0.26 + lines * 0.22 + 0.22
        hline(ax, MET_X + 0.2, MET_X + MET_W - 0.2, my + 0.1, LIGHT_BORDER, 0.5)

    # ── VERDICT BOX ───────────────────────────────────────────────────────────
    VD_X = MET_X
    VD_Y = CMP_Y
    VD_W = MET_W
    VD_H = CMP_H

    ans = verdict["answer"]
    vd_fg, vd_bg = VERDICT_COLORS.get(ans, (GREEN, "#f0fff4"))

    rbox(ax, VD_X, VD_Y - VD_H, VD_W, VD_H, fc=vd_bg, ec=vd_fg, lw=2, zorder=3)
    section_header(ax, VD_X, VD_Y, VD_W, "DID Y-OS CREATE VALUE?", vd_fg)
    rbox(ax, VD_X + 0.3, VD_Y - 1.4, VD_W - 0.6, 0.75, fc=vd_fg, ec=vd_fg, lw=0, zorder=4)
    t(ax, VD_X + VD_W/2, VD_Y - 0.85, ans, c=WHITE, sz=22, w="bold", ha="center", va="top", z=5)

    cy = VD_Y - 1.65
    for reason in verdict["reasons"]:
        t(ax, VD_X + 0.25, cy, reason, c=vd_fg, sz=8, va="top")
        cy -= 0.28

    # ── SAVE PNG + SVG ────────────────────────────────────────────────────────
    plt.savefig(out_base + ".png", format="png", dpi=DPI, bbox_inches="tight",
                facecolor=WHITE, edgecolor="none")
    plt.savefig(out_base + ".svg", format="svg", dpi=DPI, bbox_inches="tight",
                facecolor=WHITE, edgecolor="none")
    plt.close()
    print(f"PNG: {out_base}.png")
    print(f"SVG: {out_base}.svg")

    # ── BUILD EXCALIDRAW ──────────────────────────────────────────────────────
    build_excalidraw(d, out_base + ".excalidraw")
    print(f"Excalidraw: {out_base}.excalidraw")


# ══════════════════════════════════════════════════════════════════════════════
# EXCALIDRAW BUILDER
# ══════════════════════════════════════════════════════════════════════════════
def uid():
    return str(uuid.uuid4())[:8]

def ex_rect(x, y, w, h, bg="#ffffff", stroke="#333333", lw=1, label="", font_sz=14,
            bold=False, color="#000000", zorder=1, corner=8):
    el = {
        "id": uid(), "type": "rectangle", "x": x, "y": y, "width": w, "height": h,
        "backgroundColor": bg, "strokeColor": stroke, "strokeWidth": lw,
        "fillStyle": "solid", "roughness": 0, "opacity": 100,
        "roundness": {"type": 3, "value": corner},
    }
    els = [el]
    if label:
        els.append(ex_text(x + w/2, y + h/2, label, font_sz, bold, color, "center", "middle"))
    return els

def ex_text(x, y, text, sz=14, bold=False, color="#000000", ha="center", va="middle"):
    return {
        "id": uid(), "type": "text", "x": x, "y": y,
        "text": text, "fontSize": sz, "fontFamily": 1,
        "textAlign": ha, "verticalAlign": va,
        "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "roughness": 0, "opacity": 100,
        "width": len(text) * sz * 0.6, "height": sz * 1.4,
    }

def ex_arrow(x1, y1, x2, y2, color="#333333", lw=2, label=""):
    el = {
        "id": uid(), "type": "arrow",
        "x": x1, "y": y1,
        "points": [[0, 0], [x2-x1, y2-y1]],
        "strokeColor": color, "strokeWidth": lw,
        "fillStyle": "solid", "roughness": 0, "opacity": 100,
        "startArrowhead": None, "endArrowhead": "arrow",
    }
    els = [el]
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        els.append(ex_text(mx, my - 16, label, 11, False, color))
    return els

SCALE = 28  # matplotlib units → excalidraw pixels

def m2e(x, y, fig_h=FIG_H):
    """Convert matplotlib coords to excalidraw coords (flip Y)."""
    return x * SCALE, (fig_h - y) * SCALE

def build_excalidraw(d, out_path):
    elements = []
    cols_data = d["team_columns"]
    metrics = d["metrics"]
    verdict = d["verdict"]
    m = d["mission"]
    req = d["request"]

    # Title
    tx, ty = m2e(FIG_W/2, FIG_H - 0.25)
    elements.append(ex_text(tx, ty, "Y-OS TEAM TRACE — EXECUTION TRACE", 22, True, "#111111"))
    tx2, ty2 = m2e(FIG_W/2, FIG_H - 0.75)
    elements.append(ex_text(tx2, ty2, f"Mission: {m['id']}  •  {m['date']}  •  {m['title']}", 12, False, "#888888"))

    # Request box
    REQ_X, REQ_Y = 0.25, FIG_H - 1.2
    REQ_W, REQ_H = 2.8, 3.2
    rx, ry = m2e(REQ_X, REQ_Y - REQ_H)
    elements += ex_rect(rx, ry, REQ_W*SCALE, REQ_H*SCALE, bg="#fafaf8", stroke=ROLE_COLORS["human"], lw=2,
                        label=f"{req['user']}\nREQUEST\n\n{req['quote']}", font_sz=11, color=ROLE_COLORS["human"])

    # Team columns
    TEAM_X_START = REQ_X + REQ_W + 0.35
    TEAM_AREA_W  = FIG_W - TEAM_X_START - 5.8
    N_COLS = len(cols_data)
    COL_GAP = 0.18
    COL_W = (TEAM_AREA_W - COL_GAP * (N_COLS-1)) / N_COLS
    COL_H = 7.8
    TEAM_HEADER_Y = FIG_H - 1.1
    COL_TOP = TEAM_HEADER_Y - 0.38
    COL_BODY_Y = COL_TOP - COL_H

    # Team header
    thx, thy = m2e(TEAM_X_START, COL_TOP + 0.38)
    elements += ex_rect(thx, thy, TEAM_AREA_W*SCALE, 0.38*SCALE,
                        bg="#e8eef8", stroke=ROLE_COLORS["human"], lw=1,
                        label="TEAM VIEW — WHO WORKED", font_sz=12, bold=True, color=ROLE_COLORS["human"])

    for i, cd in enumerate(cols_data):
        cx = TEAM_X_START + i * (COL_W + COL_GAP)
        c_ = ROLE_COLORS.get(cd["color_role"], DARK)
        ecx, ecy = m2e(cx, COL_BODY_Y)
        # Card body
        elements += ex_rect(ecx, ecy - COL_H*SCALE, COL_W*SCALE, COL_H*SCALE,
                             bg="#ffffff", stroke=c_, lw=2)
        # Header bar
        hbx, hby = m2e(cx, COL_BODY_Y + COL_H)
        elements += ex_rect(hbx, hby - 0.55*SCALE, COL_W*SCALE, 0.55*SCALE,
                             bg=c_, stroke=c_, lw=0,
                             label=f"{cd['num']}  {cd['title']}", font_sz=9, bold=True, color="#ffffff")
        # Fields summary
        field_text = "\n".join(f"{k}: {v}" for k, v in list(cd["fields"].items())[:6])
        ftx, fty = m2e(cx + COL_W/2, COL_BODY_Y + COL_H - 1.6)
        elements.append(ex_text(ftx, fty, field_text, 8, False, MID, "center", "top"))

    # Handoffs row
    handoffs = d["handoffs"]
    HO_Y = COL_BODY_Y - 0.25
    HO_H = 1.6
    hox, hoy = m2e(TEAM_X_START, HO_Y - HO_H)
    elements += ex_rect(hox, hoy - HO_H*SCALE, TEAM_AREA_W*SCALE, HO_H*SCALE,
                        bg="#fffbf0", stroke=AMBER, lw=1,
                        label="HAND-OFFS (ARTIFACTS PASSED BETWEEN TEAM MEMBERS)",
                        font_sz=10, bold=True, color=AMBER)

    for i, ho in enumerate(handoffs):
        col_i = i + 1
        x1 = TEAM_X_START + col_i * (COL_W + COL_GAP) + COL_W * 0.1
        x2 = TEAM_X_START + (col_i+1) * (COL_W + COL_GAP) - COL_W * 0.1
        y_ho = HO_Y - HO_H/2 - 0.1
        ax1, ay1 = m2e(x1, y_ho)
        ax2, ay2 = m2e(x2, y_ho)
        elements += ex_arrow(ax1, ay1, ax2, ay2, color=AMBER, lw=2, label=ho["name"])

    # Metrics panel
    MET_X = FIG_W - 5.5
    MET_Y = FIG_H - 1.1
    MET_W = 5.25
    MET_H = 18.5
    mx, my = m2e(MET_X, MET_Y - MET_H)
    elements += ex_rect(mx, my - MET_H*SCALE, MET_W*SCALE, MET_H*SCALE,
                        bg="#fafaf8", stroke=BORDER, lw=1)
    # Header
    mhx, mhy = m2e(MET_X, MET_Y)
    elements += ex_rect(mhx, mhy - 0.4*SCALE, MET_W*SCALE, 0.4*SCALE,
                        bg=DARK, stroke=DARK, lw=0,
                        label="RUNTIME METRICS", font_sz=11, bold=True, color="#ffffff")
    met_text = (
        f"Total Time: {metrics['total_time']}\n"
        f"Total Cost: {metrics['total_cost']}\n"
        f"Total Tokens: {metrics['total_tokens']}\n"
        f"Models: {metrics['models_used'].split(chr(10))[0]}\n"
        f"Plugins Skipped: {metrics['plugins_skipped']}"
    )
    mtx, mty = m2e(MET_X + MET_W/2, MET_Y - 1.0)
    elements.append(ex_text(mtx, mty, met_text, 10, False, MID, "center", "top"))

    # Verdict box
    ans = verdict["answer"]
    vd_fg, vd_bg = VERDICT_COLORS.get(ans, (GREEN, "#f0fff4"))
    CMP_Y = HO_Y - HO_H - 0.3 - 3.8 - 0.3
    VD_H = 3.2
    vdx, vdy = m2e(MET_X, CMP_Y - VD_H)
    elements += ex_rect(vdx, vdy - VD_H*SCALE, MET_W*SCALE, VD_H*SCALE,
                        bg=vd_bg, stroke=vd_fg, lw=2)
    vdtx, vdty = m2e(MET_X + MET_W/2, CMP_Y - 0.5)
    elements.append(ex_text(vdtx, vdty, "DID Y-OS CREATE VALUE?", 11, True, vd_fg, "center"))
    vdax, vday = m2e(MET_X + MET_W/2, CMP_Y - 1.0)
    elements.append(ex_text(vdax, vday, ans, 28, True, vd_fg, "center"))
    reasons_text = "\n".join(verdict["reasons"])
    vrx, vry = m2e(MET_X + 0.3, CMP_Y - 1.7)
    elements.append(ex_text(vrx, vry, reasons_text, 9, False, vd_fg, "left", "top"))

    excalidraw_obj = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {
            "viewBackgroundColor": "#ffffff",
            "gridSize": None,
        },
        "files": {}
    }
    with open(out_path, "w") as f:
        json.dump(excalidraw_obj, f, indent=2)


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 render_value_trace.py <schema.json> <output_base>")
        sys.exit(1)
    render(sys.argv[1], sys.argv[2])
