# BUS Runtime Backend Protocol

**Version:** 1.0.0
**Status:** active

---

## Backend Priority

```
1. direct_file   — preferred fast transport (non-versioned)
2. manus_cloud   — probe required before production use
3. git           — durable/auditable fallback
4. google_drive  — cloud synced fallback
5. nas           — optional local network
6. blob_payload  — experimental payload only (requires pointer)
```

---

## Backend Selection Rules

1. Check if `$YOS_BUS_RUNTIME_ROOT` is set and accessible.
2. If yes: use `direct_file` backend.
3. If no: check if Manus cloud workspace is stable and addressable (probe required).
4. If no: fall back to `git` backend (requires commit).
5. If Git is unavailable: use `google_drive` if configured.
6. If none available: report `no_transport_backend_available`.

---

## Backend Definitions

### direct_file (preferred)

- **Status:** preferred
- **Versioned:** no
- **Requires Git commit for transport:** no
- **Root:** `$YOS_BUS_RUNTIME_ROOT`
- **Use when:** runtime root is accessible (local disk, NAS, iCloud, Dropbox, mounted volume).

### manus_cloud (probe required)

- **Status:** probe_required
- **Versioned:** no
- **Requires Git commit for transport:** no
- **Use when:** Manus persistent workspace is confirmed stable and addressable across sessions.
- **Probe questions:** see `05_RUNTIME/manus-cloud/README.md`.

### git (fallback)

- **Status:** fallback
- **Versioned:** yes
- **Requires Git commit for transport:** yes
- **Use when:** no fast transport available; durable audit trail required.
- **Limitation:** requires commit/push cycle; slower than direct_file.

### google_drive (fallback)

- **Status:** fallback
- **Versioned:** no
- **Requires Git commit for transport:** no
- **Use when:** Google Drive sync folder is accessible and configured.

### nas (optional)

- **Status:** optional
- **Versioned:** no
- **Requires Git commit for transport:** no
- **Use when:** NAS/N100 or local network filesystem is accessible.

### blob_payload (experimental)

- **Status:** experimental_payload_only
- **Versioned:** object-level
- **Requires pointer:** yes
- **Use when:** storing large payload content in Git blob; NOT for discoverable queues.
- **Limitation:** blob alone is not BUS — requires a pointer file to be discoverable.

---

## Runtime Root Configuration

Set environment variable:

```bash
export YOS_BUS_RUNTIME_ROOT=/path/to/your/bus/runtime
```

The runtime root must have the following structure:

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

Initialize with:

```bash
python 01_BACKBONE/BUS/08_TOOLS/bus.py init-runtime --root /path/to/runtime
```
