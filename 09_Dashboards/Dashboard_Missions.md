---
id: yos-dashboard-missions
title: Dashboard — Missions
type: dashboard
date: '2026-06-14'
tags: ['#dashboard', '#missions', '#yos']
parent: '[[09_Dashboards_MOC]]'
---

# Dashboard — Missions

*Requires Dataview plugin.*

---

## All Missions

```dataview
TABLE
  title AS "Title",
  status AS "Status",
  date AS "Date",
  owner AS "Owner"
FROM "/"
WHERE type = "mission"
SORT date ASC
```

---

## Passed Missions

```dataview
TABLE
  title AS "Title",
  date AS "Date",
  related_adrs AS "ADRs"
FROM "/"
WHERE type = "mission" AND status = "PASSED"
SORT date ASC
```

---

## Missions by Owner

```dataview
TABLE
  title AS "Title",
  status AS "Status",
  date AS "Date"
FROM "/"
WHERE type = "mission"
GROUP BY owner
SORT date DESC
```

---

## Navigation

- [[03_Missions_MOC]] — Mission Map of Content
- [[YOS_Mission_Evolution]] — Visual Mission Timeline


## Semantic Links

- **reports_to:** [[lmp_canonicalize_MISSION-016-C]], [[lmp_compile_MISSION-016-C]], [[lmp_inject_MISSION-016-C]]