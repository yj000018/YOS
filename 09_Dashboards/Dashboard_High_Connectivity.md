---
id: yos-dashboard-high-connectivity
title: Dashboard — High Connectivity Nodes
type: dashboard
date: '2026-06-14'
tags: ['#dashboard', '#graph', '#yos']
parent: '[[09_Dashboards_MOC]]'
---

# Dashboard — High Connectivity Nodes

*Requires Dataview plugin. Shows files with the most semantic relations.*

---

## Files with Most Outbound Relations

```dataview
TABLE
  title AS "Title",
  type AS "Type",
  length(produces) + length(implements) + length(governed_by) + length(depends_on) + length(validates) AS "Outbound Edges"
FROM "/"
WHERE type != "dashboard"
SORT length(produces) + length(implements) + length(governed_by) + length(depends_on) + length(validates) DESC
LIMIT 20
```

---

## Concept Nodes with Most Connections

```dataview
TABLE
  title AS "Title",
  domain AS "Domain",
  length(adr_lineage) AS "ADR Links",
  length(mission_evidence) AS "Mission Links"
FROM "concepts/"
WHERE type = "concept"
SORT length(adr_lineage) + length(mission_evidence) DESC
LIMIT 20
```

---

## ADRs with Most Dependencies

```dataview
TABLE
  title AS "Title",
  length(depends_on) AS "Depends On",
  length(enables) AS "Enables",
  length(governed_by) AS "Governed By"
FROM "/"
WHERE type = "adr"
SORT length(depends_on) + length(enables) DESC
LIMIT 20
```

---

## Navigation

- [[00_Y-OS_Home]] — Home
- [[Dashboard_Orphans]] — Orphan Files
- [[YOS_ADR_Dependency_Map]] — ADR Dependency Map
