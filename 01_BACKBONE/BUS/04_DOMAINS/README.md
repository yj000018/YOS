# BUS Domains

BUS domains provide namespace isolation for inter-agent message routing. Each domain has its own inbox/workspace/outbox/archive lifecycle.

## Registered Domains

| Domain | Purpose | Status |
|---|---|---|
| `general` | Default domain for unclassified BUS messages | active |
| `mpm` | MPM packet transport — Mega Prompt Manager stream | active |
| `kap` | Knowledge Assimilation Pipeline domain | active |
| `casatao` | Casatao project domain | active |
| `kosmos` | Kosmos project domain | active |
| `yworld` | yWorld project domain | active |

## Legacy Domain Mapping

| Old Domain (yos-bus) | New Domain | Notes |
|---|---|---|
| `general` | `general` | Direct mapping |
| `casatao` | `casatao` | Direct mapping |
| `yac` | `yworld` | yac = legacy alias for yworld |
| `lakshmi` | TBD | Legacy alias — decide in future gate |
| `fcs` | archive/legacy | No current canonical domain |

## Adding a New Domain

1. Create `04_DOMAINS/{domain}/README.md`
2. For active domains with full lifecycle: create `inbox/`, `workspace/`, `outbox/`, `archive/` subfolders with `.gitkeep`
3. Add domain to `bus_manifest.yaml` domains list
4. Add domain to `05_RUNTIME/runtime-registry.json` domains array
5. Execute via MPM gate
