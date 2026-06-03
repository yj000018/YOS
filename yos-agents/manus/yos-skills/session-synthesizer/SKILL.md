---
name: session-synthesizer
description: Cross-session synthesis and analysis for Manus conversations. Use when user requests to analyze, synthesize, or create memory from multiple Manus sessions, extract themes across conversations, or build knowledge bases from session history.
---

# Session Synthesizer

Analyze and synthesize insights across multiple Manus sessions to create structured knowledge, identify patterns, and build cross-session memory.

## When to Use

- User provides multiple Manus session URLs (share links or private URLs)
- Request to "synthesize", "analyze", or "summarize" multiple sessions
- Building knowledge bases from conversation history
- Identifying themes, decisions, or patterns across sessions
- Creating cross-session memory for projects

## Core Workflow

### 0. Auto-Collect Session IDs (Optional)

If user doesn't provide URLs, automatically extract from Manus interface:

```python
# Navigate to Manus app
browser_navigate("https://manus.im/app", intent="informational", focus="Session list")

# Extract session IDs and titles via console
browser_console_exec("""
const sessions = [];
const sidebar = document.querySelector('nav');
const allClickables = Array.from(sidebar?.querySelectorAll('div[role="button"]') || []);

const menuItems = ['New task', 'Agents', 'Search', 'Library', 'Projects', 'View more', 'All tasks'];

const sessionElements = allClickables.filter(el => {
  const title = el.textContent?.trim();
  const clickId = el.getAttribute('data-manus_click_id');
  return title && title.length >= 10 && clickId && !menuItems.includes(title);
}).slice(0, 10);

for (const el of sessionElements) {
  sessions.push({
    id: el.getAttribute('data-manus_click_id'),
    title: el.textContent?.trim()
  });
}

JSON.stringify(sessions, null, 2);
""")
```

**Output**: List of 10 most recent sessions with IDs and titles.

**Interactive Selection**:

Present sessions to user in numbered list format:

```
Found 10 recent sessions:

1. [ID: 20] Partager les sessions via lien de synthèse globale
2. [ID: 22] Création de Site Web Original et Interactif avec EYA
3. [ID: 26] VISUAL REALITY - Experienced Art
...
10. [ID: 47] UI/UX Redesign for yOS Dashboard and Control Center

Which sessions do you want to synthesize?
Options:
- "all" for all 10 sessions
- "1,3,5" for specific sessions by number
- "1-5" for range of sessions
```

Parse user selection and build final URL list.

**Note**: This requires authenticated browser session. If user is not logged in, ask for share links instead.

### 1. Collect Session URLs

Accept session URLs in these formats:
- **Share links**: `https://manus.im/share/{id}` (publicly accessible)
- **Private URLs**: `https://manus.im/app/{id}` (requires authentication)
- **Internal IDs**: From Step 0 auto-collection

Validate URLs and confirm count with user before proceeding.

### 2. Extract Session Content

For each session:

```python
# Navigate to session URL
browser_navigate(url, intent="informational", focus="Extract full conversation content")

# Read extracted markdown
file_read(f"/home/ubuntu/page_texts/manus.im_share_{id}.md")

# Save to structured file
file_write(f"/home/ubuntu/sessions/session_{id}.md", content)
```

**Key extraction points:**
- Full conversation transcript
- User requests and agent responses
- Decisions made
- Files/artifacts created
- Action items or next steps

### 3. Analyze Themes

Identify cross-session patterns:
- **Recurring topics**: Themes mentioned across multiple sessions
- **Decision chains**: How decisions in one session affect later ones
- **Knowledge evolution**: How understanding develops over time
- **Action tracking**: Completed vs pending items across sessions

### 4. Create Synthesis Document

Structure:
1. **Executive Summary** (2-3 paragraphs)
2. **Session Overview** (table with ID, title, date, key focus)
3. **Cross-Session Themes** (major patterns with session references)
4. **Decision Timeline** (chronological decisions with context)
5. **Knowledge Graph** (concepts and their relationships)
6. **Action Items** (consolidated from all sessions)
7. **Recommendations** (next steps based on synthesis)

### 5. Archive to Memory (Optional)

Use memory-manager skill to persist synthesis to Notion.

**Important**: This creates a **copy** of the synthesis in Notion for long-term reference. Original Manus sessions remain untouched and accessible.

## Best Practices

### Content Extraction

- **Save incrementally**: Write each session to file immediately after extraction
- **Handle failures**: If a session URL fails, log it and continue with others
- **Preserve structure**: Maintain markdown formatting for readability

### Analysis Quality

- **Cite sources**: Always reference which session(s) support each insight
- **Avoid hallucination**: Only synthesize from actual session content
- **Identify gaps**: Note when sessions reference missing context

### Synthesis Structure

- **Be concise**: Executive summary should be scannable in 60 seconds
- **Use tables**: Session overviews and timelines work best in tabular format
- **Link concepts**: Show how ideas connect across sessions explicitly

## Output Formats

### Standard Synthesis

Markdown document with sections above. Attach as primary deliverable.

### Knowledge Base Export

JSON format for programmatic use:

```json
{
  "sessions": [...],
  "themes": [...],
  "decisions": [...],
  "knowledge_graph": {...},
  "action_items": [...]
}
```

### Notion Archive

Structured Notion page via memory-manager with:
- Session links as database entries
- Themes as tags
- Decisions as timeline
- Actions as checkboxes

## Error Handling

### Session Access Failures

If session URL returns 404 or auth error:
1. Log the failure
2. Ask user if they can provide share link instead
3. Continue with accessible sessions
4. Note missing sessions in synthesis

### Incomplete Extraction

If markdown extraction is truncated:
1. Scroll and re-extract
2. Use browser_console_exec to get full HTML
3. Mark session as "partial" in synthesis

## Examples

### Example 1: Project Retrospective

**Input**: 5 sessions about building a webapp
**Output**: Synthesis showing:
- Initial requirements → final implementation
- Design decisions and rationale
- Technical challenges and solutions
- Lessons learned

### Example 2: Research Compilation

**Input**: 10 sessions exploring AI agents
**Output**: Knowledge base with:
- Key concepts and definitions
- Comparative analysis of approaches
- Unanswered questions
- Recommended reading

## Limitations

- **Maximum sessions**: Recommend <20 sessions per synthesis (context limits)
- **Session length**: Very long sessions (>50k tokens) may need summarization first
- **Real-time sync**: Synthesis is snapshot, not live-updated
- **Private sessions**: Require user authentication, cannot be shared

## Integration with Other Skills

- **memory-manager**: Archive synthesis to Notion for persistence
- **task-manager**: Extract and track action items from synthesis
- **github-gem-seeker**: Find tools mentioned across sessions
