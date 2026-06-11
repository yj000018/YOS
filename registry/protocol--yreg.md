---
slug: protocol--yreg
name: "Y-REG"
type: protocol
status: active
visibility: public
registration_stage: registry
version: "1.0.0"
description: "Y-OS Registry Protocol — defines how objects are discovered, validated and registered in Y-OS. Obsidian+Git is the source of truth. Supabase is a runtime cache."
tags: ["governance", "registry", "core"]
git_path: "registry/protocol--yreg.md"
---

# Y-REG — Y-OS Registry Protocol

Y-REG is the central registry of all Y-OS objects. It governs the full lifecycle from Discovery to Archive, and ensures every component of Y-OS is discoverable, versioned, and queryable.

## Pipeline
Discovery → Candidate → Validation → Registry
