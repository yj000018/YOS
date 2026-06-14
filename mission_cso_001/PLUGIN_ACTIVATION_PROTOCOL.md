# Plugin Activation Protocol — Y-OS

**Authority:** ADR-SIMP-002  
**Default state:** ALL PLUGINS INACTIVE  
**Activation:** Explicit request by Yannick only

---

## Activation Request Form

Copy and fill this form before activating any plugin.

```
PLUGIN ACTIVATION REQUEST
==========================
Date: YYYY-MM-DD
Plugin: [P1 ODT / P2 Strategic / P3 Simulation / P4 Observability]
Requested by: Yannick

1. WHY IS THIS PLUGIN NEEDED NOW?
   (Specific decision or question that requires it)
   → 

2. WHICH DECISION REQUIRES IT?
   (Name the decision — not "it would be useful")
   → 

3. COULD THE CORE ALONE ANSWER THIS?
   (Honest answer — if yes, do not activate)
   → YES / NO
   If NO, explain why:
   → 

4. EXPECTED VALUE
   (What specific output will this plugin produce?)
   → 

5. TIME BUDGET
   (How long should this plugin run before returning to core-only?)
   → 

CSO APPROVAL: ☐ APPROVED / ☐ REJECTED
Reason if rejected:
```

---

## Plugin Activation Log

| Date | Plugin | Decision requiring it | Value delivered (1–5) | Core sufficient? | Duration |
|---|---|---|---|---|---|
| | | | | | |

---

## Plugin Descriptions

### P1 — Organizational Digital Twin
**Activate when:** Monthly organizational review, architecture audit, onboarding a new collaborator.  
**Do NOT activate for:** Daily tasks, single-session questions, curiosity.  
**Expected output:** Full organizational state snapshot, evolution timeline.  
**Deactivate after:** Review session complete.

### P2 — Strategic Intelligence
**Activate when:** Quarterly planning, "what should Y-OS do next?", before a major mission decision.  
**Do NOT activate for:** Single task execution, routine work.  
**Expected output:** Prioritized recommendation list, next mission proposals.  
**Deactivate after:** Planning session complete.

### P3 — Simulation / Time Machine
**Activate when:** Major irreversible decision (architecture change, provider switch, mission sequence change).  
**Do NOT activate for:** Routine decisions, curiosity, "what if" without a real decision pending.  
**Expected output:** Scenario comparison, impact propagation, counterfactual analysis.  
**Deactivate after:** Decision made.

### P4 — Advanced Observability
**Activate when:** Weekly health check, performance degradation suspected, Obsidian navigation session.  
**Do NOT activate for:** Every session (overhead > value at that frequency).  
**Expected output:** EIS score, health dashboard, governance compliance.  
**Deactivate after:** Review complete.

---

## Activation Frequency Targets

| Plugin | Target frequency | Maximum frequency |
|---|---|---|
| P1 ODT | Monthly | Monthly |
| P2 Strategic | Quarterly | Monthly |
| P3 Simulation | Per major decision | Weekly |
| P4 Observability | Weekly | Daily |

**If a plugin is being activated more frequently than its target → it should be promoted to core (CSO review required).**
