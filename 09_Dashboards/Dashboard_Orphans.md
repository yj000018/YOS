---
id: yos-dashboard-orphans
title: Dashboard — Orphan Files
type: dashboard
date: '2026-06-14'
tags: ['#dashboard', '#orphans', '#yos']
parent: '[[09_Dashboards_MOC]]'
---

# Dashboard — Orphan Files

*Requires Dataview plugin. Shows files with no inbound links.*

---

## Files with Unknown Type

```dataview
TABLE
  file.name AS "File",
  file.folder AS "Folder",
  file.mtime AS "Modified"
FROM "/"
WHERE !type OR type = "unknown"
SORT file.mtime DESC
LIMIT 50
```

---

## Files with No Relations

```dataview
TABLE
  file.name AS "File",
  type AS "Type",
  file.folder AS "Folder"
FROM "/"
WHERE !derives_from AND !supersedes AND !implements AND !governed_by AND !depends_on AND !produces AND !validates
AND type != "concept" AND type != "moc" AND type != "dashboard"
SORT file.name ASC
LIMIT 50
```

---

## Files with No Parent MOC

```dataview
TABLE
  file.name AS "File",
  type AS "Type"
FROM "/"
WHERE !parent
SORT file.name ASC
LIMIT 50
```

---

## Navigation

- [[00_Y-OS_Home]] — Home
- [[Dashboard_High_Connectivity]] — High Connectivity Files


## Semantic Links

- **reports_to:** [[lmp_canonicalize_MISSION-016-C]], [[lmp_compile_MISSION-016-C]], [[lmp_inject_MISSION-016-C]]