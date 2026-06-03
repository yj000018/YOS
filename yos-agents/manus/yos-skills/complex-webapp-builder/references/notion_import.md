# Notion Import Workflow

When user provides a Notion link containing requirements, follow this workflow to import all content.

## Detecting Notion Links

Notion links follow these patterns:
- `https://www.notion.so/Page-Title-{page_id}`
- `https://notion.so/{workspace}/Page-Title-{page_id}`
- Any URL containing `notion.so`

## Import Process

### Step 1: Read Main Page

Use Notion MCP to read the main requirements page:

```bash
manus-mcp-cli resource read notion://{page_id} --server notion
```

The page ID is the last segment of the URL (after the last hyphen).

Example:
- URL: `https://www.notion.so/My-App-Requirements-abc123def456`
- Page ID: `abc123def456`

### Step 2: Discover Subpages

Check if the main page contains links to subpages:
- Look for internal Notion links in the content
- Identify child pages in the page structure
- Extract all subpage IDs

### Step 3: Read All Subpages

For each discovered subpage:

```bash
manus-mcp-cli resource read notion://{subpage_id} --server notion
```

### Step 4: Aggregate Content

Combine all content into a single requirements document:
1. Start with main page content
2. Append each subpage with clear section headers
3. Preserve hierarchy and structure
4. Save aggregated content to a local file for reference

## Example Workflow

```bash
# Read main page
manus-mcp-cli resource read notion://abc123def456 --server notion > requirements_main.md

# If subpages exist, read them
manus-mcp-cli resource read notion://xyz789ghi012 --server notion > requirements_sub1.md
manus-mcp-cli resource read notion://def456jkl345 --server notion > requirements_sub2.md

# Aggregate into single file
cat requirements_main.md requirements_sub1.md requirements_sub2.md > full_requirements.md
```

## Handling Errors

**Authentication Issues:**
- Notion MCP will trigger OAuth automatically if needed
- Wait for user to complete authentication
- Retry the read operation

**Permission Errors:**
- Verify user has access to the page
- Ask user to share the page or provide alternative access

**Missing Subpages:**
- If subpage links are broken, note in requirements
- Ask user if content is missing or if links should be ignored

## Content Processing

After importing:
1. Parse markdown content for structured information
2. Extract feature lists, requirements, and specifications
3. Identify technical constraints and dependencies
4. Proceed to Phase 1 requirements analysis
