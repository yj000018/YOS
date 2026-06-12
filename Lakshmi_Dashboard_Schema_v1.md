# Dashboard Schema v1

**Owner:** Chief Architect (Brahma)  
**Status:** Accepted  
**Date:** 2026-06-13  

## JSON Output Schema

The runtime will output `lakshmi_dashboard_state.json` matching this schema.

```json
{
  "timestamp": "ISO-8601",
  "metrics": {
    "total_missions": 0,
    "active_missions": 0,
    "blocked_missions": 0,
    "completed_missions": 0,
    "total_artifacts": 0,
    "artifacts_in_draft": 0,
    "artifacts_in_review": 0
  },
  "missions": [
    {
      "id": "string",
      "name": "string",
      "status": "string",
      "health": "Green|Yellow|Red",
      "current_phase": "string",
      "open_loop_count": 0
    }
  ],
  "open_loops": [
    {
      "id": "string",
      "mission_id": "string",
      "artifact_id": "string",
      "rule_id": "string",
      "severity": "P1|P2|P3",
      "assignee": "string",
      "description": "string"
    }
  ],
  "ceo_action_queue": [
    {
      "type": "Decision|Action",
      "description": "string",
      "artifact_id": "string"
    }
  ]
}
```
