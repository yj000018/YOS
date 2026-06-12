---
id: protocol--yid
type: protocol
name: Y-ID
slug: yid
status: active
visibility: public
version: "1.0"
description: Naming, namespaces and identifier management module. Ensures consistent naming across all Y-OS objects.
question: How do we identify things?
produces: Resolved identifiers, namespace maps
consumes: Object definitions
equivalent_role: Information Architect
tags: [core, identity, naming, deterministic, backend]
module_owner: Y-ID
created_at: "2026-06-12"
---

# Y-ID — Identity Module

Y-ID is a system module (deterministic). It manages naming conventions and namespaces.

## Responsibilities
- Define and enforce naming conventions for Y-OS objects
- Resolve identifiers across modules (slug, id, canonical name)
- Manage namespaces to prevent collisions
- Provide canonical lookup: name → id, slug → object

## Non-Responsibilities
- Does not store object content (Y-REG)
- Does not store memory (Y-MEM)
- Does not orchestrate (Y-ORC)

## Naming Convention
Format: `{type}--{slug}` (e.g., `protocol--ydev`, `skill--memory-manager`)
Slugs: lowercase, hyphen-separated, no special characters.
