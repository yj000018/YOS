---
name: complex-webapp-builder
description: Build production-ready web applications from detailed requirements documents. Use when user provides comprehensive specifications (10+ features), technical requirements documents, or "mega-prompts" describing complex web applications with database, authentication, API integrations, or multi-step processing workflows.
license: MIT
---

# Complex Web Application Builder

Build production-ready web applications from detailed requirements documents using a structured, phase-based approach that ensures complete feature implementation, proper testing, and stable deployment.

## When to Use This Skill

Use this skill when the user provides:
- Detailed requirements documents with 10+ features (text, attachments, or Notion links)
- Technical specifications or "mega-prompts" for web applications
- Notion pages containing requirements (single page or page with subpages)
- Complex application requirements involving databases, authentication, API integrations
- Multi-step data processing workflows
- Applications requiring LLM integration, file processing, or external service connections

## Core Workflow

### Phase 1: Requirements Analysis and Planning

**Import requirements** from provided source:
- If user provides a Notion link: Use Notion MCP to read the page and all subpages (see `references/notion_import.md` for detailed workflow)
- If user provides text/attachment: Read directly from message or file
- Aggregate all content into a comprehensive requirements document

**Parse the requirements document** to extract:
- Core purpose and user value proposition
- Complete feature list (categorize by: database, backend, frontend, integrations)
- Technical constraints (authentication, file formats, API providers)
- Data models and relationships
- Processing workflows and business logic

**Create structured plan**:
1. Use `plan` tool to define phases: schema design → backend implementation → frontend development → testing → delivery
2. Create `todo.md` at project root with ALL features as unchecked items organized by category
3. Never skip todo.md creation - it's the single source of truth for progress tracking

**Example todo.md structure**:
```markdown
# Project TODO

## Database & Schema
- [ ] Design user and project tables
- [ ] Create migration for relationships
- [ ] Add query helpers

## Backend Processing
- [ ] Implement file upload handler
- [ ] Build data extraction engine
- [ ] Create export generator

## Frontend Interface
- [ ] Design upload component with drag-drop
- [ ] Build processing dashboard
- [ ] Create export download UI

## Testing
- [ ] Write unit tests for core features
- [ ] Validate end-to-end workflow
```

### Phase 2: Database Schema Design

**Design comprehensive schema** covering:
- User management (if authentication required)
- Core domain entities (projects, jobs, items, etc.)
- Relationships and foreign keys
- Metadata fields (timestamps, status enums)
- Configuration storage (API keys, settings)

**Implementation**:
1. Edit `drizzle/schema.ts` with all tables
2. Run `pnpm db:push` to apply migrations
3. Add query helpers to `server/db.ts` for all CRUD operations
4. Mark schema tasks complete in `todo.md`

**Key patterns**:
- Use `int().autoincrement().primaryKey()` for IDs
- Use `timestamp().defaultNow()` for created/updated fields
- Use `mysqlEnum()` for status fields
- Always include foreign key relationships with `.references()`

### Phase 3: Backend Implementation

**Build processing engine** in `server/processing/`:
- Create modular processors (extraction, transformation, export)
- Implement external API integrations (LLM, storage, third-party services)
- Build background job processing if needed
- Add error handling and logging

**Create tRPC procedures** in `server/routers.ts`:
- Group by feature domain (projects, uploads, processing, exports)
- Use `protectedProcedure` for authenticated endpoints
- Use `publicProcedure` for public access
- Implement proper input validation with Zod schemas

**Mark completed backend tasks** in `todo.md` as `[x]` immediately after implementation.

### Phase 4: Frontend Development

**Choose layout pattern** based on app type:
- **Internal tools/dashboards**: Use `DashboardLayout` with sidebar navigation
- **Public-facing apps**: Design custom navigation and landing page

**Implement UI** in `client/src/pages/`:
- Start with landing/home page
- Create feature-specific pages (upload, processing, results)
- Use shadcn/ui components for consistency
- Implement proper loading states and error handling

**Data fetching patterns**:
- Use `trpc.*.useQuery()` for data fetching
- Use `trpc.*.useMutation()` for actions
- Implement optimistic updates for instant feedback
- Handle loading/empty/error states explicitly

