# BUS Domain Index

> **Source of truth:** `bus_manifest.yaml` and `05_RUNTIME/runtime-registry.json`

## Active Domains

| Domain | Purpose | Git Path | Runtime Path |
|---|---|---|---|
| `general` | Default unclassified domain | `04_DOMAINS/general/` | `$YOS_BUS_RUNTIME_ROOT/{stage}/general/` |
| `mpm` | MPM packet transport | `04_DOMAINS/mpm/` | `$YOS_BUS_RUNTIME_ROOT/{stage}/mpm/` |
| `kap` | Knowledge Assimilation Pipeline | `04_DOMAINS/kap/` | `$YOS_BUS_RUNTIME_ROOT/{stage}/kap/` |
| `casatao` | Casatao project | `04_DOMAINS/casatao/` | `$YOS_BUS_RUNTIME_ROOT/{stage}/casatao/` |
| `kosmos` | Kosmos project | `04_DOMAINS/kosmos/` | `$YOS_BUS_RUNTIME_ROOT/{stage}/kosmos/` |
| `yworld` | yWorld project | `04_DOMAINS/yworld/` | `$YOS_BUS_RUNTIME_ROOT/{stage}/yworld/` |

## Legacy Domain Aliases

| Old Domain | Maps To | Notes |
|---|---|---|
| `yac` | `yworld` | Legacy alias from yos-bus |
| `lakshmi` | TBD | Pending future gate decision |
| `fcs` | archive/legacy | No current canonical domain |

## Runtime Backend Priority

```
1. direct_file   (preferred)
2. manus_cloud   (probe_required)
3. git           (fallback)
4. google_drive  (fallback)
5. nas           (optional)
6. blob_payload  (experimental_payload_only)
```
