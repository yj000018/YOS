# MPM BUS Packet Template

Use this template to create a new MPM BUS packet for transport via BUS `inbox/mpm/`. Replace all `{PLACEHOLDER}` values.

---

```json
{
  "bus_packet_id": "BUS-MPM-{YYYYMMDD}-{MP_ID_SLUG}",
  "domain": "mpm",
  "type": "mpm_packet",
  "status": "inbox",
  "created_by": "{ChatGPT_A_G|other_agent}",
  "created_at": "{ISO8601_TIMESTAMP}",
  "mp_id": "MPM-{YYYYMMDD}-{SLUG}",
  "mode": "{sprint|run|marathon}",
  "risk_flags": [],
  "mpm_payload_kind": "{inline_markdown|path|url|blob_sha}",
  "payload": "{mp_content_or_path}",
  "canonical_mp_path": "01_BACKBONE/MPM/04_QUEUE/ready/MPM-{YYYYMMDD}-{SLUG}.md",
  "expected_mpr_path": "01_BACKBONE/MPM/06_REPORTS/awaiting-review/MPM-{YYYYMMDD}-{SLUG}-REPORT.md",
  "auto_run_eligible": false,
  "claimed_by": null,
  "claimed_at": null
}
```

---

## Field Guide

| Field | Required | Notes |
|---|---|---|
| `mp_id` | yes | MPM packet ID |
| `mode` | yes | sprint/run/marathon |
| `risk_flags` | yes | Empty = auto-run eligible if exactly one ready |
| `mpm_payload_kind` | yes | How MP content is delivered |
| `canonical_mp_path` | no | Git path for MP file |
| `expected_mpr_path` | no | Expected MPR path after execution |
| `auto_run_eligible` | no | Set true only if risk_flags empty and mode safe |

---

## Usage

1. Create this JSON file at `$YOS_BUS_RUNTIME_ROOT/inbox/mpm/BUS-MPM-{YYYYMMDD}-{SLUG}.json`
2. Or commit to `01_BACKBONE/BUS/04_DOMAINS/mpm/inbox/` as Git fallback.
3. Manus will discover and claim it via `MP` command resolution order.
