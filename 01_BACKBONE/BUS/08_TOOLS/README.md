# BUS Tools

## bus.py

**Path:** `01_BACKBONE/BUS/08_TOOLS/bus.py`
**Requirements:** Python 3 stdlib only — no external dependencies.

### Commands

```bash
# Show BUS status and configuration
python 01_BACKBONE/BUS/08_TOOLS/bus.py status

# List all registered BUS domains
python 01_BACKBONE/BUS/08_TOOLS/bus.py domains

# List inbox contents for a domain
python 01_BACKBONE/BUS/08_TOOLS/bus.py inbox --domain mpm

# Dry-run claim from domain inbox (shows what would be claimed)
python 01_BACKBONE/BUS/08_TOOLS/bus.py claim --domain mpm --dry-run

# Apply claim (moves one file from inbox to workspace)
python 01_BACKBONE/BUS/08_TOOLS/bus.py claim --domain mpm --apply

# Validate BUS structure
python 01_BACKBONE/BUS/08_TOOLS/bus.py validate

# Show runtime paths
python 01_BACKBONE/BUS/08_TOOLS/bus.py runtime-paths

# Initialize a new runtime root
python 01_BACKBONE/BUS/08_TOOLS/bus.py init-runtime --root /path/to/runtime

# List outbox contents for a domain
python 01_BACKBONE/BUS/08_TOOLS/bus.py outbox --domain mpm
```

### Safety Rules

- `bus.py` does not execute MPM content.
- `claim --dry-run` only shows what would be claimed — no file moves.
- `claim --apply` moves exactly one file if exactly one candidate exists and no ambiguity.
- No arbitrary command execution from BUS packets.
- Safe path handling — no path traversal.
