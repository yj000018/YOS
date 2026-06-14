---
id: yos-dashboard-concepts
title: Dashboard — Concepts
type: dashboard
date: '2026-06-14'
tags: ['#dashboard', '#concepts', '#yos']
parent: '[[09_Dashboards_MOC]]'
---

# Dashboard — Concepts

*Requires Dataview plugin.*

---

## All Concept Nodes

```dataview
TABLE
  title AS "Title",
  domain AS "Domain",
  status AS "Status",
  constitutional_grounding AS "Constitution"
FROM "concepts/"
WHERE type = "concept"
SORT domain ASC, title ASC
```

---

## Concepts by Domain

```dataview
TABLE
  title AS "Title",
  status AS "Status"
FROM "concepts/"
WHERE type = "concept"
GROUP BY domain
SORT domain ASC
```

---

## Concepts with ADR Lineage

```dataview
TABLE
  title AS "Title",
  adr_lineage AS "ADR Lineage",
  mission_evidence AS "Mission Evidence"
FROM "concepts/"
WHERE type = "concept" AND adr_lineage
SORT title ASC
```

---

## Navigation

- [[10_Concepts_MOC]] — Concepts Map of Content
- [[YOS_Organizational_Digital_Twin]] — Full System Map


## Semantic Links

- **reports_to:** [[lmp_canonicalize_MISSION-016-C]], [[lmp_compile_MISSION-016-C]], [[lmp_inject_MISSION-016-C]]