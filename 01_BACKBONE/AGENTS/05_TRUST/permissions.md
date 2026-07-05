# Permissions

> **Version:** v1.0.0
> **Gate:** MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE

---

## Permission Matrix

| Permission | T0 | T1 | T2 | T3 | T4 | T5 |
|---|---|---|---|---|---|---|
| read | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| write_runtime | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| write_git | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| execute_code | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| access_secrets | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| modify_corpus | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| create_automation | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| approve_canonical | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## Permission Scope

- `read` — read any yOS artifact (Git, filesystem, registry)
- `write_runtime` — write to sandbox/runtime filesystem (/home/ubuntu/)
- `write_git` — commit and push to yj000018/YOS
- `execute_code` — execute shell commands, Python, Node.js
- `access_secrets` — read API keys, tokens from Manus Secrets / 1Password
- `modify_corpus` — modify canonical corpus files (requires guardian review)
- `create_automation` — deploy n8n workflows, cron jobs, webhooks
- `approve_canonical` — approve canonical designation gates (MPM marathon)
