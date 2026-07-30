# Y-OS Architecture Baseline v0.5
## 11 — Source-of-Truth Matrix

| Domain | Primary candidate | Secondary | Notes |
|---|---|---|---|
| Code | Git | deployment/runtime | versioned truth |
| Architecture docs | Git Markdown | Obsidian / Notion | final role audit |
| Human knowledge interface | Obsidian | Notion | ADR evidence |
| Operational documentation | Notion | Obsidian | do not disrupt yet |
| Raw evidence | ARCH store | provider exports | append-only |
| Canonical knowledge | KAP Graph | Git artifacts | provenance required |
| Capability registry | Y-REG | Git schema | Growth adds lifecycle evidence |
| Runtime state | Y-Nexus/runtime DB | Supabase candidate | not canonical memory |
| Context products | Context Pack store | KAP views | CCR compiles |
| Job state | Y-Nexus | event log | auditable |
| Model routing | CRT policy store | Y-REG metadata | Growth calibrates |
| Action routing | ART policy store | Y-REG metadata | includes non-LLM tools |
| Historical narrative | Chronicles | ARCH Archaeology | narrative vs evidence |
| Personal data | Universe candidate | KAP / Obsidian | boundary unresolved |
| Secrets | dedicated secret manager | secure local store | never Git/Notion/chat |

## Principle
No repository or SaaS becomes authoritative merely because it is convenient. Authority is declared by domain and recorded through ADR.
