# VALUE TRACE TEMPLATE — Guide v2.0

**Pipeline:** `value_trace_schema.json` → `render_value_trace.py` → `.png` + `.svg` + `.excalidraw`

---

## How to Generate a Mission Trace in 5 Steps

**Step 1 — Copy the schema**

```bash
cp value_trace_schema.json my_mission_schema.json
```

**Step 2 — Edit only the mission data**

Open `my_mission_schema.json` and update:

| Section | What to change |
| :--- | :--- |
| `mission` | `id`, `title`, `date`, `trace_id`, `type` |
| `request` | `quote` — the user's actual request |
| `team_columns` | One object per team member (role, worker, fields) |
| `handoffs` | Artifact names + token counts + latency per transfer |
| `plugins_skipped` | Plugins that were NOT activated |
| `architecture_view` | Steps summary + task type note |
| `team_view` | Icons + taglines |
| `value_view` | KPI numbers + summary |
| `metrics` | Total time, cost, tokens, tools, artifacts |
| `verdict` | `answer` (YES / NO / AMBER) + `reasons` list |
| `without_yos` | Manual process steps + time estimate |
| `with_yos` | Automated steps + time estimate |

**Step 3 — Run the renderer**

```bash
python3 render_value_trace.py my_mission_schema.json ./output/my_mission
```

**Step 4 — Verify the output**

Three files are produced:
- `my_mission.png` — printable A4-compatible, 3800px wide
- `my_mission.svg` — vector, zoomable
- `my_mission.excalidraw` — importable at excalidraw.com or Obsidian

**Step 5 — Commit and deliver**

```bash
cd /home/ubuntu/yreg
git add mission_[ID]/
git commit -m "TRACE: [MISSION_ID] — team trace"
git push origin master:y-os-doctrine
```

---

## Color Coding

| Role | Color | Hex |
| :--- | :--- | :--- |
| Human (Yannick) | Blue | `#1a4fa0` |
| Orchestrator | Mid-grey | `#444444` |
| Architect | Purple | `#6b3fa0` |
| Worker (Researcher/Builder/Writer) | Teal | `#1a7a6e` |
| Validator (Lakshmi) | Orange | `#c85a00` |
| Memory / Git | Mid-grey | `#444444` |
| Deliverable | Amber | `#b87800` |
| Verdict YES | Green | `#1a6e2e` |
| Verdict NO | Red | `#c0392b` |
| Verdict AMBER | Amber | `#b87800` |
| Plugins skipped | Red border | `#c0392b` |

---

## Fixed Layout Zones (do not modify)

| Zone | Content |
| :--- | :--- |
| Top | Title, mission ID, date, trace ID |
| Left | Yannick request box |
| Center | Team columns (N columns, auto-sized) |
| Below columns | Artifact handoffs row |
| Left below | Plugins NOT ACTIVATED panel |
| Bottom center | 3 synchronized views (Architecture / Team / Value) |
| Bottom full | WITHOUT Y-OS vs WITH Y-OS comparison |
| Right top | Runtime Metrics panel |
| Right bottom | DID Y-OS CREATE VALUE? verdict |

---

## Verdict Logic

| Answer | When to use |
| :--- | :--- |
| `YES` | Real work delivered, value created, external project |
| `NO` | Pure self-analysis, no deliverable, no external value |
| `AMBER` | Self-referential input → actionable output (valid use) |

---

## CSO Constraint

> No new runtime modules. No dashboard. No live system.
> This is a static artifact generated on demand from a JSON file.
> One JSON → one trace. Reusable across all missions.
