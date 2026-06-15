"""
build_native_excalidraw.py
Generates a native Excalidraw JSON that visually matches the reference sketch:
- 9 numbered team columns with rounded boxes
- Colored header bars per role
- Text fields inside each column
- Handoffs row with arrows and labels
- Plugins NOT ACTIVATED panel (left)
- 3 synchronized views (Architecture / Team / Value)
- Runtime Metrics panel (right)
- DID Y-OS CREATE VALUE? verdict box
- WITHOUT vs WITH Y-OS comparison (bottom)

Usage:
    python3 build_native_excalidraw.py <schema.json> <output.excalidraw>
"""
import json, sys, uuid, math

# ─── ID helpers ───────────────────────────────────────────────────────────────
def uid(): return str(uuid.uuid4())[:8]

# ─── PALETTE ──────────────────────────────────────────────────────────────────
ROLE_COLOR = {
    "human":        "#1a4fa0",
    "orchestrator": "#444444",
    "architect":    "#6b3fa0",
    "worker":       "#1a7a6e",
    "validator":    "#c85a00",
    "memory":       "#555555",
    "deliverable":  "#b87800",
    "skipped":      "#888888",
}
ROLE_BG = {
    "human":        "#e8f0fb",
    "orchestrator": "#f0f0f0",
    "architect":    "#f0eafa",
    "worker":       "#e8f5f3",
    "validator":    "#fdf0e8",
    "memory":       "#f0f0f0",
    "deliverable":  "#fdf8e8",
    "skipped":      "#f5f5f5",
}
WHITE   = "#ffffff"
DARK    = "#1e1e1e"
RED_BG  = "#ffeaea"
RED_STR = "#c0392b"
GRN_BG  = "#e8f5e9"
GRN_STR = "#1a6e2e"
AMB_BG  = "#fff8e1"
AMB_STR = "#b87800"
HAND_BG = "#fffde7"
HAND_STR= "#b87800"
METRICS_BG  = "#f8f8f8"
METRICS_STR = "#1e1e1e"
ARCH_BG = "#e8f0fb"
TEAM_BG = "#f3e8ff"
VAL_BG  = "#fff8e1"

# ─── ELEMENT BUILDERS ─────────────────────────────────────────────────────────
def rect(x, y, w, h, bg=WHITE, stroke=DARK, sw=1.5, radius=8, label="", fsize=14,
         bold=False, italic=False, color=DARK, align="left", valign="top",
         roughness=1, opacity=100, zorder=1):
    eid = uid()
    fw = "bold" if bold else "normal"
    fs = "italic" if italic else "normal"
    return {
        "id": eid, "type": "rectangle",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": bg,
        "fillStyle": "solid", "strokeWidth": sw, "strokeStyle": "solid",
        "roughness": roughness, "opacity": opacity,
        "groupIds": [], "frameId": None, "roundness": {"type": 3, "value": radius},
        "seed": int(eid[:4], 16), "version": 1, "versionNonce": 0,
        "isDeleted": False, "boundElements": None, "updated": 0, "link": None, "locked": False,
        "text": label, "fontSize": fsize, "fontFamily": 1,
        "textAlign": align, "verticalAlign": valign,
        "baseline": fsize, "containerId": None, "originalText": label,
        "fontWeight": fw, "fontStyle": fs, "lineHeight": 1.25,
        "strokeColor_text": color,
    }

def text_el(x, y, w, h, label, fsize=13, bold=False, italic=False,
            color=DARK, align="left", valign="top"):
    eid = uid()
    fw = "bold" if bold else "normal"
    fs = "italic" if italic else "normal"
    return {
        "id": eid, "type": "text",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
        "roughness": 1, "opacity": 100,
        "groupIds": [], "frameId": None, "roundness": None,
        "seed": int(eid[:4], 16), "version": 1, "versionNonce": 0,
        "isDeleted": False, "boundElements": None, "updated": 0, "link": None, "locked": False,
        "text": label, "fontSize": fsize, "fontFamily": 1,
        "textAlign": align, "verticalAlign": valign,
        "baseline": fsize, "containerId": None, "originalText": label,
        "fontWeight": fw, "fontStyle": fs, "lineHeight": 1.25,
    }

