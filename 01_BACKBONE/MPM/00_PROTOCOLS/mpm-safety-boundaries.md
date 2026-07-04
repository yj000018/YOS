# yOS MPM Safety Boundaries

> **yOS MPM — Mega Prompt Manager** (Inter-LLM Prompt Runtime & Relay System)
> Permanent Safety Constraints
> Version: 1.1.0 — Patch: YOS-MPM-NAMING-PATCH-2026-07-04

---

## 1. Permanent Boundaries (Non-Negotiable)

The following constraints apply to **every yOS MPM packet execution** regardless of mode or packet type, unless an explicit Architect & Guardian override is documented in the packet frontmatter and confirmed by a gate.

| Boundary | Description |
| :--- | :--- |
| No live source mutation | Do not modify source corpora (Obsidian vaults, GDrive, iCloud, GitHub Y-WORLD) outside of explicitly authorized gates. |
| No premature merge | Do not merge source corpora until the merge plan has been reviewed and authorized. |
| No premature synthesis | Do not generate Current Best Synthesis until the `CURRENT-BEST-KNOWLEDGE-AUTHORIZATION-GATE` has been passed. |
| No premature canonicalization | Do not promote any source to canonical status without a gate report and Architect & Guardian acceptance. |
| No broad unbounded scan | Do not scan entire vaults or directories without a scoped metadata-only gate first. |
| No destructive deduplication | Do not delete source fragments or claims. Deduplication is synthesis-layer only. |
| No ingestion before gate approval | Do not ingest any source into the KAP pipeline without a passed extraction gate. |
| No source corpus contamination | Do not mix control-plane artifacts (gate reports, schemas, registries) into source corpora. |
| All extractions into quarantine | All extracted source material goes to `_raw_quarantine/` subdirectories. |
| All decisions traceable through Git | Every decision must be committed to Git with a hash. No ephemeral decisions. |

## 2. LUDIVINE-Specific Boundaries

- No content access to LOCAL-OBS-001 (LUDIVINE) until `LUDIVINE-SCOPE-DECISION-GATE` is passed.
- No file copy, extraction, dry-run, or synthesis from LUDIVINE.
- Metadata-only operations (file names, folder names, sizes, dates) are allowed only within an authorized gate.

## 3. Boundary Violation Protocol

If a boundary is violated:
1. **STOP immediately.**
2. Write a boundary violation report to `06_REPORTS/BOUNDARY-VIOLATION-<DATE>.md`.
3. Mark the MPM `blocked`.
4. Update the ledger JSON.
5. Notify the Architect & Guardian.
6. Do not attempt to self-correct without Architect & Guardian authorization.

## 4. Boundary Confirmation in Reports

Every gate report must include a **Boundary Confirmations** section explicitly listing all 10 permanent boundaries and confirming each was respected.
