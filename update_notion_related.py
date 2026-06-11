#!/usr/bin/env python3
"""Update Y-REG related Notion pages to reflect 9-module architecture."""
import subprocess, json

def mcp_call(tool, payload):
    cmd = ["manus-mcp-cli", "tool", "call", tool,
           "--server", "notion", "--input", json.dumps(payload)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    output = result.stdout + result.stderr
    print(f"[{tool}] {output[-300:]}")
    return output

# ─────────────────────────────────────────────────────────────────────────────
# 1. Update Y-REG Object Model — add Y-CTX, Y-ID, Y-LOG to relationships
# ─────────────────────────────────────────────────────────────────────────────
OBJECT_MODEL_PAGE_ID = "37c35e21-8cf8-81b3-a707-d0a4791d4f75"

OBJECT_MODEL_ADDENDUM = """

---

## Update v1.1 — 9-Module Architecture (June 12, 2026)

Three new modules have been added to Y-OS Core Architecture:

**Y-CTX (Context)** — Extracts and assembles context from Y-MEM. Produces Context Packs consumed by Y-ORC. Not a storage module; a processing module.

**Y-ID (Identity)** — Manages naming conventions, namespaces, and unique identifiers across all Y-OS objects. Ensures consistency in Y-REG object naming.

**Y-LOG (Audit)** — Records operational history and audit trail. Receives events from Y-ORC after Mission Pack execution.

### Impact on Y-REG Object Model

Y-REG objects should now include a `module_owner` field indicating which module is responsible for the object lifecycle. Y-CTX, Y-ID, and Y-LOG are valid module owners alongside the original 6.

### Updated Module-to-Object Mapping

| Module | Primary Objects in Y-REG |
|--------|--------------------------|
| Y-REG  | Protocol, Collection |
| Y-MEM  | Knowledge System |
| Y-CTX  | Workflow (context assembly) |
| Y-ORC  | Agent, Workflow (orchestration) |
| Y-CAP  | Capability |
| Y-DEV  | Skill, Script, Prompt |
| /YOS   | Command |
| Y-ID   | (naming conventions, not stored as objects) |
| Y-LOG  | (audit records, separate from Y-REG) |
"""

mcp_call("notion-update-page", {
    "page_id": OBJECT_MODEL_PAGE_ID,
    "command": "insert_content",
    "content": OBJECT_MODEL_ADDENDUM,
    "position": {"type": "end"}
})

# ─────────────────────────────────────────────────────────────────────────────
# 2. Update Y-REG Technical Architecture — note on Y-CTX split from Y-ORC
# ─────────────────────────────────────────────────────────────────────────────
TECH_ARCH_PAGE_ID = "37c35e21-8cf8-81a1-87be-df16944646d4"

TECH_ARCH_ADDENDUM = """

---

## Architecture Update — Y-CTX Extracted from Y-ORC (June 12, 2026)

The original architecture described Y-ORC as both assembling context AND orchestrating execution. This has been formally separated:

**Y-CTX** now owns context extraction and assembly (reads Y-MEM, produces Context Pack).

**Y-ORC** now exclusively owns orchestration (consumes Context Pack, produces Mission Pack).

This separation improves testability, caching (Context Packs can be cached), and module clarity.

### Updated Data Flow

```
Y-MEM --> Y-CTX --> [Context Pack] --> Y-ORC --> [Mission Pack] --> Execution
                                          |
                                       Y-REG (tool lookup)
                                          |
                                       Y-LOG (audit)
```

This does not change the technical architecture choice (Architecture C: Obsidian+Git + Supabase Cache). It refines the internal module boundaries.
"""

mcp_call("notion-update-page", {
    "page_id": TECH_ARCH_PAGE_ID,
    "command": "insert_content",
    "content": TECH_ARCH_ADDENDUM,
    "position": {"type": "end"}
})

# ─────────────────────────────────────────────────────────────────────────────
# 3. Update ADR — note that module count changed from 6 to 9
# ─────────────────────────────────────────────────────────────────────────────
ADR_PAGE_ID = "37c35e21-8cf8-81ce-9bef-c037bab5873b"

ADR_ADDENDUM = """

---

## ADR Update — Module Count: 6 -> 9 (June 12, 2026)

The original ADR was written with 6 modules. Y-OS Core Architecture v1 has been updated to 9 modules.

**New modules added:**
- Y-CTX (Context) — extracted from Y-ORC for separation of concerns.
- Y-ID (Identity) — naming and namespace management.
- Y-LOG (Audit) — operational history and audit trail.

**Architecture Decision C remains valid.** The addition of Y-CTX, Y-ID, and Y-LOG does not change the storage architecture. These modules interact with the same Obsidian+Git source of truth and Supabase runtime cache.

**Y-CTX** will read from Y-MEM (Supabase cache or Git fallback) to assemble Context Packs. No new storage backend required.

**Y-LOG** will write to a dedicated `yreg_audit_log` table in Supabase. This is append-only and does not affect the core Y-REG schema.

**Y-ID** is a pure naming convention module — no dedicated storage required.
"""

mcp_call("notion-update-page", {
    "page_id": ADR_PAGE_ID,
    "command": "insert_content",
    "content": ADR_ADDENDUM,
    "position": {"type": "end"}
})

print("\n=== All 3 related pages updated ===")
