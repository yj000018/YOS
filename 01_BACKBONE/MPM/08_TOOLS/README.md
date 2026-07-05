# yOS MPM — Local CLI Tools

> **Canonical runtime:** `yj000018/YOS @ main / 01_BACKBONE/MPM/`
> **Legacy bootstrap:** `kap-control-plane` — fallback only, never default.

## Purpose

`mpm.py` is a dependency-light Python 3 CLI for local MPM queue/ledger/report operations.

It enables the optimized local runtime loop:

```
git pull
python 01_BACKBONE/MPM/08_TOOLS/mpm.py queue
python 01_BACKBONE/MPM/08_TOOLS/mpm.py run-next --dry-run
# Manus executes the selected MP cognitively/agentically
python 01_BACKBONE/MPM/08_TOOLS/mpm.py finalize-run --mp-id <mp_id> --status executed_awaiting_architect_guardian_review
git add .
git commit -m "Execute MP <mp_id>"
git push
```

## Design Principles

- Python 3 only — no external dependencies beyond stdlib
- Safe by default — no arbitrary command execution from MP content
- Usable from repo root: `python 01_BACKBONE/MPM/08_TOOLS/mpm.py <command>`
- JSON-first: all writes go to JSON first, MD views are generated
- One commit per MP run

## Commands

| Command | Description |
| :--- | :--- |
| `queue` | Show ready queue + queue condition |
| `latest-report` | Show latest MPR pointer |
| `validate` | Validate MPM structure integrity |
| `run-next --dry-run` | Show what would run (no execution) |
| `reconcile-ledger --dry-run` | Show ledger inconsistencies |
| `reconcile-ledger --apply` | Apply safe metadata patches |
| `write-latest-report --mp-id <id>` | Update latest-mpr.json pointer |
| `finalize-run --mp-id <id> --status <status>` | Update ledger after execution |

## Files

```
08_TOOLS/
├── README.md          ← this file
├── mpm.py             ← CLI entry point
└── tests/
    ├── README.md
    └── test_mpm_cli.py
```

## Usage Examples

```bash
# From repo root:
python 01_BACKBONE/MPM/08_TOOLS/mpm.py queue
python 01_BACKBONE/MPM/08_TOOLS/mpm.py validate
python 01_BACKBONE/MPM/08_TOOLS/mpm.py run-next --dry-run
python 01_BACKBONE/MPM/08_TOOLS/mpm.py latest-report
python 01_BACKBONE/MPM/08_TOOLS/mpm.py reconcile-ledger --dry-run
```
