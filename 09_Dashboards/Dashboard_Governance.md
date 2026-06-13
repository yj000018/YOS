---
id: yos-dashboard-governance
title: Dashboard — Governance
type: dashboard
date: '2026-06-14'
tags: ['#dashboard', '#governance', '#yos']
parent: '[[09_Dashboards_MOC]]'
---

# Dashboard — Governance

*Requires Dataview plugin.*

---

## All Governance Reports

```dataview
TABLE
  title AS "Title",
  status AS "Status",
  date AS "Date"
FROM "/"
WHERE type = "governance_report"
SORT date DESC
```

---

## ADRs Validated by Lakshmi

```dataview
TABLE
  title AS "Title",
  date AS "Date",
  governed_by AS "Governed By"
FROM "/"
WHERE type = "adr" AND governed_by
SORT date DESC
```

---

## Constitutional Articles Referenced

```dataview
TABLE
  title AS "Title",
  constrained_by AS "Constrained By",
  type AS "Type"
FROM "/"
WHERE constrained_by
SORT title ASC
```

---

## Navigation

- [[concepts/Governance_Determinism]] — Governance Determinism Concept
- [[concepts/Lakshmi_Governance]] — Lakshmi Governance Concept
- [[YOS_Governance_Flow]] — Visual Governance Flow
- [[YOS_Constitutional_Stack]] — Constitutional Stack Map
