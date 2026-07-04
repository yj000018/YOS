# YOS Cleanup Candidates

> **Status:** Proposal only — no deletion performed.
> All items require explicit Architect & Guardian approval before any action.
> Generated: 2026-07-05 | Branch: `yos-monorepo-canonical-reorganization`

---

## Cleanup Candidates

| Path | Reason | Safe Action Later | Dependencies | Risk | A&G Required |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `yos-governance/` | Migrated to `01_BACKBONE/GOVERNANCE/` | archive or delete after verification | ADRs, policy-manifest.json | medium | yes |
| `yos-governance/yos-governance/` | Nested duplicate folder | delete (content merged to parent) | none | low | yes |
| `plugins/` | Migrated to `04_INTERFACES/obsidian/` | archive or delete after verification | yos-reader plugin | low | yes |
| `archive/` | Empty (.gitkeep only) | delete | none | low | no |
| `yos-related/legacy/` | Empty (.gitkeep only) | delete | none | low | no |
| `yos-related/temporary/` | Empty (.gitkeep only) | delete | none | low | no |
| `yos-agents/routing/` | Migrated to `01_BACKBONE/ROUTING/` | archive or delete after verification | routing rules | low | yes |
| `yos-related/undecided/Y-Browser-Admin/` | Unknown classification | classify first, then archive or migrate | unknown | medium | yes |
| `yos-related/undecided/YMap/` | Unknown classification | classify first, then archive or migrate | unknown | medium | yes |

---

## Do NOT Clean Up (Keep In Place)

| Path | Reason |
| :--- | :--- |
| `yos-agents/` | Large — migration deferred to next gate |
| `yos-apps/` | Large — migration deferred to next gate |
| `yos-automations/` | Migration deferred to next gate |
| `yos-vault/` | Large vault (281 files) — migration deferred |
| `README.md` | Root README — update, do not delete |

---

## Next Steps

1. Architect & Guardian reviews this list
2. Approves specific items for deletion/archiving
3. Manus executes approved cleanup in a dedicated gate: `YOS-CLEANUP-EXECUTION-GATE`

---

*Worker G — Lane G | Manus — 2026-07-05*
