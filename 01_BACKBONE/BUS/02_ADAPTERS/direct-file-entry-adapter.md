# YOS BUS — Direct File Entry Adapter

**Status:** validated_local_runtime
**Backend ID:** direct_file
**Versioned:** no
**Transport commit required:** no

---

## Role

Fastest local/runtime entry backend. Places packets directly into `$YOS_BUS_RUNTIME_ROOT/inbox/domain/`.

**Validated in:** MPM-20260705-YOS-BUS-DIRECT-FILE-RUNTIME-PROBE-GATE
**Claim latency:** ~43ms

---

## Requirements

```bash
export YOS_BUS_RUNTIME_ROOT=/tmp/yos-bus-runtime   # or persistent path
```

Runtime must be initialized:
```bash
bus.py init-runtime --root "$YOS_BUS_RUNTIME_ROOT"
```

---

## Write Path

```
$YOS_BUS_RUNTIME_ROOT/inbox/{domain}/{packet_filename}
```

---

## bus.py ingest behavior (direct_file)

```bash
bus.py ingest --domain mpm --file /path/to/packet.md
# -> copies to $YOS_BUS_RUNTIME_ROOT/inbox/mpm/packet.md
```

---

## Persistence Note

`/tmp/yos-bus-runtime` is ephemeral in the Manus sandbox.
For cross-session persistence use: `/home/ubuntu/yos-bus-runtime`

See: `06_INDEXES/direct-file-runtime-probe-latest.json`
