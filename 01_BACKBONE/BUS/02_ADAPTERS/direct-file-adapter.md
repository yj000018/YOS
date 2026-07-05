# BUS Direct File Adapter

**Status:** preferred
**Versioned:** no
**Requires Git commit for transport:** no

---

## Overview

The direct file adapter is the preferred fast transport backend for YOS BUS. It uses the local filesystem (or any mounted filesystem) as the transport medium. No Git commits are required for message passing.

---

## Configuration

Set the runtime root environment variable:

```bash
export YOS_BUS_RUNTIME_ROOT=/path/to/bus/runtime
```

Supported runtime root locations:
- Local disk (`/home/ubuntu/yos-bus-runtime/`)
- NAS mount (`/mnt/nas/yos-bus-runtime/`)
- iCloud Drive sync folder
- Dropbox sync folder
- Google Drive sync folder (use `google_drive` adapter instead for explicit tracking)
- Any mounted volume

---

## Runtime Structure

```
$YOS_BUS_RUNTIME_ROOT/
├── inbox/{general,mpm,kap,casatao,kosmos,yworld}/
├── workspace/{general,mpm,kap,casatao,kosmos,yworld}/
├── outbox/{general,mpm,kap,casatao,kosmos,yworld}/
├── archive/{general,mpm,kap,casatao,kosmos,yworld}/
├── ack/
├── locks/
└── dead-letter/
```

---

## Claim Atomicity

Claim should be atomic: rename/move `inbox/domain/file` → `workspace/domain/file`.

On POSIX systems, `os.rename()` is atomic within the same filesystem. Use this for claim operations.

---

## Initialization

```bash
python 01_BACKBONE/BUS/08_TOOLS/bus.py init-runtime --root /path/to/runtime
```

---

## Limitations

- Not versioned: no history of messages unless explicitly archived to Git.
- Not network-transparent: requires shared filesystem access.
- Not durable across machine failures unless on a reliable mounted volume.
