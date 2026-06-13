#!/usr/bin/env python3
"""
MISSION-015 — Generate 8 Dataview dashboard notes
"""

from pathlib import Path

DASH_DIR = Path("/home/ubuntu/yreg/09_Dashboards")
DASH_DIR.mkdir(exist_ok=True)
TODAY = "2026-06-14"

DASHBOARDS = {
    "Dashboard_ADRs": """---
id: yos-dashboard-adrs
title: Dashboard — ADRs
type: dashboard
date: '{today}'
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
""",

    "Dashboard_Missions": """---
id: yos-dashboard-missions
title: Dashboard — Missions
type: dashboard
date: '{today}'
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
""",

    "Dashboard_Concepts": """---
id: yos-dashboard-concepts
title: Dashboard — Concepts
type: dashboard
date: '{today}'
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
""",

    "Dashboard_Governance": """---
id: yos-dashboard-governance
title: Dashboard — Governance
type: dashboard
date: '{today}'
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
""",

    "Dashboard_Runtime": """---
id: yos-dashboard-runtime
title: Dashboard — Runtime
type: dashboard
date: '{today}'
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
""",

    "Dashboard_Memory": """---
id: yos-dashboard-memory
title: Dashboard — Memory
type: dashboard
date: '{today}'
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
""",

    "Dashboard_Orphans": """---
id: yos-dashboard-orphans
title: Dashboard — Orphan Files
type: dashboard
date: '{today}'
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
""",

    "Dashboard_High_Connectivity": """---
id: yos-dashboard-high-connectivity
title: Dashboard — High Connectivity Nodes
type: dashboard
date: '{today}'
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
""",
}

def gen_dashboards():
    for name, content in DASHBOARDS.items():
        path = DASH_DIR / f"{name}.md"
        path.write_text(content.replace("{today}", TODAY), encoding="utf-8")
        print(f"  ✅ {name}.md")

    # MOC for dashboards
    moc = f"""---
id: yos-dashboards-moc
title: 09 Dashboards MOC
type: moc
date: '{TODAY}'
tags: ['#moc', '#dashboard', '#yos']
parent: '[[00_Y-OS_Home]]'
---

# 09 — Dashboards

*Requires Dataview plugin: Settings → Community Plugins → Dataview*

---

## All Dashboards

| Dashboard | Focus |
| :--- | :--- |
| [[Dashboard_ADRs]] | All ADRs, status, supersession chains |
| [[Dashboard_Missions]] | All missions, status, ADR links |
| [[Dashboard_Concepts]] | All concept nodes by domain |
| [[Dashboard_Governance]] | Governance reports, constitutional references |
| [[Dashboard_Runtime]] | Runtime components, implementations |
| [[Dashboard_Memory]] | Memory pipeline, LMP artifacts |
| [[Dashboard_Orphans]] | Files with no links or unknown type |
| [[Dashboard_High_Connectivity]] | Top connected nodes in the graph |

---

## Navigation

- [[00_Y-OS_Home]] — Home
- [[08_Visual_Maps_MOC]] — Visual Maps
- [[10_Concepts_MOC]] — Concepts
"""
    moc_path = DASH_DIR / "09_Dashboards_MOC.md"
    moc_path.write_text(moc, encoding="utf-8")
    print(f"  ✅ 09_Dashboards_MOC.md")

if __name__ == "__main__":
    gen_dashboards()
    print(f"\nTotal files in 09_Dashboards/: {len(list(DASH_DIR.iterdir()))}")
    print("Done.")
