# Y-OS Architecture Baseline v0.5
## 07 — Implementation Evidence Matrix

| Claim | Classification | Confidence | Required evidence |
|---|---|---:|---|
| Y-ORC operational | IMPLEMENTATION_CLAIM | Medium-high | code, logs, missions |
| ART operational | IMPLEMENTATION_CLAIM | Medium-high | code, routes |
| Y-REG operational | IMPLEMENTATION_CLAIM | Medium-high | schema, API |
| CRT Runtime v1 designed | IMPLEMENTATION_CLAIM | High | ARCH-001 |
| CRT Runtime implemented | UNVERIFIED | Medium | source, tests |
| CCR Runtime v1 validated 5/5 | IMPLEMENTATION_CLAIM | Medium-high | golden tests |
| CCR Runtime v2 implemented | IMPLEMENTATION_CLAIM | Medium-high | six modules, tests |
| MISSION-001 passed | IMPLEMENTATION_CLAIM | Medium | run artifacts |
| MISSION-014 passed | IMPLEMENTATION_CLAIM | Medium-high | ADR-0041, graph |
| MISSION-016 passed | IMPLEMENTATION_CLAIM | Medium | run report |
| MODE-B/D/E without raw history | IMPLEMENTATION_CLAIM | Medium | tests |
| Y-OS Reader built | IMPLEMENTATION_CLAIM | Medium-high | repo/release |
| MOP partially implemented | IMPLEMENTATION_CLAIM | Medium-high | docs/workflows |
| KAP repository exists | VERIFIED_REPO | High | deeper audit pending |
| Obsidian vault integrated in YOS | VERIFIED_README | High | content audit |
| Git source-of-truth ADR | VERIFIED_GOVERNANCE | High | ADR-001 |
| Obsidian human-interface ADR | VERIFIED_GOVERNANCE | High | ADR-002 |

## Promotion rule

A claim becomes `IMPLEMENTED` only when code/configuration exists. It becomes `OPERATIONAL` only when a current successful run is evidenced. It becomes `CANON` only through architectural approval.
