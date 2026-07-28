---
type: dashboard
status: active
domain: Y-WORLD
project: Y-WORLD
created: 2026-05-28
updated: 2026-05-28
system_layer: system
automation_relevance: high
manus_actionable: true
---

# Y-WORLD Dashboard

This dashboard aggregates the active state of all Y-WORLD regions.

## 🎯 Active Projects
```dataview
TABLE status, priority, review_date
FROM "50_Projects"
WHERE status = "active"
SORT priority DESC
```

## 🔄 Open Loops & Inbox
* **Inbox Count**: `10_Inbox/` contains unprocessed capture items.
* **Review Cycles**: Next Weekly Review scheduled for Friday.

## 🧠 Recent K-Cards
```dataview
TABLE domain, tags
FROM "40_K-Cards"
SORT file.mtime DESC
LIMIT 8
```

## 🗺️ System Map

| Layer       | Component                             | Status         |
| :---------- | :------------------------------------ | :------------- |
| Interface   | [[HOME]] · [[Y-WORLD Command Center]] | ✅ Active       |
| Memory      | [[Notion Memory Hub]]                 | ✅ Active       |
| Routing     | [[CRT Model Routing]]                 | ✅ Active       |
| Automation  | [[n8n Cognitive Automation]]          | ✅ Active       |
| Hardware    | [[Coral Edge TPU]] · [[Frigate NVR]]  | ✅ Active       |
| Sanctuaries | [[CasaTAO]] · [[ARC Anandaz]]         | ✅ Active       |
| Publishing  | [[Y-Publishing Dashboard]]            | 🔄 In Progress |
| Web         | [[REALITY INTERFACES MAP]]            | 🔜 Planned     |

## 🏛️ Life Notes
```dataview
LIST
FROM "20_Life"
SORT file.mtime DESC
```

## ✅ Open Tasks
```tasks
not done
```
