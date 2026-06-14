#!/usr/bin/env python3
"""Renders value_trace_template_preview.png — a visual map of the 8 zones."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

FIG_W, FIG_H, DPI = 26, 18, 150
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
ax.set_xlim(0, FIG_W); ax.set_ylim(0, FIG_H)
ax.set_aspect("equal"); ax.axis("off")
fig.patch.set_facecolor("#0f172a"); ax.set_facecolor("#0f172a")

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
}

def zone(ax, x, y, w, h, title, subtitle, bg, border, text_color="#f8fafc", font_size=9):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                       linewidth=1.5, edgecolor=border, facecolor=bg, zorder=2)
    ax.add_patch(p)
    ax.text(x + w/2, y + h - 0.18, title, ha="center", va="top",
            color=text_color, fontsize=font_size + 2, fontweight="bold", zorder=3)
    if subtitle:
        ax.text(x + w/2, y + h - 0.48, subtitle, ha="center", va="top",
                color=text_color, fontsize=font_size - 1, alpha=0.8, zorder=3,
                style="italic")

def arrow(ax, x1, y1, x2, y2, label=""):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color="#fde047", lw=1.5), zorder=4)
    if label:
        ax.text((x1+x2)/2, (y1+y2)/2 + 0.12, label, ha="center", va="bottom",
                color="#fde047", fontsize=7, zorder=5,
                bbox=dict(boxstyle="round,pad=0.1", facecolor="#0f172a",
                          edgecolor="#fde047", lw=0.8, alpha=0.9))

# Title
ax.text(FIG_W/2, FIG_H - 0.3, "Y-OS VALUE TRACE — TEMPLATE LAYOUT",
        ha="center", va="top", color="#f8fafc", fontsize=16, fontweight="bold")
ax.text(FIG_W/2, FIG_H - 0.7, "MISSION-TRACE-STANDARD-001  |  8 Mandatory Zones",
        ha="center", va="top", color="#94a3b8", fontsize=11, style="italic")

# Legend
legend = [("Human","human"),("Agent","agent"),("LLM","llm"),
          ("Tool","tool"),("Governance","governance"),("Artifact","artifact"),("Skipped","skipped")]
for i, (label, key) in enumerate(legend):
    lx = 0.3 + i * 3.65
    p = FancyBboxPatch((lx, FIG_H-1.35), 3.3, 0.42, boxstyle="round,pad=0.05",
                       linewidth=1, edgecolor=C[key][1], facecolor=C[key][0], zorder=3)
    ax.add_patch(p)
    ax.text(lx+1.65, FIG_H-1.14, label, ha="center", va="center",
            color="#f8fafc", fontsize=9, fontweight="bold", zorder=4)

# Main flow: 7 columns
BOX_TOP = FIG_H - 1.75
BOX_H = 6.2
BOX_W = 3.2
GAP = 0.25
cols = [
    ("A. REQUEST", "User / Request\nIntent / Expected Output", "human"),
    ("B1. ORCHESTRATOR", "Manus\nRouting + Classification", "agent"),
    ("B2. WORKER", "Architect / Researcher\nProvider / Model / Tools", "llm"),
    ("B3. VALIDATOR", "Lakshmi\nConstitution Check", "governance"),
    ("B4. ARCHIVIST", "Registry\nArtifact Lineage", "tool"),
    ("B5. MEMORY", "Git / Notion / Obsidian\nPersistence", "tool"),
    ("DELIVERABLE", "Final Answer\nto Yannick", "artifact"),
]
col_rights = []
for i, (title, subtitle, key) in enumerate(cols):
    bx = 0.25 + i * (BOX_W + GAP)
    by = BOX_TOP - BOX_H
    zone(ax, bx, by, BOX_W, BOX_H, title, subtitle, C[key][0], C[key][1])
    col_rights.append(bx + BOX_W)

# Arrows
handoff_labels = [
    "Request\n0 tokens", "CTX-[ID]\n[X] tokens", "ARTIFACT-[ID]\n[X] tokens",
    "Approved\n0 tokens", "Registered\n0 tokens", "Persisted\n0 tokens"
]
for i in range(len(cols) - 1):
    x1 = col_rights[i]
    x2 = 0.25 + (i+1) * (BOX_W + GAP)
    y_mid = BOX_TOP - BOX_H / 2
    arrow(ax, x1, y_mid, x2, y_mid, handoff_labels[i])

# C. Artifact handoffs label
ax.text(FIG_W/2, BOX_TOP - BOX_H - 0.15,
        "C. ARTIFACT HANDOFFS — Each arrow: artifact name, token count, latency, cost, status",
        ha="center", va="top", color="#fde047", fontsize=8, style="italic")

# D. Plugins skipped
SKIP_Y = BOX_TOP - BOX_H - 0.55
skip_w = 5.8
for i, (name, desc) in enumerate([
    ("D. ODT", "NOT ACTIVATED"), ("D. STRATEGIC INTEL", "NOT ACTIVATED"),
    ("D. SIMULATION", "NOT ACTIVATED"), ("D. OBSERVABILITY", "NOT ACTIVATED")
]):
    sx = 0.25 + i * (skip_w + 0.25)
    zone(ax, sx, SKIP_Y - 1.2, skip_w, 1.1, name, desc, C["skipped"][0], C["skipped"][1], "#9ca3af", 8)

# E. Metrics
METRICS_Y = SKIP_Y - 1.4
zone(ax, 0.25, METRICS_Y - 0.9, FIG_W - 0.5, 0.85,
     "E. RUNTIME METRICS",
     "Total Time  |  Total Cost  |  Total Tokens  |  Models Used  |  Tools Used  |  Artifacts Created  |  Plugins Skipped",
     C["value"][0], C["value"][1], "#f8fafc", 9)

# F. Value Panel
VALUE_Y = METRICS_Y - 1.1
zone(ax, 0.25, VALUE_Y - 1.1, FIG_W - 0.5, 1.0,
     "F. VALUE PANEL",
     "Artifacts Created  |  Decisions Produced  |  Knowledge Added  |  Repos Updated  |  Final Deliverable",
     C["value"][0], C["value"][1], "#f8fafc", 9)

# G. Verdict
VERDICT_Y = VALUE_Y - 1.3
zone(ax, 0.25, VERDICT_Y - 1.3, FIG_W - 0.5, 1.2,
     "G. DID Y-OS CREATE VALUE?  [YES / NO / AMBER]",
     "Explanation  |  Where value was produced  |  Time saved  |  Cost saved",
     C["verdict"][0], C["verdict"][1], "#f0fdf4", 10)

# H. Without / With
COMP_Y = VERDICT_Y - 1.5
half = (FIG_W - 0.75) / 2
zone(ax, 0.25, COMP_Y - 1.2, half, 1.1,
     "H. WITHOUT Y-OS",
     "Manual search / Copy-paste / Ask LLM / Save manually\nNo audit trail / No governance",
     "#1c1917", "#78716c", "#d1d5db", 9)
zone(ax, 0.5 + half, COMP_Y - 1.2, half, 1.1,
     "H. WITH Y-OS",
     "Auto context / Team routing / Governance\nArtifact lineage / Memory update / Final answer",
     C["verdict"][0], C["verdict"][1], "#f0fdf4", 9)

base = "/home/ubuntu/yreg/mission_trace_standard_001/value_trace_template_preview"
plt.tight_layout(pad=0)
plt.savefig(base + ".png", format="png", dpi=DPI, bbox_inches="tight",
            facecolor=fig.get_facecolor())
plt.close()
print(f"Preview PNG: {base}.png")
