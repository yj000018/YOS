# Open Loop Engine

**Owner:** Chief Architect (Brahma)  
**Status:** Accepted  
**Date:** 2026-06-13  

## 1. Rule Definitions

The engine evaluates every artifact and every mission against these rules.

### Lineage Rules
*   **L-01 (Missing Parent):** `parent_id` is empty AND `Artifact Type` != "Strategy Brief". (P1, Producer)
*   **L-02 (Missing Child):** `status` == "Consumed" AND `child_ids` is empty AND `Artifact Type` not in terminal types (Learning Report, CEO Briefing). (P1, Consumer)
*   **L-03 (Orphan):** `mission_id` is empty. (P1, Producer)

### Velocity Rules
*   **V-01 (Stalled Review):** `status` == "Ready For Review" AND `updated_date` > 48h ago. (P2, Review Owner)
*   **V-02 (Stalled Execution):** `status` == "Accepted" AND `child_ids` is empty AND `updated_date` > 72h ago. (P2, Consumer)
*   **V-03 (Abandoned Draft):** `status` == "Draft" AND `updated_date` > 7 days ago. (P3, Producer)
*   **V-04 (Stalled Rework):** `status` == "Rejected" AND `updated_date` > 48h ago. (P2, Producer)

### Mission Rules
*   **M-01 (Blocked Mission):** `Mission Status` == "Blocked". (P1, CEO/Ganesha)
*   **M-02 (Missing Learning):** `Mission Status` == "Completed" AND no "Learning Report" artifact exists for this mission. (P2, Saraswati)

## 2. Execution

The engine runs *after* the Mission Graph Engine has grouped artifacts. It returns a flat list of `OpenLoop` objects that are appended to the `dashboard_state.json` and `open_loops.json`.
