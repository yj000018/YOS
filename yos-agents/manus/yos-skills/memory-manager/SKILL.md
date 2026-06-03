---
name: memory-manager
description: Persistent memory system using Notion for storing conversations, projects, knowledge, and preferences. Use when user requests to store information, archive conversations, load project context, search past discussions, create/update projects, or manage memory. Also use when detecting references to known projects or themes in conversation.
---

# Memory Manager

This skill enables persistent memory management through Notion, allowing Manus to remember context across sessions.

## System Overview

The memory system uses a Notion database "🧠 Manus Memory Hub" to organize information into five types:

1. **📝 Conversation Archive** - Structured summaries with ToC, key points, decisions, and transcripts
2. **🎯 Projet / Thème** - Project contexts with vision, status, and evolution
3. **💡 Connaissance Explicite** - Explicit knowledge user wants stored
4. **⚙️ Préférence / Configuration** - User preferences and settings
5. **📊 Résumé de Session** - Real-time session summaries

**Key constants and URLs**: Read `/home/ubuntu/skills/memory-manager/references/memory_system_constants.md` for database IDs, URLs, and configuration.

## User Preferences

- **Archiving**: On demand only (not automatic)
- **Format**: Both summary + chaptered transcript with ToC
- **Notifications**: Notify user at every memory update
- **Primary Project**: yOS (Yannick Operating System)

## Core Workflows

### 1. Store Explicit Knowledge

**Trigger**: User says "Stocke en mémoire : [info]" or similar

**Steps**:
1. Extract the information to store
2. Identify relevant tags from available tags list
3. Create page in Notion with Type = "💡 Connaissance Explicite"
4. Structure content clearly with context and examples
5. Notify user: "✅ Stocké en mémoire : [title]"

**Example**:
```
User: "Stocke en mémoire : Je préfère les architectures modulaires"
→ Create page "💡 Préférence Architecture Modulaire"
→ Tags: ["systems-thinking"]
→ Content: Description, context, examples
```

### 2. Archive Conversation

**Trigger**: User says "Archive cette conversation" or similar

**Steps**:
1. Analyze the conversation to extract:
   - Main subject (for title)
   - Executive summary (2-3 sentences)
   - Chapter structure (ToC)
   - Key points by chapter
   - Decisions made
   - Action items
   - Relevant tags
   - Related projects (if any)
2. Create JSON file with structure for archive_conversation.py script
3. Run: `python /home/ubuntu/skills/memory-manager/scripts/archive_conversation.py <json_file>`
4. Update related project pages with mention of this conversation
5. Notify user: "✅ Conversation archivée : [title] - [URL]"

**JSON Structure**:
```json
{
  "title": "Main subject",
  "summary": "2-3 sentence executive summary",
  "toc_items": ["Chapter 1", "Chapter 2", "Chapter 3"],
  "key_points": {
    "Chapter 1": ["Point 1", "Point 2"],
    "Chapter 2": ["Point 3", "Point 4"]
  },
  "decisions": ["Decision 1", "Decision 2"],
  "actions": ["Action 1", "Action 2"],
  "transcript_chapters": {
    "Chapter 1": "Full transcript text...",
    "Chapter 2": "Full transcript text..."
  },
  "tags": ["yOS", "philosophy"],
  "related_projects": ["https://www.notion.so/project-url"]
}
```

### 3. Load Project Context

**Trigger**: User says "Charge le contexte de [project]" or similar

**Steps**:
1. Search Notion for the project: `manus-mcp-cli tool call notion-search --server notion --input '{"query": "project name", "query_type": "internal"}'`
2. Fetch the project page: `manus-mcp-cli tool call notion-fetch --server notion --input '{"id": "page-url"}'`
3. Summarize context for user (vision, status, key themes, next steps)
4. Keep full content in active memory for this session
5. Notify user: "✅ Contexte chargé : [project name]"

### 4. Search Memory

**Trigger**: User asks "Qu'est-ce que je t'ai dit sur [subject]?" or similar

**Steps**:
1. Perform semantic search in Notion: `manus-mcp-cli tool call notion-search --server notion --input '{"query": "subject", "query_type": "internal"}'`
2. Fetch relevant pages
3. Synthesize findings for user
4. Provide links to full pages

**Advanced search options**:
- By date: Add `"filters": {"created_date_range": {"start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD"}}`
- By tag: Search with tag name in query
- By type: Filter results by entry type

### 5. Create New Project

**Trigger**: User says "Crée un nouveau projet : [name]" or similar

