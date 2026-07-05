# YOS BUS — MPM Entry Packet Template

**Usage:** Use this template when creating a BUS packet that wraps an MPM packet for first-mile transport.

---

```yaml
---
bus_packet_id: BUS-MPM-{YYYYMMDD}-{SHORT_ID}
domain: mpm
type: mpm_entry_packet
status: inbox
created_by: {creator}
created_at: "{ISO8601}"
payload_kind: inline
risk_flags: []
entry_backend: {direct_file|git|manual_upload|...}
mp_id: {MPM-ID}
---

# BUS MPM Entry Packet — {MP_TITLE}

## Payload

{paste MP content here or reference external file}

---

## Entry Metadata

- **Entry backend:** {backend}
- **Target domain:** mpm
- **Target inbox:** $YOS_BUS_RUNTIME_ROOT/inbox/mpm/ or Git fallback
- **Created at:** {ISO8601}
```

---

## Notes

- This template is for BUS-wrapped MPM packets
- For direct MP files, use `bus.py ingest --domain mpm --file <mp_file>` directly
- Do not commit runtime entry packets to Git
