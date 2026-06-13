---
id: yos-dashboard-runtime
title: Dashboard — Runtime
type: dashboard
date: '2026-06-14'
tags: ['#dashboard', '#runtime', '#yos']
parent: '[[09_Dashboards_MOC]]'
---

# Dashboard — Runtime

*Requires Dataview plugin.*

---

## Runtime Components

```dataview
TABLE
  title AS "Title",
  status AS "Status",
  implements AS "Implements",
  depends_on AS "Depends On"
FROM "concepts/"
WHERE domain = "runtime"
SORT title ASC
```

---

## Files Implementing CCR Runtime

```dataview
TABLE
  title AS "Title",
  type AS "Type",
  date AS "Date"
FROM "/"
WHERE implements AND contains(implements, "[[CCR_Runtime]]")
SORT date DESC
```

---

## Files Implementing Artifact Primacy

```dataview
TABLE
  title AS "Title",
  type AS "Type"
FROM "/"
WHERE implements AND contains(implements, "[[Artifact_Primacy]]")
SORT title ASC
```

---

## Navigation

- [[concepts/Y_ORC]] — Y-ORC Concept
- [[concepts/CCR_Runtime]] — CCR Runtime Concept
- [[YOS_Runtime_Flow]] — Visual Runtime Flow
