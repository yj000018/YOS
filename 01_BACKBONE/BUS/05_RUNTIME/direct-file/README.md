# BUS Runtime: direct-file

**Status:** preferred
**Versioned:** no

---

## Expected External Runtime Root

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

## Rules

- This runtime root is not Git-tracked by default.
- It is used for ultra-fast handoff.
- File writes are direct filesystem writes.
- Claim should be atomic where possible: rename/move `inbox/domain/file` → `workspace/domain/file`.
- Processed messages may later be persisted into YOS Git.
- Runtime root can be Manus cloud workspace, NAS, Google Drive synced folder, Dropbox, iCloud, local disk, mounted volume, etc.

---

## Configuration

```bash
export YOS_BUS_RUNTIME_ROOT=/path/to/your/bus/runtime
```

---

## Initialization

```bash
python 01_BACKBONE/BUS/08_TOOLS/bus.py init-runtime --root /path/to/runtime
```
