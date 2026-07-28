# Y-WORLD Vault — KAP Import

**Source:** `yj000018/Y-WORLD` (private GitHub repo)  
**Imported:** 2026-07-28  
**Notes:** 234 MD files | 19 subsystems | Obsidian PKM vault

## Structure

| Folder | Content |
|---|---|
| `00_raw_vault/` | Raw Obsidian vault (234 notes, no .obsidian config) |
| `01_kap_processed/` | KAP-generated artifacts (index, factsheets, synthesis, catalog) |

## Processed Artifacts

| File | Description |
|---|---|
| `01_kap_processed/YWORLD-GLOBAL-SYNTHESIS.md` | Global synthesis of the vault (architecture, subsystems, principles) |
| `01_kap_processed/YWORLD-KAP-INDEX.md` | Full index — all 234 notes with stats |
| `01_kap_processed/YWORLD-MANUS-ACTIONABLE.md` | Notes flagged manus_actionable:true |
| `01_kap_processed/yworld-notes-catalog.json` | Machine-readable catalog (JSON) |
| `01_kap_processed/factsheets/` | 20 factsheets — one per folder/subsystem |

## Next Pipeline Steps

1. Cross-reference with Notion sessions in KAP (deduplication)
2. Inject K-Cards (`40_K-Cards/`) into Mem0
3. Sync `07_Agent_Operations/` with current Manus config
4. Feed `80_Archetypes/` into Archetypes synthesis pipeline
5. When Mac vaults arrive (Y-OS Main, KOSMOS, LUDIVINE) — merge & deduplicate
