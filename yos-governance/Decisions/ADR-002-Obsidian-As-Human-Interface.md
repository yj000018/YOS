# ADR-002: Obsidian as Human Cognitive Interface

**Date:** 2026-06-03  
**Status:** Accepted  
**Decided by:** YOS Governance

---

## Context

YOS requires a human interface that supports non-linear thinking, linked notes, knowledge graphs, and daily logs — without being code-first.

## Decision

Obsidian (via Y-WORLD repository) is the designated human cognitive interface for YOS.

## Consequences

- Y-WORLD is a Core YOS repo (Category A)
- Obsidian vault syncs to Git via Y-WORLD
- Human reads/writes happen in Obsidian
- Agents read structured content from Git, not directly from Obsidian
- Obsidian plugins and vault config are version-controlled in Y-WORLD
