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

# Obsidian OS Cockpit

This document defines the configuration strategy to transform Obsidian into a functional, aesthetic, and live cockpit for Y-WORLD.

## 1. UI Configuration

* **Theme**: **Minimal Theme** (Clean, high performance, customizable).
* **Color Scheme**: Dark mode by default, high contrast but soft on the eyes (Nord or Gruvbox palette recommended).
* **Font**: Monospace or clean Sans-Serif (e.g., Inter, JetBrains Mono) to emphasize structure.
* **Layout**:
  * **Left Sidebar**: File Explorer (collapsed by default), Search, and Quick Capture.
  * **Right Sidebar**: Backlinks, Tag Pane, and Calendar.
  * **Center Pane**: Split vertically into two main views when operating:
    * Left side: `01_Cockpit/HOME.md` or a Map.
    * Right side: Active Workspace Note / Daily Log.

## 2. Interface Elements

* **Homepage**: Configured using the **Homepage** plugin to open `01_Cockpit/HOME.md` automatically on startup.
* **Commander Icons**: Customized navigation bar at the top or status bar for fast access to:
  1. Open HOME (`01_Cockpit/HOME.md`)
  2. Open Y-WORLD ROOT MAP (`02_Maps/Y-WORLD ROOT MAP.md`)
  3. Create K-Card (via QuickAdd)
  4. Create Daily Note
  5. Sync Git
* **Iconize**: Assign distinct, functional emojis or SVG icons to the core folder structure to provide immediate visual hierarchy.
