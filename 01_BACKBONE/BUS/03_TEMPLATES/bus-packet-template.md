# BUS Packet Template

Use this template to create a new BUS packet. Replace all `{PLACEHOLDER}` values.

---

```json
{
  "bus_packet_id": "BUS-{YYYYMMDD}-{DOMAIN}-{SLUG}",
  "domain": "{general|mpm|kap|casatao|kosmos|yworld}",
  "type": "{task|artifact|decision|mpm_packet|mpr_pointer|event}",
  "status": "inbox",
  "created_by": "{agent_name}",
  "created_at": "{ISO8601_TIMESTAMP}",
  "claimed_by": null,
  "claimed_at": null,
  "payload_kind": "{inline|path|url|blob_sha|external_pointer}",
  "payload": "{content_or_pointer}",
  "risk_flags": [],
  "canonicalization_target": null
}
```

---

## Field Guide

| Field | Required | Notes |
|---|---|---|
| `bus_packet_id` | yes | Format: BUS-YYYYMMDD-DOMAIN-SLUG |
| `domain` | yes | One of the registered BUS domains |
| `type` | yes | Packet type |
| `status` | yes | Start with `inbox` |
| `created_by` | yes | Agent or system name |
| `created_at` | yes | ISO 8601 UTC timestamp |
| `claimed_by` | no | Set when claimed |
| `claimed_at` | no | Set when claimed |
| `payload_kind` | yes | How payload is delivered |
| `payload` | yes | Content or pointer |
| `risk_flags` | no | Empty array if no risk |
| `canonicalization_target` | no | Git path for durable storage |
