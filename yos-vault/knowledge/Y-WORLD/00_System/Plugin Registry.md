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

# Plugin Registry

| Plugin | Category | Status | Profile | Purpose | Risk | Dependencies | Configuration Notes | Manus Relevance | Activation Mode |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Dataview** | Core | Core | Minimal, Research, Operator, AI | Dynamic metadata queries & dashboards. | Low | None | Enable JS queries, set refresh interval to 10s. | High (reads state) | Auto |
| **Templater** | Core | Core | Minimal, Research, Operator | Advanced note generation with JS support. | Low | None | Set template folder to `04_Templates/`. | High (creates notes) | Auto |
| **QuickAdd** | Core | Core | Minimal, Operator | Fast note creation and structured capture. | Low | Templater | Configure hotkeys for K-Cards, Projects, Logs. | High (triggers) | Auto |
| **Metadata Menu**| Core | Core | Operator | Schema enforcement and property editing. | Low | Dataview | Define fields for note types (k-card, project). | High (edits metadata) | Auto |
| **Tasks** | Core | Core | Minimal, Operator | Task aggregation and tracking across vault. | Low | None | Define global task filter if needed. | Medium (reads tasks) | Auto |
| **Obsidian Git** | Core | Core | Minimal, Operator | Version control and automated backups. | Low | Git | Configure auto-backup interval (e.g., 60m). | High (backup) | Auto |
| **Linter** | Core | Core | Minimal | Enforce formatting and metadata hygiene. | Low | None | Run on save. Formats YAML, spacing, lists. | Medium (hygiene) | Auto |
| **Homepage** | Cockpit | Recommended| Operator | Force vault to open on `HOME.md`. | Low | None | Set to `01_Cockpit/HOME.md`. | Low | Manual |
| **Commander** | Cockpit | Recommended| Operator | Add custom buttons to UI panels. | Low | None | Bind buttons to QuickAdd and Templater commands. | Low | Manual |
| **Excalidraw** | Cockpit | Recommended| Research, Operator | Visual mind mapping and spatial control. | Low | None | Enable embed support and auto-export SVG. | Medium (reads maps) | Manual |
| **Local REST API**| Auto | Recommended| Operator, AI | Local HTTP server to read/write vault. | High | None | Require HTTPS, secure API token in Manus Secrets.| Critical (API) | Secure |
| **Advanced URI** | Auto | Recommended| Operator | Trigger Obsidian actions via URL. | Medium | None | Allow executing commands via external links. | High (automation) | Auto |
| **Shell Commands**| Auto | Optional | Operator | Execute local shell commands from Obsidian. | High | None | Restrict to non-destructive Git & sync tasks. | Medium | Manual |
| **Omnisearch** | Research | Recommended| Research | Semantic search inside PDFs, images, notes. | Low | None | Enable indexing. | Low | Manual |
| **Zotero Integr.**| Research | Recommended| Research | Sync academic papers and citations. | Low | Zotero | Configure template for reference notes. | Low | Manual |
| **Readwise Off.** | Research | Recommended| Research | Sync highlights from articles and books. | Low | Readwise | Configure sync on startup. | Low | Auto |
| **Copilot** | AI | Experimental| AI | Chat with vault using local or cloud LLMs. | Medium | API Keys | Configure Anthropic or OpenAI API keys securely. | Low | Manual |
| **Smart Connect.**| AI | Experimental| AI | Vector-based semantic note linking. | Medium | OpenAI API | Indexing takes time; use cloud embedding. | Low | Manual |
