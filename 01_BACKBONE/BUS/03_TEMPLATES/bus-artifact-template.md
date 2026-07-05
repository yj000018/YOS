# BUS Artifact Template

Use this template to create a new BUS artifact packet. Replace all `{PLACEHOLDER}` values.

---

```json
{
  "bus_packet_id": "BUS-ART-{YYYYMMDD}-{DOMAIN}-{SLUG}",
  "domain": "{general|mpm|kap|casatao|kosmos|yworld}",
  "type": "artifact",
  "status": "outbox",
  "created_by": "{agent_name}",
  "created_at": "{ISO8601_TIMESTAMP}",
  "artifact_title": "{Human-readable artifact title}",
  "artifact_kind": "{report|document|code|data|image|audio|video|pointer|other}",
  "payload_kind": "{inline|path|url|blob_sha|external_pointer}",
  "payload": "{content_or_pointer}",
  "source_task_id": "{bus_task_id_or_null}",
  "canonicalization_target": "{yos_git_path_or_null}",
  "risk_flags": []
}
```

---

## Field Guide

| Field | Required | Notes |
|---|---|---|
| `artifact_title` | yes | Human-readable |
| `artifact_kind` | yes | Type of artifact |
| `payload_kind` | yes | How payload is delivered |
| `payload` | yes | Content or pointer |
| `source_task_id` | no | BUS task that produced this |
| `canonicalization_target` | no | Git path for durable storage |
