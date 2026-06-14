# Y-OS Value Trace Standard

**Standard ID:** MISSION-TRACE-STANDARD-001  
**Date:** 2026-06-14  
**Status:** ACTIVE

This document defines the standard for generating visual traces of Y-OS execution.

## 1. Core Principle

**Value first, architecture second.**

The purpose of a trace is not to show that Y-OS is complex or has many modules. The purpose is to prove that Y-OS creates operational value for Yannick.

Every trace must answer one question: *Did this help Yannick finish real work?*

## 2. When to Use Which Format

* **Mermaid + Obsidian Canvas:** Default for lightweight, everyday traces.
* **Excalidraw (This Standard):** On-demand only. Used for important missions, external sharing, architectural review, or when Yannick explicitly requests a detailed visual explanation.

## 3. Mandatory Zones

Every Excalidraw trace must include these 8 zones, laid out from left to right:

### A. REQUEST PANEL
Shows exactly what Yannick asked, the classified intent, and the expected output.

### B. TEAM FLOW
Shows the team members (Client, Orchestrator, Workers, Validator, Memory Systems) who touched the request.
Each box must include: Role, Worker, Provider, Model, Tools used, Input, Output, Latency, Cost, and Artifact created.

### C. ARTIFACT HANDOFFS
The arrows between team members must explicitly state what was passed: Artifact Name, Token Count, Latency, and Cost.

### D. PLUGINS SKIPPED
Must clearly list inactive plugins (e.g., ODT, Strategic Intel) to prove that Core-Only Mode (or the active governance policy) was respected.

### E. RUNTIME METRICS
Aggregate data: Total time, total cost, total tokens, models used, tools used, artifacts created.

### F. VALUE PANEL
Must list:
- What was created (Artifacts)
- What decisions were produced
- What knowledge was added
- What repositories were updated
- The final deliverable returned to Yannick

### G. FINAL VERDICT: DID Y-OS CREATE VALUE?
Must be **YES**, **NO**, or **AMBER**.
- **YES:** Show exactly where value was produced.
- **AMBER:** Explain what was self-referential and what was actionable.
- **NO:** Explain what was overhead and why no value was created.

### H. WITHOUT Y-OS vs WITH Y-OS
A bottom comparison panel showing the manual steps required without Y-OS vs the automated steps with Y-OS. This proves the operational value.

## 4. Color Coding

To maintain consistency across all traces:
- **Blue:** Humans (Client)
- **Purple:** Agents (Orchestrators)
- **Green:** LLMs (Workers)
- **Orange:** Tools (Memory, External APIs)
- **Red:** Governance (Validators)
- **Yellow:** Artifacts / Deliverables
- **Grey:** Skipped plugins

## 5. Implementation

Do not create new runtime modules to generate these traces. Use the provided `value_trace_schema.json` to structure the data, and generate the Excalidraw JSON programmatically using the established Python scripts.