**Steps**:
1. Gather information: vision, themes, initial context
2. Select appropriate tags
3. Create page with Type = "🎯 Projet / Thème"
4. Use standard project structure:
   - Vision & Objectif
   - Contexte et Historique
   - État Actuel
   - Thèmes Clés
   - Prochaines Étapes (checklist)
   - Ressources Clés
   - Conversations Liées
   - Notes et Réflexions
5. Update ToC page with new project
6. Notify user: "✅ Projet créé : [name] - [URL]"

### 6. Update Project

**Trigger**: User says "Ajoute à la mémoire du projet [X] : [info]" or during conversation about known project

**Steps**:
1. Fetch current project page
2. Identify appropriate section to update
3. Use `notion-update-page` with `insert_content_after` or `replace_content_range`
4. Notify user: "✅ Projet [X] mis à jour : [what was updated]"

**Auto-detection**: When user mentions a known project name (e.g., "yOS"), proactively ask: "Je détecte des infos importantes sur [Project]. Dois-je mettre à jour la mémoire ?"

### 7. List Projects/Themes

**Trigger**: User says "Montre-moi mes projets actifs" or "Liste tous mes thèmes"

**Steps**:
1. Search for Type = "🎯 Projet / Thème" with Statut = "Actif"
2. Present as organized list with status and priority
3. Provide direct links

### 8. Create Preference Entry

**Trigger**: User states a preference or says "Stocke cette préférence"

**Steps**:
1. Extract preference and domain
2. Create page with Type = "⚙️ Préférence / Configuration"
3. Document: description, context, examples
4. Notify user

### 9. Session Summary (Real-time)

**Trigger**: Long conversation (>10 exchanges) or user requests

**Steps**:
1. Create/update page with Type = "📊 Résumé de Session"
2. Capture ongoing: decisions, insights, actions
3. Update incrementally during conversation
4. At end: "Veux-tu que j'archive cette session comme conversation complète ?"

## Advanced Features

### Contextual Intelligence

**Pattern Detection**: Monitor for recurring themes/questions. When detected 3+ times, suggest: "Je remarque que tu reviens souvent sur [theme]. Veux-tu que je crée un projet dédié ?"

**Auto-linking**: When creating/updating entries, automatically identify related projects and add mentions.

### Alerts & Reminders

**Integration with Google Calendar**: When user requests reminder about a project:
1. Create calendar event using Google Calendar MCP
2. Link to Notion project page in event description
3. Set appropriate notification

**Command**: "Rappelle-moi dans [timeframe] de réviser [project]"

### Analytics & Insights

**Usage Statistics**: When user asks "Qu'est-ce qui m'a occupé ce mois-ci ?" or similar:
1. Search conversations and updates by date range
2. Analyze tags and project mentions
3. Generate summary with themes, frequency, evolution

**Commands**:
- "Analyse mes thèmes récents"
- "Montre-moi l'évolution de [project]"
- "Quels projets j'ai négligés ?"

### Custom Templates

**Project Templates**: User can define custom templates for different project types.

**Creating template**: "Crée un template projet [type]" → Store in references/ or as Notion page

**Using template**: "Crée un projet [name] avec template [type]"

### Multi-Tool Integration

**Asana/Linear**: When user mentions tasks related to a memory project:
- Offer to create linked tasks in Asana/Linear
- Sync task status back to Notion project

**Slack**: Archive important Slack messages to memory with context

**GitHub**: Link GitHub repos to projects, track commits

**Wrike**: Sync Wrike projects with memory projects

**Command pattern**: "Lie ce projet à [tool]" or "Synchronise avec [tool]"

### Advanced Search

**By period**: "Qu'est-ce qu'on a discuté en décembre ?"
- Use `created_date_range` filter

**By multiple tags**: "Montre-moi tout sur philosophy ET consciousness"
- Search with combined query

**By status**: "Mes projets archivés"
- Filter by Statut property

## Notification Protocol

Always notify user after memory operations with format:

**Storage**: "✅ [Type emoji] Stocké : [title] - [URL]"

**Update**: "✅ [Type emoji] Mis à jour : [what] dans [project]"

**Search**: "🔍 Trouvé [N] résultats pour '[query]'"

**Context loaded**: "✅ Contexte chargé : [project] - [brief summary]"

## Error Handling

**Project not found**: Search with fuzzy matching, suggest similar names

**Notion API error**: Retry once, then inform user and suggest manual check

**Ambiguous request**: Ask clarifying questions before creating entries

## Best Practices

**Tagging**: Always add 2-4 relevant tags for better searchability

**Linking**: Cross-link related entries (conversations ↔ projects)

**Summaries**: Keep executive summaries concise (2-3 sentences max)

**Structure**: Use consistent heading hierarchy and formatting

**Updates**: When updating projects, preserve existing structure and add to appropriate sections

**Context**: When loading project context, provide actionable summary, not just raw content
