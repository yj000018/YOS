---
id: yos-dashboard-memory
title: Dashboard — Memory
type: dashboard
date: '2026-06-14'
tags: ['#dashboard', '#memory', '#lmp', '#yos']
parent: '[[09_Dashboards_MOC]]'
---

# Dashboard — Memory

*Requires Dataview plugin.*

---

## Memory Concepts

```dataview
TABLE
  title AS "Title",
  status AS "Status",
  adr_lineage AS "ADR Lineage"
FROM "concepts/"
WHERE domain = "memory"
SORT title ASC
```

---

## Files Implementing Living Memory

```dataview
TABLE
  title AS "Title",
  type AS "Type",
  date AS "Date"
FROM "/"
WHERE implements AND contains(implements, "[[Living_Memory]]")
SORT date DESC
```

---

## Files with Session Delta Relations

```dataview
TABLE
  title AS "Title",
  type AS "Type"
FROM "/"
WHERE implements AND contains(implements, "[[Session_Delta]]")
SORT title ASC
```

---

## Navigation

- [[concepts/Living_Memory]] — Living Memory Concept
- [[concepts/Session_Delta]] — Session Delta Concept
- [[concepts/Canonical_Memory]] — Canonical Memory Concept
- [[YOS_Living_Memory_Pipeline]] — Visual Pipeline Map
