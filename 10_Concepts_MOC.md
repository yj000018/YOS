---
id: yos-concepts-moc
title: Y-OS Concepts — Map of Content
type: index
status: ACTIVE
date: '2026-06-13'
owner: Brahma
parent: '[[00_Y-OS_Home]]'
related_adrs:
- '[[ADR-0041]]'
- '[[ADR-0040]]'
tags:
- '#yos'
- '#artifact'
- '#accepted'
aliases:
- Concepts MOC
- Concept Layer
source_branch: y-os-doctrine
canonical: true
---

# Y-OS Concepts — Map of Content

> Concepts are the **first-class semantic entities** of the Y-OS Cognitive Graph. They are not documents, not ADRs, not missions. They are the named abstractions that give meaning to the document layer beneath them.

---

## The Three Layers

```
Document Graph  →  Concept Graph  →  Cognitive Graph
(MISSION-013)       (MISSION-014)      (MISSION-015+)
```

---

## Concept Index

### Constitutional Domain

| Concept | Domain | Constitutional Grounding | Status |
| :--- | :--- | :--- | :--- |
| [[Artifact_Primacy]] | constitution | Article I | CANONICAL |
| [[Preservation_Principle]] | constitution | Article II | CANONICAL |
| [[Derivation_Transparency]] | constitution | Article III | CANONICAL |
| [[Human_Override]] | constitution | Article IV | CANONICAL |
| [[Governance_Before_Autonomy]] | constitution | Article V | CANONICAL |

### Context Architecture Domain

| Concept | Domain | ADR Lineage | Status |
| :--- | :--- | :--- | :--- |
| [[CCR_Runtime]] | context | ADR-0029 → ADR-0030 → ADR-0037 | CANONICAL |
| [[Context_Pack]] | context | ADR-0036, ADR-0037 | CANONICAL |
| [[Context_Router]] | context | ADR-0037 | CANONICAL |

### Memory Domain

| Concept | Domain | ADR Lineage | Status |
| :--- | :--- | :--- | :--- |
| [[Session_Delta]] | memory | ADR-0038 | CANONICAL |
| [[Living_Memory]] | memory | ADR-0039 | CANONICAL |

### Governance Domain

| Concept | Domain | ADR Lineage | Status |
| :--- | :--- | :--- | :--- |
| [[Constitutional_Governance]] | governance | ADR-0033, ADR-0034, ADR-0035 | CANONICAL |
| [[Governance_Determinism]] | governance | ADR-0033 | CANONICAL |

---

## Concept Relationships

```
Artifact_Primacy ──────────────────────────────────────────┐
  └─depends_on──→ Preservation_Principle                   │
  └─depends_on──→ Derivation_Transparency                  │
                                                            │
Governance_Before_Autonomy ────────────────────────────────┤
  └─implements──→ Constitutional_Governance                 │
  └─depends_on──→ Governance_Determinism                   │
                                                            │
CCR_Runtime ───────────────────────────────────────────────┤
  └─implements──→ Context_Pack                             │
  └─implements──→ Context_Router                           │
  └─depends_on──→ Session_Delta                            │
                                                            │
Living_Memory ─────────────────────────────────────────────┤
  └─depends_on──→ Session_Delta                            │
  └─depends_on──→ CCR_Runtime                              │
  └─depends_on──→ Canonical_Memory (future concept)        │
                                                            │
All concepts ──────────────────────────────────────────────┘
  └─governed_by──→ Artifact_Primacy (Article I)
```

---

## Semantic Query Examples (Dataview)

```dataview
TABLE domain, status, constitutional_grounding
FROM "concepts"
WHERE type = "concept"
SORT domain ASC
```

```dataview
TABLE adr_lineage, mission_evidence
FROM "concepts"
WHERE type = "concept" AND domain = "context"
```

---

## Navigation

- [[00_Y-OS_Home]] — Home
- [[01_Constitution_MOC]] — Constitutional Layer
- [[02_ADR_MOC]] — ADR Register
- [[06_Context_Architecture_MOC]] — Context Architecture
- [[07_Living_Memory_MOC]] — Living Memory
