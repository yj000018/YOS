# Authentication

> **Version:** v1.0.0
> **Gate:** MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE

---

## Authentication Model

Authentication in yOS is identity-based, not credential-based.

An agent is authenticated by:
1. Its `agent_id` matching a registered entry in `agents.json`
2. Its declared `trust_level` matching the registry
3. Its message being carried by a trusted transport

---

## Transport Authentication

| Transport | Auth Method |
|---|---|
| Workspace Filesystem | Manus session identity (implicit) |
| Git | GitHub PAT (Manus Secrets) |
| Manus API | x-manus-api-key header |
| Manual Upload | Human operator session |
| Webhooks | Webhook secret (future) |
| MCP | MCP server auth (future) |

---

## Authentication Invariants

- Secrets MUST be stored in Manus Secrets or 1Password
- Secrets MUST NOT be copy-pasted manually
- Authentication tokens MUST NOT appear in Git commits
- Authentication failures MUST be logged as YARP ERROR messages
