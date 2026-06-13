---
id: protocol--yid
title: protocol--yid
type: protocol
status: active
date: '2026-06-13'
version: '1.0'
owner: Manus Y-OS
tags:
- core
- identity
- naming
- deterministic
- backend
source_branch: y-os-doctrine
canonical: true
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
