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

# Metadata Schema

Every note in Y-WORLD should contain standardized frontmatter properties. This enables Dataview indexing, Metadata Menu validation, and agent parsing.

## 1. Core Properties

| Property | Type | Description | Allowed Values |
| :--- | :--- | :--- | :--- |
| `type` | text | The functional type of the note. | `world-node`, `project`, `k-card`, `dashboard`, `map`, `workflow`, `agent`, `tool`, `source`, `concept`, `decision`, `log`, `protocol`, `template` |
| `status` | text | The active state of the note or project. | `active`, `paused`, `completed`, `future`, `deprecated` |
| `domain` | text | The primary Y-WORLD region this note belongs to. | `Y-OS`, `Life`, `Knowledge`, `Projects`, `CasaTAO`, `ARC-Anandaz`, `Archetypes`, `Y-Publishing`, `AI-Systems`, `Interfaces` |
| `project` | text | The specific project this note is linked to. | e.g., `Y-WORLD`, `CasaTAO-Frigate`, `ARC-Infrastructure` |
| `created` | date | Note creation date (YYYY-MM-DD). | Date |
| `updated` | date | Note last updated date (YYYY-MM-DD). | Date |
| `source` | text | Source URL, book title, or reference. | URL, Text, or WikiLink |
| `tags` | list | Categorization tags (avoid tag explosion). | List of tags (e.g., `#cognitive`, `#automation`) |
| `related` | list | Links to related notes in the vault. | List of WikiLinks (e.g., `[[Y-OS MAP]]`) |
| `priority` | text | Priority level for actions or projects. | `high`, `medium`, `low` |
| `review_date` | date | Next scheduled review date. | Date |
| `owner` | text | The responsible entity or agent. | `Yannick`, `Manus`, `n8n` |
| `system_layer` | text | System level. | `system`, `user` |
| `automation_relevance` | text | Level of relevance for automated agents. | `high`, `medium`, `low` |
| `manus_actionable` | boolean| Whether Manus can directly modify this note. | `true`, `false` |