**Mark frontend tasks complete** in `todo.md` after each page/component.

### Phase 5: Testing and Validation

**Write comprehensive tests** in `server/*.test.ts`:
- Test core business logic and data transformations
- Validate API procedures with mock contexts
- Test database operations and relationships
- Ensure proper error handling

**Run tests**:
```bash
pnpm test
```

**Fix failures** by debugging implementation, not tests (unless clear test error).

**Mark testing tasks complete** in `todo.md`.

### Phase 6: Checkpoint and Delivery

**Before creating checkpoint**:
1. Read `todo.md` to verify ALL items are marked `[x]`
2. Run `webdev_check_status` to confirm server health
3. Test critical user flows in browser preview

**Create checkpoint**:
```typescript
webdev_save_checkpoint({
  description: "Complete feature summary with all implemented functionality listed"
})
```

**Deliver to user**:
- Provide brief summary (< 100 words) of what was built
- Attach checkpoint URL: `manus-webdev://{version_id}`
- Suggest 2-3 concrete next steps for enhancement

## Critical Rules

### Todo.md Management
- **MUST create `todo.md` immediately after planning** - never skip this step
- **MUST update `todo.md` before implementing** when user requests changes
- **MUST mark items `[x]` immediately after completion** - not at checkpoint time
- **MUST verify all items complete** before creating checkpoint

### Checkpoint Discipline
- **First checkpoint only after complete delivery** - not during development
- **Subsequent checkpoints after each feature addition** - for rollback safety
- **Always verify todo.md completion** before checkpoint

### Dependency Management
- **Remove problematic native dependencies** if causing crashes (e.g., sharp, canvas)
- **Simplify algorithms** to avoid heavy dependencies when possible
- **Test server startup** after removing dependencies

### Testing Requirements
- **Write tests for core business logic** - not just CRUD operations
- **Test before delivery** - treat as required, not optional
- **Fix implementation when tests fail** - assume code is wrong first

## Common Patterns

### File Upload and Processing
```typescript
// Backend: Accept base64 or file URL
const uploadProcedure = protectedProcedure
  .input(z.object({ 
    fileName: z.string(),
    fileData: z.string(), // base64 or URL
  }))
  .mutation(async ({ input, ctx }) => {
    // Store to S3 using storagePut()
    const { url } = await storagePut(fileKey, buffer, mimeType);
    // Save metadata to database
    return { fileId, url };
  });
```

### Background Job Processing
```typescript
// Trigger job without blocking
async function processJobInBackground(jobId: number) {
  // Update status to "processing"
  await updateJobStatus(jobId, "processing");
  
  try {
    // Perform long-running work
    const result = await performProcessing(jobId);
    await updateJobStatus(jobId, "completed");
  } catch (error) {
    await updateJobStatus(jobId, "failed");
  }
}

// Don't await - return immediately
processJobInBackground(jobId);
return { jobId, status: "processing" };
```

### LLM Integration
```typescript
import { invokeLLM } from "./server/_core/llm";

const result = await invokeLLM({
  messages: [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: userPrompt },
  ],
});

const text = result.choices[0].message.content;
```

## Troubleshooting

### Server Crashes on Startup
- Check `.manus-logs/devserver.log` for errors
- Look for native module failures (sharp, canvas, etc.)
- Remove problematic dependencies and simplify implementation
- Restart server after fixes: `webdev_restart_server`

### Database Errors
- Verify foreign key relationships exist
- Check that `pnpm db:push` completed successfully
- Ensure user exists before creating related records in tests
- Use proper type casting for `insertId`: `Number((result as any)[0]?.insertId)`

### Test Failures
- Ensure database user exists before testing other features
- Call `upsertUser()` in test setup for authenticated contexts
- Check that return types match expected schema
- Verify async operations complete before assertions

## Success Criteria

Application is complete when:
- ✅ All items in `todo.md` marked `[x]`
- ✅ Server starts without errors
- ✅ All tests passing (`pnpm test`)
- ✅ Critical user flows work in browser preview
- ✅ Checkpoint created with comprehensive description
- ✅ User receives working application with next steps

## Tags

`#webdev` `#full-stack` `#database` `#trpc` `#react` `#complex-apps` `#requirements-driven` `#Manus`
