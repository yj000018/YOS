# SOURCE SURFACE REGISTRY

**Last Updated:** 2026-07-04 (Overnight Batch — Registry Correction Patch)
**Version:** v3 — corrected all Y-WORLD counts

## All Known Source Surfaces

| Surface ID | Name | Channel | MD Count | Status |
|---|---|---|---|---|
| GITHUB-YWORLD | Y-WORLD GitHub Repo | GitHub | 234 | `GITHUB_YWORLD_CANONICAL_CANDIDATE` |
| GDRIVE-OBS-003 | Y-WORLD (GDrive — BACKUP) | GDrive | 61 | `GDRIVE_YWORLD_PARTIAL_SNAPSHOT` |
| LOCAL-GIT-YW | Y-WORLD (Local Git — BACKUP) | Local | 61 | `LOCAL_GIT_YW_PARTIAL_SNAPSHOT` |
| ICLOUD-YWORLD | Y-World iCloud Vault | iCloud | 17 (3 retained) | `ICLOUD_YWORLD_UNIQUE_FRAGMENTS` |
| LOCAL-YWORLD | Y-WORLD Local Vault (distinct) | Local | Unknown | `LOCAL_YWORLD_UNPROBED_GAP` |
| LOCAL-OBS-001 | LUDIVINE Principal | Local | 1842 | `DISCOVERED_NOT_AUTHORIZED_PENDING_SCOPE_DECISION` |
| LOCAL-OBS-002 | LUDIVINE Backup | Local | 1418 | `BACKUP_EXCLUDED_FINAL` |
| LOCAL-OBS-003 | testing vault | Local | 5 | `TEST_EXCLUDED_FINAL` |
| ICLOUD-TEST | iCloud Test vault | iCloud | Unknown | `TEST_EXCLUDED_FINAL` |
| GDRIVE-OBS-001 | Obsidian Vault (GDrive) | GDrive | 1 | `CONFIGURATION_ONLY_EXCLUDE` |
| GDRIVE-OBS-002 | Obsidian Vault 2 (GDrive) | GDrive | 0 | `OUT_OF_SCOPE_EXCLUDE` |

## Correction Log (v3)

- GDrive Y-WORLD count corrected from "235" and ">100" to **61 MD files**.
- GDrive Y-WORLD role corrected from "mirror" to "partial older snapshot".
- LOCAL-GIT-YW confirmed as matching GDrive snapshot (61 MD).
- GitHub Y-WORLD confirmed as strongest canonical candidate (234 MD).
