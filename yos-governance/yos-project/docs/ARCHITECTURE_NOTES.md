# Architecture Notes — yOS

## System Architecture

```
User (Yannick)
    ↓
Manus (AI Operator)
    ├── Notion MCP → Thinking Layer
    ├── GitHub (PAT) → Building Layer
    ├── Gmail MCP → Communication
    ├── Slack MCP → Team Communication
    └── n8n → Automation Layer
            ├── NAS → Persistence
            └── External APIs
```

## Key Design Decisions

1. **Notion as single source of truth for thinking** — all vision, specs, decisions live in Notion
2. **GitHub as single source of truth for building** — all code, prompts, assets live in GitHub
3. **Manus as primary operator** — executes, builds, maintains, never just assists
4. **Skills as persistent protocols** — reusable across sessions via /home/ubuntu/skills/

## PAT Management

- PAT with `repo` scope: stored in 1Password as "GitHub API Token - PAT"
- PAT without scope: stored as "GitHub PAT — yOS-GITHUB-MCP-2026-03" (read-only)