def arrow_el(x1, y1, x2, y2, label="", color=DARK, sw=1.5):
    eid = uid()
    return {
        "id": eid, "type": "arrow",
        "x": x1, "y": y1,
        "width": abs(x2-x1), "height": abs(y2-y1),
        "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": sw, "strokeStyle": "solid",
        "roughness": 1, "opacity": 100,
        "groupIds": [], "frameId": None, "roundness": {"type": 2},
        "seed": int(eid[:4], 16), "version": 1, "versionNonce": 0,
        "isDeleted": False, "boundElements": None, "updated": 0, "link": None, "locked": False,
        "points": [[0, 0], [x2-x1, y2-y1]],
        "lastCommittedPoint": None, "startBinding": None, "endBinding": None,
        "startArrowhead": None, "endArrowhead": "arrow",
        "text": label, "fontSize": 11, "fontFamily": 1,
        "textAlign": "center", "verticalAlign": "middle",
    }

def circle_el(cx, cy, r, bg, stroke, label="", fsize=18, bold=True, color=WHITE):
    eid = uid()
    fw = "bold" if bold else "normal"
    return {
        "id": eid, "type": "ellipse",
        "x": cx - r, "y": cy - r, "width": r*2, "height": r*2,
        "angle": 0, "strokeColor": stroke, "backgroundColor": bg,
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 1, "opacity": 100,
        "groupIds": [], "frameId": None, "roundness": {"type": 3, "value": r},
        "seed": int(eid[:4], 16), "version": 1, "versionNonce": 0,
        "isDeleted": False, "boundElements": None, "updated": 0, "link": None, "locked": False,
        "text": label, "fontSize": fsize, "fontFamily": 1,
        "textAlign": "center", "verticalAlign": "middle",
        "baseline": fsize, "containerId": None, "originalText": label,
        "fontWeight": fw, "fontStyle": "normal", "lineHeight": 1.25,
        "strokeColor_text": color,
    }

