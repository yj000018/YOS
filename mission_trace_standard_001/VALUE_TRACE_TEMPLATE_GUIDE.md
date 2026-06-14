# VALUE TRACE TEMPLATE — Usage Guide

**Standard:** MISSION-TRACE-STANDARD-001  
**Template:** `value_trace_template_clean.excalidraw`

---

## How to invoke

Say: **`/trace-excalidraw [MISSION_ID]`**

Manus will:
1. Read the execution data from the last mission
2. Fill the template zones with real data
3. Generate `.excalidraw` + `.png` + `.svg`
4. Commit to `y-os-doctrine`

---

## Template zones (8 mandatory)

| Zone | Label | Fill with |
| :--- | :--- | :--- |
| Legend | Color categories | Fixed — do not change |
| A | REQUEST | User, exact request, intent, expected output |
| B–F | TEAM FLOW | Role, Worker, Provider, Model, Tools, Input, Output, Artifact, Latency, Cost |
| C | ARTIFACT HANDOFFS | Arrow labels: artifact name, token count, latency, cost |
| D | PLUGINS SKIPPED | List inactive plugins + reason |
| E | RUNTIME METRICS | Aggregated totals |
| F | VALUE PANEL | Artifacts, decisions, knowledge, repos, deliverable |
| G | FINAL VERDICT | YES / NO / AMBER + reason + savings |
| H | WITHOUT vs WITH | Manual steps vs Y-OS steps |

---

## Design rules

- Dark background `#0f172a` — always
- Sparse text — placeholders only, no narrative prose
- No icons, no decorative elements
- Readable when zoomed out to 50%
- Color coding must match the legend row

---

## When to use Excalidraw vs lighter formats

| Format | When |
| :--- | :--- |
| **Mermaid + Canvas** | Default — lightweight daily traces |
| **Excalidraw (this template)** | Important missions, review, external sharing, explicit request |

---

## CSO constraint

Do not build a trace engine or dashboard.  
This template is a static artifact, generated on demand by a lightweight Python script.
