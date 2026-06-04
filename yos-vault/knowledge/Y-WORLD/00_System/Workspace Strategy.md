---
type: world-node
status: active
domain: Y-WORLD
project: Y-WORLD
created: 2026-05-28
updated: 2026-05-28
system_layer: system
automation_relevance: high
manus_actionable: true
---

# Workspace Strategy

Workspaces organize the physical layout of Obsidian (opened panes, sidebars, pinned notes) to match the active cognitive profile.

## 1. Defined Workspaces

### 1️⃣ Home Workspace
* **Primary Note**: `01_Cockpit/HOME.md` (Pinned, left side)
* **Secondary Panes**: `03_Dashboards/Y-WORLD Dashboard.md` (Right side, vertical split)
* **Visual Layer**: `02_Maps/Y-WORLD ROOT MAP.md` (Bottom pane or Excalidraw view)
* **Sidebars**: Collapsed left sidebar, right sidebar showing Tasks/Calendar.

### 2️⃣ Operator Workspace
* **Primary Note**: `03_Dashboards/Manus Dashboard.md`
* **Secondary Panes**: `03_Dashboards/Y-OS Dashboard.md`, `07_Agent_Operations/Manus Task Queue.md`
* **Sidebars**: Left sidebar expanded to show file structure and registries.

### 3️⃣ Research Workspace
* **Primary Note**: `03_Dashboards/Knowledge Dashboard.md`
* **Secondary Panes**: `10_Inbox/` (Folder view), active source note, Zotero import pane.
* **Sidebars**: Right sidebar showing backlinks and semantic graph.

### 4️⃣ Project Workspace
* **Primary Note**: `03_Dashboards/Projects Dashboard.md`
* **Secondary Panes**: Active Project Note (e.g., `50_Projects/Active-Project.md`), Project Log, related submap.
* **Sidebars**: Right sidebar showing project-specific tasks.

### 5️⃣ Symbolic Workspace
* **Primary Note**: `03_Dashboards/Archetypes Dashboard.md`
* **Secondary Panes**: `02_Maps/ARCHETYPES MAP.md` (Excalidraw/Canvas), Visual Atlas notes.
* **Sidebars**: Backlinks and image gallery folders.

### 6️⃣ CasaTAO Workspace
* **Primary Note**: `03_Dashboards/CasaTAO Dashboard.md`
* **Secondary Panes**: Smart home architecture, Home Assistant integration status, spatial map of CasaTAO.

## 2. Implementation

Workspaces should be saved using Obsidian's native **Workspaces** core plugin or the **Workspaces Plus** community plugin, matching these names exactly.
