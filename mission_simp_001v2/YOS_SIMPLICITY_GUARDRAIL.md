---
id: YOS_SIMPLICITY_GUARDRAIL
title: Y-OS Simplicity Guardrail — Permanent Rules
status: ACTIVE
date: 2026-06-14
tags: [guardrail, simplicity, governance, permanent]
---

# Y-OS Simplicity Guardrail

> **Complexity is the enemy of daily use. Every module added is a module that must be understood, maintained, and debugged.**

---

## The 5 Guardrail Rules

### G1 — Weekly Test
> Any component not needed weekly is OPTIONAL.  
> Any component not needed monthly is ARCHIVE candidate.

Before adding a module, ask: *Will I use this every week?*  
If no → it's optional infrastructure, not core.

### G2 — Workload Test
> Any component that does not reduce human workload is suspect.

Before adding a module, ask: *Does this save me time or cognitive effort?*  
If no → it's theoretical completeness, not daily usefulness.

### G3 — Boring Infrastructure Preference
> Prefer boring, well-understood infrastructure over clever abstractions.

A `dict` is better than a `Registry`. A `list` is better than a `Queue`.  
Complexity should be earned, not assumed.

### G4 — Fewer Modules Preference
> When two modules do similar things, merge them.  
> When a module has one use case, archive it after use.

The correct number of modules is the minimum that covers the cognitive loop.

### G5 — No Theoretical Completeness
> Y-OS is not a research project. It is a personal tool.  
> Build for what you do, not for what you might do.

---

## The Complexity Budget

Y-OS has a **complexity budget** of 30 active modules.

| Zone | Budget | Current | Status |
|:---|---:|---:|:---|
| Core (5 modules) | 20 modules | 20 | ✅ |
| Optional (activated) | 10 modules | varies | ✅ |
| **Total active** | **30 modules** | **20–30** | ✅ |
| Experimental (archived) | unlimited | 34 | archived |

**Rule:** If adding a module exceeds 30 active modules, one must be archived first.

---

## The Simplicity Review (Monthly)

Every month, run this 5-question review:

1. Which modules did I use this week?
2. Which modules did I not use this month?
3. What is the current active module count?
4. Is there anything I can merge?
5. Is there anything I can archive?

If active count > 30 → archive the lowest-use module.

---

## Anti-Patterns to Avoid

| Anti-Pattern | Example | Correct Approach |
|:---|:---|:---|
| Module proliferation | 4 dashboard generators | 1 templated generator |
| Version accumulation | kg_compiler v1, v2, v3, v4 | Archive all but current |
| One-time tools as permanent | legacy_lineage_recovery | Archive after use |
| Experimental as core | simulation_engine | Keep in /experimental/ |
| Abstraction for abstraction | simulation_governance | Merge into lakshmi |
| Dashboard sprawl | 17 dashboards | 3 canonical |
| Canvas sprawl | 26 canvas maps | 3 canonical |

---

## The Simplicity Manifesto

Y-OS is a **Personal Cognitive Operating System**.

It is not:
- A research platform
- An enterprise architecture showcase
- A theoretical completeness exercise

It is:
- A daily tool for thinking better
- A memory system for working smarter
- An execution layer for acting faster

**Simple enough to understand in 5 minutes. Powerful enough to run a cognitive organization.**
