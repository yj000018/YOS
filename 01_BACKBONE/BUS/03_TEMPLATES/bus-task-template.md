# BUS Task Template

Use this template to create a new BUS task packet. Replace all `{PLACEHOLDER}` values.

---

```json
{
  "bus_packet_id": "BUS-TASK-{YYYYMMDD}-{DOMAIN}-{SLUG}",
  "domain": "{general|mpm|kap|casatao|kosmos|yworld}",
  "type": "task",
  "status": "inbox",
  "created_by": "{agent_name}",
  "created_at": "{ISO8601_TIMESTAMP}",
  "task_title": "{Short human-readable task title}",
  "task_description": "{Full task description and context}",
  "assigned_to": "{target_agent_or_null}",
  "priority": "normal",
  "due_at": null,
  "dependencies": [],
  "output_expected": "{expected_output_path_or_null}",
  "risk_flags": [],
  "claimed_by": null,
  "claimed_at": null
}
```

---

## Field Guide

| Field | Required | Notes |
|---|---|---|
| `bus_packet_id` | yes | Format: BUS-TASK-YYYYMMDD-DOMAIN-SLUG |
| `task_title` | yes | Short, human-readable |
| `task_description` | yes | Full context for the executing agent |
| `assigned_to` | yes | Target agent; null = unassigned |
| `priority` | no | critical/high/normal/low |
| `due_at` | no | ISO 8601 deadline |
| `dependencies` | no | List of bus_packet_ids |
| `output_expected` | no | Expected output path |
