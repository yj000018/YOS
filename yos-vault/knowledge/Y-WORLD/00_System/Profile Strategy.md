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

# Profile Strategy

To prevent plugin bloat, performance degradation, and cognitive overload, Y-WORLD uses modular **Cognitive Profiles**. These profiles determine which plugins are active depending on the user's current focus.

## 1. Profile Matrix

| Profile | Focus | Core Plugins (Always ON) | Profile-Specific Plugins (ON) | Plugins (OFF) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Minimal** | Writing, low-distraction, high speed | Dataview, Templater, QuickAdd, Tasks, Git, Linter | None | AI plugins, heavy visual plugins, experimental plugins |
| **2. Research**| Reading, sources, PDFs, highlights, knowledge capture | Dataview, Templater, QuickAdd, Tasks, Git, Linter | Zotero Integration, Readwise, PDF++, Omnisearch, Excalidraw | AI plugins, heavy automation plugins |
| **3. Operator**| Y-WORLD cockpit, automation, dashboards, Manus control | Dataview, Templater, QuickAdd, Tasks, Git, Linter | Metadata Menu, Commander, Homepage, Advanced URI, Local REST API, Shell Commands, Excalidraw | Experimental AI plugins |
| **4. AI** | AI experimentation, semantic search, augmentation | Dataview, Templater, QuickAdd, Tasks, Git, Linter | Copilot, Smart Connections, Text Generator, Khoj, Local REST API | None |
| **5. Lab** | Plugin testing, unstable experimentation | None | Tested plugins | Main vault plugins (Use a separate test vault instead) |

## 2. Profile Rules

* **Default Profile**: The **Operator** profile is the default operational state of the vault.
* **Minimal as Escape**: Switch to the **Minimal** profile when needing long stretches of uninterrupted deep focus or writing.
* **AI Isolation**: AI plugins must remain isolated in the **AI** profile. They are never enabled by default in daily operations to prevent performance lag and API token drainage.
* **Lab Protocol**: Never test unstable or unverified plugins directly in the main Y-WORLD vault. Use a secondary "Sandbox" vault for all testing.
