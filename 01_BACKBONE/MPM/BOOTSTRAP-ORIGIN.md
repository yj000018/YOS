# MPM Bootstrap Origin

## History

MPM was originally developed in `yj000018/kap-control-plane` (private repo) as part of the KAP project bootstrap phase.

The bootstrap repo was named `kap-control-plane` because MPM was initially developed in the context of KAP. However, MPM is not KAP-specific — it is a universal yOS Backbone protocol for inter-LLM orchestration.

## Bootstrap Repo

```
repo:    yj000018/kap-control-plane (private)
branch:  master
runtime: 02_MPMs/
ledger:  00_META/inter_llm_execution_ledger.json
reports: 06_REPORTS/
```

## Migration Status

| Asset | Bootstrap Path | YOS Path | Status |
| :--- | :--- | :--- | :--- |
| Protocols | `02_MPMs/_runtime/*.md` | `01_BACKBONE/MPM/00_PROTOCOLS/` | copied |
| Schemas | `02_MPMs/_runtime/*.json` | `01_BACKBONE/MPM/01_SCHEMAS/` | copied |
| Adapters | `02_MPMs/_runtime/*-adapter.md` | `01_BACKBONE/MPM/02_ADAPTERS/` | copied |
| Templates | `02_MPMs/_runtime/*-template.md` | `01_BACKBONE/MPM/03_TEMPLATES/` | copied |
| Ledger (bootstrap snapshot) | `00_META/inter_llm_execution_ledger.json` | `01_BACKBONE/MPM/05_LEDGER/inter_llm_execution_ledger_bootstrap.json` | copied (snapshot) |
| KAP run history | `02_MPMs/executed/` | `01_BACKBONE/KAP/05_RUNS/bootstrap-history/` | deferred |

## Rules

- `kap-control-plane` must NOT be deleted until migration is Guardian-approved
- The bootstrap ledger snapshot is read-only reference — the live ledger remains in `kap-control-plane`
- KAP-specific MPM execution history stays in `kap-control-plane` or moves to `01_BACKBONE/KAP/05_RUNS/bootstrap-history/`

---

*MPM Bootstrap Origin — 2026-07-05*
