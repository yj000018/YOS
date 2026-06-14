---
id: yos-dashboard-adrs
title: Dashboard — ADRs
type: dashboard
date: '2026-06-14'
tags: ['#dashboard', '#adrs', '#yos']
parent: '[[09_Dashboards_MOC]]'
---

# Dashboard — ADRs

*Requires Dataview plugin. Install: Settings → Community Plugins → Dataview*

---

## All ADRs

```dataview
TABLE
  title AS "Title",
  status AS "Status",
  date AS "Date",
  owner AS "Owner"
FROM "/"
WHERE type = "adr"
SORT date DESC
```

---

## ADRs by Status

```dataview
TABLE
  title AS "Title",
  date AS "Date"
FROM "/"
WHERE type = "adr" AND status = "ACCEPTED"
SORT date ASC
```

---

## ADRs with Supersession Chain

```dataview
TABLE
  title AS "Title",
  supersedes AS "Supersedes",
  superseded_by AS "Superseded By"
FROM "/"
WHERE type = "adr" AND (supersedes OR superseded_by)
SORT date ASC
```

---

## ADRs Linked to Missions

```dataview
TABLE
  title AS "Title",
  mission AS "Mission",
  produces AS "Produces"
FROM "/"
WHERE type = "adr" AND mission
SORT mission ASC
```

---

## Navigation

- [[02_ADRs_MOC]] — ADR Map of Content
- [[YOS_ADR_Dependency_Map]] — Visual Dependency Map


## Semantic Links

- **reports_to:** [[lmp_canonicalize_MISSION-016-C]], [[lmp_compile_MISSION-016-C]], [[lmp_inject_MISSION-016-C]]