# ─── MAIN BUILDER ─────────────────────────────────────────────────────────────
def build(schema_path, out_path):
    with open(schema_path) as f:
        d = json.load(f)

    m       = d["mission"]
    req     = d["request"]
    cols    = d["team_columns"]
    handoffs= d["handoffs"]
    plugins = d["plugins_skipped"]
    plug_reason = d.get("plugins_skipped_reason", "Core-Only Mode")
    arch    = d["architecture_view"]
    tv      = d["team_view"]
    vv      = d["value_view"]
    metrics = d["metrics"]
    verdict = d["verdict"]
    wo      = d["without_yos"]
    wi      = d["with_yos"]

    els = []

    # ── CANVAS DIMENSIONS ──────────────────────────────────────────────────────
    # Total width: ~4800, height: ~3400
    TOTAL_W = 4800
    TOTAL_H = 3400

    # ── TITLE BAR ─────────────────────────────────────────────────────────────
    els.append(text_el(600, 20, 3200, 50,
        f"Y-OS TEAM TRACE — EXECUTION TRACE",
        fsize=36, bold=True, color=DARK, align="center"))
    els.append(text_el(600, 70, 3200, 30,
        f"Mission: {m['id']}  •  Date: {m['date']}  •  {m['title']}",
        fsize=16, color="#555555", align="center"))
    els.append(text_el(3900, 20, 800, 30,
        f"TRACE ID: {m['trace_id']}",
        fsize=14, bold=True, color="#1a4fa0", align="right"))

    # ── YANNICK REQUEST BOX ───────────────────────────────────────────────────
    els.append(rect(20, 120, 220, 160, bg="#e8f0fb", stroke="#1a4fa0", sw=2, radius=10))
    els.append(text_el(30, 125, 200, 20, f"{req['user']} REQUEST", fsize=13, bold=True, color="#1a4fa0"))
    els.append(circle_el(130, 185, 28, "#1a4fa0", "#1a4fa0", req["user_icon"], fsize=20))
    els.append(text_el(30, 220, 200, 55, f'"{req["quote"]}"', fsize=11, italic=True, color=DARK))

    # ── TEAM VIEW HEADER ──────────────────────────────────────────────────────
    TEAM_X = 260
    TEAM_Y = 110
    TEAM_W = 3620
    TEAM_H = 580
    els.append(rect(TEAM_X, TEAM_Y, TEAM_W, TEAM_H, bg="#f8f8f8", stroke="#333333", sw=1.5, radius=6))
    els.append(text_el(TEAM_X+10, TEAM_Y+8, TEAM_W-20, 24, "TEAM VIEW — WHO WORKED",
        fsize=15, bold=True, color=DARK, align="center"))

    # Arrow from Yannick box to team
    els.append(arrow_el(240, 200, 260, 200, color="#1a4fa0", sw=2))

    # ── TEAM COLUMNS ──────────────────────────────────────────────────────────
    N = len(cols)
    COL_W = (TEAM_W - 20) / N
    COL_H = TEAM_H - 50
    COL_Y = TEAM_Y + 40

    for i, col in enumerate(cols):
        cx = TEAM_X + 10 + i * COL_W
        role = col.get("color_role", "worker")
        rc   = ROLE_COLOR.get(role, DARK)
        rbg  = ROLE_BG.get(role, WHITE)

        # Column outer box
        els.append(rect(cx, COL_Y, COL_W-4, COL_H, bg=WHITE, stroke=rc, sw=2, radius=6))

        # Header bar
        els.append(rect(cx, COL_Y, COL_W-4, 38, bg=rc, stroke=rc, sw=0, radius=6))
        els.append(text_el(cx+4, COL_Y+4, COL_W-12, 30,
            f"{col['num']}. {col['title'].replace(chr(10), ' ')}",
            fsize=12, bold=True, color=WHITE, align="center"))

        # Icon circle
        icon_cx = cx + (COL_W-4)/2
        icon_cy = COL_Y + 70
        els.append(circle_el(icon_cx, icon_cy, 22, rc, rc, col["icon"], fsize=16))

        # Fields text
        fields = col.get("fields", {})
        fy = COL_Y + 100
        for k, v in fields.items():
            label_color = rc if k in ("Role", "Worker", "Provider", "Model") else "#555555"
            bold_k = k in ("Role", "Worker")
            els.append(text_el(cx+6, fy, COL_W-16, 14, k, fsize=10, bold=True, color=label_color))
            fy += 14
            els.append(text_el(cx+6, fy, COL_W-16, 28, str(v), fsize=10, color=DARK))
            fy += 28

        # Arrow to next column
        if i < N - 1:
            ax1 = cx + COL_W - 4
            ax2 = cx + COL_W
            els.append(arrow_el(ax1, COL_Y + COL_H/2, ax2 + 4, COL_Y + COL_H/2, color=rc, sw=1.5))

    # ── PLUGINS NOT ACTIVATED (left panel) ───────────────────────────────────
    PL_X = 20
    PL_Y = TEAM_Y + TEAM_H + 20
    PL_W = 230
    PL_H = 380
    els.append(rect(PL_X, PL_Y, PL_W, PL_H, bg="#fff5f5", stroke=RED_STR, sw=2, radius=8))
    els.append(text_el(PL_X+8, PL_Y+8, PL_W-16, 20, "PLUGINS", fsize=13, bold=True, color=RED_STR))
    els.append(text_el(PL_X+8, PL_Y+26, PL_W-16, 20, "NOT ACTIVATED", fsize=12, bold=True, color=RED_STR))
    els.append(text_el(PL_X+8, PL_Y+46, PL_W-16, 16, "(Core-Only Mode)", fsize=10, italic=True, color="#888888"))

    py = PL_Y + 68
    for p in plugins:
        els.append(rect(PL_X+8, py, PL_W-16, 56, bg=WHITE, stroke="#cccccc", sw=1, radius=4))
        els.append(text_el(PL_X+14, py+4, PL_W-28, 16, "✕ " + p["name"].replace("\n", " "), fsize=11, bold=True, color=RED_STR))
        if p.get("desc"):
            els.append(text_el(PL_X+14, py+20, PL_W-28, 28, p["desc"].replace("\n", " "), fsize=9, color="#888888"))
        els.append(text_el(PL_X+14, py+38, PL_W-28, 14, "✕ SKIPPED", fsize=9, bold=True, color=RED_STR))
        py += 64

    els.append(text_el(PL_X+8, py+4, PL_W-16, 40,
        "Reason:\n" + plug_reason.replace("\n", " / "), fsize=9, italic=True, color="#888888"))

    # ── HANDOFFS ROW ──────────────────────────────────────────────────────────
    HO_Y = TEAM_Y + TEAM_H + 20
    HO_X = 260
    HO_W = TEAM_W
    HO_H = 80
    els.append(rect(HO_X, HO_Y, HO_W, HO_H, bg=HAND_BG, stroke=HAND_STR, sw=1.5, radius=6))
    els.append(text_el(HO_X+10, HO_Y+6, HO_W-20, 18,
        "HAND-OFFS  (ARTIFACTS PASSED BETWEEN TEAM MEMBERS)",
        fsize=12, bold=True, color=HAND_STR, align="center"))

    ho_slot_w = HO_W / (len(handoffs) + 1)
    for i, ho in enumerate(handoffs):
        hx = HO_X + (i + 0.5) * ho_slot_w
        # Arrow
        els.append(arrow_el(hx, HO_Y + 28, hx + ho_slot_w * 0.8, HO_Y + 28, color=HAND_STR, sw=1.5))
        # Label box
        els.append(rect(hx - 60, HO_Y + 32, 120, 40, bg=WHITE, stroke=HAND_STR, sw=1, radius=4))
        els.append(text_el(hx - 56, HO_Y + 34, 112, 16, ho["name"], fsize=10, bold=True, color=HAND_STR, align="center"))
        els.append(text_el(hx - 56, HO_Y + 50, 112, 18, ho["detail"].replace("\n", " · "), fsize=9, color="#888888", align="center"))

    # ── 3 VIEWS ROW ───────────────────────────────────────────────────────────
    VIEWS_Y = HO_Y + HO_H + 20
    VIEWS_H = 220
    V1_X = 260; V1_W = 900
    V2_X = V1_X + V1_W + 10; V2_W = 1200
    V3_X = V2_X + V2_W + 10; V3_W = TEAM_W - V1_W - V2_W - 20

    # View 1 — Architecture
    els.append(rect(V1_X, VIEWS_Y, V1_W, VIEWS_H, bg=ARCH_BG, stroke="#1a4fa0", sw=1.5, radius=6))
    els.append(text_el(V1_X+8, VIEWS_Y+8, V1_W-16, 20, "View 1 — ARCHITECTURE VIEW (Validation)", fsize=13, bold=True, color="#1a4fa0"))
    step_w = (V1_W - 20) / len(arch["steps"])
    for j, s in enumerate(arch["steps"]):
        sx = V1_X + 10 + j * step_w
        sc = ROLE_COLOR.get(s["color_role"], DARK)
        sbg = ROLE_BG.get(s["color_role"], WHITE)
        els.append(rect(sx, VIEWS_Y+34, step_w-4, 44, bg=sc, stroke=sc, sw=0, radius=4))
        els.append(text_el(sx+2, VIEWS_Y+38, step_w-8, 18, s["label"], fsize=10, bold=True, color=WHITE, align="center"))
        els.append(text_el(sx+2, VIEWS_Y+56, step_w-8, 16, s["sub"], fsize=9, color=WHITE, align="center"))
        if j < len(arch["steps"]) - 1:
            els.append(arrow_el(sx + step_w - 4, VIEWS_Y + 56, sx + step_w, VIEWS_Y + 56, color=DARK, sw=1))
    els.append(text_el(V1_X+8, VIEWS_Y+88, V1_W-16, 18, arch["summary"], fsize=11, bold=True, color=DARK, align="center"))
    els.append(text_el(V1_X+8, VIEWS_Y+106, V1_W-16, 18, arch["plugins_note"], fsize=11, bold=True, color=RED_STR, align="center"))
    els.append(text_el(V1_X+8, VIEWS_Y+126, V1_W-16, 18, arch.get("task_type_note",""), fsize=10, italic=True, color=GRN_STR, align="center"))

    # View 2 — Team
    els.append(rect(V2_X, VIEWS_Y, V2_W, VIEWS_H, bg=TEAM_BG, stroke="#6b3fa0", sw=1.5, radius=6))
    els.append(text_el(V2_X+8, VIEWS_Y+8, V2_W-16, 20, "View 2 — TEAM VIEW (Who Worked)", fsize=13, bold=True, color="#6b3fa0", align="center"))
    icons = tv["icons"]
    icon_slot = V2_W / len(icons)
    for j, ic in enumerate(icons):
        ix = V2_X + (j + 0.5) * icon_slot
        ic_c = ROLE_COLOR.get(ic["color_role"], DARK)
        els.append(circle_el(ix, VIEWS_Y + 70, 22, ic_c, ic_c, ic["sym"], fsize=14))
        els.append(text_el(ix - 30, VIEWS_Y + 96, 60, 16, ic["name"], fsize=9, color=DARK, align="center"))
    els.append(text_el(V2_X+8, VIEWS_Y+122, V2_W-16, 18, tv["tagline"], fsize=11, bold=True, color=DARK, align="center"))
    els.append(text_el(V2_X+8, VIEWS_Y+140, V2_W-16, 18, tv["tagline2"], fsize=10, italic=True, color="#555555", align="center"))

    # View 3 — Value
    els.append(rect(V3_X, VIEWS_Y, V3_W, VIEWS_H, bg=VAL_BG, stroke=AMB_STR, sw=1.5, radius=6))
    els.append(text_el(V3_X+8, VIEWS_Y+8, V3_W-16, 20, "View 3 — VALUE VIEW (What Was Created)", fsize=13, bold=True, color=AMB_STR, align="center"))
    kpis = vv["kpis"]
    kpi_w = (V3_W - 16) / len(kpis)
    for j, kpi in enumerate(kpis):
        kx = V3_X + 8 + j * kpi_w
        els.append(rect(kx, VIEWS_Y+34, kpi_w-4, 70, bg=WHITE, stroke=AMB_STR, sw=1, radius=4))
        els.append(text_el(kx+2, VIEWS_Y+40, kpi_w-8, 28, kpi["num"], fsize=22, bold=True, color=AMB_STR, align="center"))
        els.append(text_el(kx+2, VIEWS_Y+68, kpi_w-8, 28, kpi["label"].replace("\n", " "), fsize=9, color=DARK, align="center"))
    els.append(text_el(V3_X+8, VIEWS_Y+114, V3_W-16, 18, vv["summary"], fsize=11, bold=True, color=AMB_STR, align="center"))
    els.append(text_el(V3_X+8, VIEWS_Y+132, V3_W-16, 18, vv.get("note",""), fsize=10, italic=True, color="#555555", align="center"))

    # ── RUNTIME METRICS PANEL (right) ─────────────────────────────────────────
    MET_X = TEAM_X + TEAM_W + 20
    MET_Y = TEAM_Y
    MET_W = 300
    MET_H = VIEWS_Y + VIEWS_H - TEAM_Y
    els.append(rect(MET_X, MET_Y, MET_W, MET_H, bg=METRICS_BG, stroke="#333333", sw=1.5, radius=8))
    # Header bar
    els.append(rect(MET_X, MET_Y, MET_W, 36, bg="#333333", stroke="#333333", sw=0, radius=8))
    els.append(text_el(MET_X+10, MET_Y+8, MET_W-20, 22, "RUNTIME METRICS", fsize=14, bold=True, color=WHITE, align="center"))

    met_items = [
        ("⏱", "Total Time",    metrics["total_time"]),
        ("$", "Total Cost",    metrics["total_cost"]),
        ("#", "Total Tokens",  metrics["total_tokens"]),
        ("🤖","Models Used",   metrics["models_used"].replace("\n", ", ")),
        ("🔧","Tools Used",    metrics["tools_used"].replace("\n", ", ")),
        ("📦","Artifacts",     metrics["artifacts_created"].replace("\n", " / ")),
        ("✕", "Plugins Skipped", metrics["plugins_skipped"]),
    ]
    my = MET_Y + 46
    for icon, label, val in met_items:
        els.append(text_el(MET_X+10, my, 24, 18, icon, fsize=13, color=AMB_STR))
        els.append(text_el(MET_X+36, my, MET_W-46, 14, label, fsize=10, bold=True, color="#888888"))
        my += 15
        els.append(text_el(MET_X+36, my, MET_W-46, 20, val, fsize=12, bold=True, color=DARK))
        my += 26

    # ── WITHOUT vs WITH Y-OS ──────────────────────────────────────────────────
    COMP_Y = VIEWS_Y + VIEWS_H + 20
    COMP_H = 180
    HALF_W = (TEAM_W - 10) / 2

    # WITHOUT
    els.append(rect(HO_X, COMP_Y, HALF_W, COMP_H, bg=RED_BG, stroke=RED_STR, sw=2, radius=8))
    els.append(text_el(HO_X+10, COMP_Y+8, HALF_W-20, 20, "WITHOUT Y-OS  (MANUAL PROCESS)", fsize=13, bold=True, color=RED_STR))
    wo_slot = (HALF_W - 20) / len(wo["steps"])
    for j, s in enumerate(wo["steps"]):
        sx = HO_X + 10 + j * wo_slot
        els.append(rect(sx, COMP_Y+34, wo_slot-4, 44, bg=WHITE, stroke=RED_STR, sw=1, radius=4))
        els.append(text_el(sx+2, COMP_Y+44, wo_slot-8, 24, s, fsize=9, color=RED_STR, align="center"))
        if j < len(wo["steps"]) - 1:
            els.append(arrow_el(sx + wo_slot - 4, COMP_Y + 56, sx + wo_slot, COMP_Y + 56, color=RED_STR, sw=1))
    els.append(rect(HO_X + HALF_W/2 - 80, COMP_Y+88, 160, 36, bg=RED_STR, stroke=RED_STR, sw=0, radius=6))
    els.append(text_el(HO_X + HALF_W/2 - 76, COMP_Y+96, 152, 20,
        wo["time_estimate"], fsize=14, bold=True, color=WHITE, align="center"))
    els.append(text_el(HO_X+10, COMP_Y+134, HALF_W-20, 18, wo["note"], fsize=10, italic=True, color=RED_STR, align="center"))

    # VS label
    els.append(text_el(HO_X + HALF_W - 20, COMP_Y + COMP_H/2 - 15, 40, 30, "VS", fsize=18, bold=True, color=DARK, align="center"))

    # WITH
    WI_X = HO_X + HALF_W + 10
    els.append(rect(WI_X, COMP_Y, HALF_W, COMP_H, bg=GRN_BG, stroke=GRN_STR, sw=2, radius=8))
    els.append(text_el(WI_X+10, COMP_Y+8, HALF_W-20, 20, "WITH Y-OS  (AUTOMATED WITH GOVERNANCE)", fsize=13, bold=True, color=GRN_STR))
    wi_slot = (HALF_W - 20) / len(wi["steps"])
    for j, s in enumerate(wi["steps"]):
        sx = WI_X + 10 + j * wi_slot
        els.append(circle_el(sx + wi_slot/2, COMP_Y + 56, 18, GRN_STR, GRN_STR, str(j+1), fsize=11))
        els.append(text_el(sx+2, COMP_Y+78, wi_slot-4, 24, s, fsize=8, color=GRN_STR, align="center"))
        if j < len(wi["steps"]) - 1:
            els.append(arrow_el(sx + wi_slot - 4, COMP_Y + 56, sx + wi_slot, COMP_Y + 56, color=GRN_STR, sw=1))
    els.append(rect(WI_X + HALF_W/2 - 80, COMP_Y+100, 160, 32, bg=GRN_STR, stroke=GRN_STR, sw=0, radius=6))
    els.append(text_el(WI_X + HALF_W/2 - 76, COMP_Y+108, 152, 18,
        wi["time_estimate"], fsize=14, bold=True, color=WHITE, align="center"))
    els.append(text_el(WI_X+10, COMP_Y+140, HALF_W-20, 18, wi["note"], fsize=9, italic=True, color=GRN_STR, align="center"))

    # ── VERDICT BOX (bottom right) ────────────────────────────────────────────
    ans = verdict["answer"]
    v_stroke, v_bg = (GRN_STR, GRN_BG) if ans == "YES" else (RED_STR, RED_BG) if ans == "NO" else (AMB_STR, AMB_BG)
    VERD_X = MET_X
    VERD_Y = COMP_Y
    VERD_W = MET_W
    VERD_H = COMP_H
    els.append(rect(VERD_X, VERD_Y, VERD_W, VERD_H, bg=v_bg, stroke=v_stroke, sw=2, radius=8))
    els.append(text_el(VERD_X+8, VERD_Y+8, VERD_W-16, 20, "DID Y-OS CREATE VALUE?", fsize=12, bold=True, color=v_stroke, align="center"))
    els.append(rect(VERD_X+20, VERD_Y+34, VERD_W-40, 44, bg=v_stroke, stroke=v_stroke, sw=0, radius=6))
    els.append(text_el(VERD_X+20, VERD_Y+44, VERD_W-40, 24, ans, fsize=22, bold=True, color=WHITE, align="center"))
    ry = VERD_Y + 86
    for reason in verdict.get("reasons", []):
        els.append(text_el(VERD_X+10, ry, VERD_W-20, 16, reason, fsize=9, color=v_stroke))
        ry += 16

    # ── ASSEMBLE EXCALIDRAW ───────────────────────────────────────────────────
    # Clean up elements: remove internal helper keys not in Excalidraw spec
    clean_els = []
    for e in els:
        # For text-bearing rectangles, split into rect + text element
        if e["type"] == "rectangle" and e.get("text"):
            label = e.pop("text", "")
            fsize = e.pop("fontSize", 13)
            ff    = e.pop("fontFamily", 1)
            ta    = e.pop("textAlign", "left")
            va    = e.pop("verticalAlign", "top")
            bl    = e.pop("baseline", fsize)
            ci    = e.pop("containerId", None)
            ot    = e.pop("originalText", label)
            fw    = e.pop("fontWeight", "normal")
            fs    = e.pop("fontStyle", "normal")
            lh    = e.pop("lineHeight", 1.25)
            tc    = e.pop("strokeColor_text", DARK)
            e.pop("strokeColor_text", None)
            clean_els.append(e)
            if label:
                tid = uid()
                clean_els.append({
                    "id": tid, "type": "text",
                    "x": e["x"] + 6, "y": e["y"] + 6,
                    "width": e["width"] - 12, "height": e["height"] - 12,
                    "angle": 0, "strokeColor": tc, "backgroundColor": "transparent",
                    "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
                    "roughness": 1, "opacity": 100,
                    "groupIds": [], "frameId": None, "roundness": None,
                    "seed": int(tid[:4], 16), "version": 1, "versionNonce": 0,
                    "isDeleted": False, "boundElements": None, "updated": 0,
                    "link": None, "locked": False,
                    "text": label, "fontSize": fsize, "fontFamily": ff,
                    "textAlign": ta, "verticalAlign": va,
                    "baseline": bl, "containerId": None, "originalText": ot,
                    "fontWeight": fw, "fontStyle": fs, "lineHeight": lh,
                })
        elif e["type"] == "ellipse" and e.get("text"):
            label = e.pop("text", "")
            fsize = e.pop("fontSize", 16)
            ff    = e.pop("fontFamily", 1)
            ta    = e.pop("textAlign", "center")
            va    = e.pop("verticalAlign", "middle")
            bl    = e.pop("baseline", fsize)
            ci    = e.pop("containerId", None)
            ot    = e.pop("originalText", label)
            fw    = e.pop("fontWeight", "bold")
            fs    = e.pop("fontStyle", "normal")
            lh    = e.pop("lineHeight", 1.25)
            tc    = e.pop("strokeColor_text", WHITE)
            e.pop("strokeColor_text", None)
            clean_els.append(e)
            if label:
                tid = uid()
                clean_els.append({
                    "id": tid, "type": "text",
                    "x": e["x"] + 4, "y": e["y"] + e["height"]/2 - fsize*0.7,
                    "width": e["width"] - 8, "height": fsize * 1.4,
                    "angle": 0, "strokeColor": tc, "backgroundColor": "transparent",
                    "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
                    "roughness": 1, "opacity": 100,
                    "groupIds": [], "frameId": None, "roundness": None,
                    "seed": int(tid[:4], 16), "version": 1, "versionNonce": 0,
                    "isDeleted": False, "boundElements": None, "updated": 0,
                    "link": None, "locked": False,
                    "text": label, "fontSize": fsize, "fontFamily": ff,
                    "textAlign": ta, "verticalAlign": va,
                    "baseline": bl, "containerId": None, "originalText": ot,
                    "fontWeight": fw, "fontStyle": fs, "lineHeight": lh,
                })
        else:
            # Remove helper keys
            for k in ["text", "fontSize", "fontFamily", "textAlign", "verticalAlign",
                      "baseline", "containerId", "originalText", "fontWeight",
                      "fontStyle", "lineHeight", "strokeColor_text"]:
                e.pop(k, None)
            clean_els.append(e)

    doc = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": clean_els,
        "appState": {
            "gridSize": None,
            "viewBackgroundColor": "#ffffff",
            "zoom": {"value": 0.5},
            "scrollX": 0, "scrollY": 0,
        },
        "files": {}
    }

    with open(out_path, "w") as f:
        json.dump(doc, f, indent=2)
    print(f"Excalidraw: {out_path}  ({len(clean_els)} elements)")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 build_native_excalidraw.py <schema.json> <output.excalidraw>")
        sys.exit(1)
    build(sys.argv[1], sys.argv[2])
