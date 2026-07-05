# YARP Artifact Mapping

> **Version:** v1.0.0
> **Status:** candidate

---

## Artifact Types

| Artifact Type | yOS Concept | Carrier Message | Format |
|---|---|---|---|
| `mp` | Mega Prompt packet | EXECUTE_MP | Markdown + YAML frontmatter |
| `mpr` | Mega Prompt Report | RESULT | Markdown + STATUS BLOCK |
| `context_pack` | Session context | EXECUTE_MP, REQUEST_INFO | JSON or Markdown |
| `oca` | Orchestration Context Artifact | EXECUTE_MP | JSON |
| `kap_pack` | KAP context pack | EXECUTE_MP | JSON |
| `markdown_file` | Human-readable document | RESULT, ERROR | Markdown |
| `json_payload` | Structured data | RESULT | JSON |
| `blob` | Binary file | EXECUTE_MP, RESULT | base64 or file_id |
| `url_pointer` | External reference | any | URL string |
| `bus_packet` | BUS transport packet | EXECUTE_MP | Markdown |
| `schema_file` | JSON Schema | EXECUTE_MP | JSON |

---

## ID Mapping Chain

```
MP (mp_id)
  └── YARP EXECUTE_MP (mp_id field in payload)
        └── task_id (Manus API task, assigned in ACK)
              └── execution (Manus agent run)
                    └── YARP RESULT (correlation_id + mp_id)
                          └── MPR (artifact_type: mpr)
                                └── latest-mpr.json (fixed pointer)
                                      └── latest-mpr.md (human-readable)
```

---

## Artifact Pointer Schema

```json
{
  "artifact_id": "string",
  "artifact_type": "mp|mpr|context_pack|oca|kap_pack|markdown_file|json_payload|blob|url_pointer|bus_packet|schema_file",
  "title": "string",
  "path": "string|null",
  "url": "string|null",
  "file_id": "string|null",
  "size_bytes": "integer|null",
  "checksum_sha256": "string|null",
  "created_at": "ISO8601",
  "created_by": "agent_id"
}
```

---

## MP → YARP EXECUTE_MP Mapping

| MP Field | YARP EXECUTE_MP Field |
|---|---|
| `mp_id` | `payload.mp_id` |
| `mode` | `payload.mp_mode` |
| `title` | `payload.mp_content` (embedded) |
| `canonical_mp_path` | `payload.mp_content` (artifact pointer path) |
| `guardian_required` | `payload.structured_output_schema` (if MPR as JSON) |
| `auto_run_eligible` | `payload.priority` |

---

## MPR → YARP RESULT Mapping

| MPR Field | YARP RESULT Field |
|---|---|
| `mpr_id` | `payload.artifacts[0].artifact_id` |
| `mp_id` | `payload.mp_id` |
| `status` | `payload.status` |
| `commit` | `payload.commit` |
| `canonical_mpr_path` | `payload.mpr_path` |
| `validation.bus` | `payload.validation.bus` |
| `validation.mpm` | `payload.validation.mpm` |

---

## BUS Integration

| BUS Path | YARP Role |
|---|---|
| `inbox/mpm/<packet>.md` | EXECUTE_MP delivery point |
| `workspace/mpm/<packet>.md` | EXECUTE_MP claimed (ACK sent) |
| `outbox/mpm/<result>.md` | RESULT delivery point |
| `archive/mpm/<packet>.md` | FINALIZE complete |
| `04_DOMAINS/mpm/inbox/` | Git fallback EXECUTE_MP |
| `04_DOMAINS/mpm/outbox/` | Git fallback RESULT |
