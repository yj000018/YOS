---
id: yos-ccr-runtime-v2-architecture
title: CCR Runtime v2 Architecture
type: runtime_spec
status: ACCEPTED
mission: MISSION-011
date: '2026-06-13'
version: v2
owner: Manus Y-OS
parent: '[[03_Missions_MOC]]'
related_adrs:
- '[[ADR-0033]]'
related_missions:
- '[[mission_011]]'
constitutional_articles:
- 'Article I: Artifact Primacy'
tags:
- '#accepted'
- '#ccr'
- '#lineage'
- '#memory'
- '#runtime'
- '#session-delta'
- '#yos'
aliases:
- MISSION-011
source_branch: y-os-doctrine
canonical: true
---

# CCR Runtime v2 — Context Orchestration Architecture

## 1. Executive Summary
CCR Runtime v2 is the production context orchestration layer for Y-OS. It replaces monolithic conversational history with an artifact-driven, multi-modal context compiler. Its primary mandate is to ensure that LLM executions receive the highest quality-per-token context substrate (Mode B by default), injecting Canonical Memory and Session Deltas only when deterministically required.

## 2. Runtime Components

### 2.1 Artifact Registry
The canonical ledger of all organizational state changes. In v2, this transitions from a Notion database to a Git-backed structured metadata store (e.g., YAML frontmatter in Markdown files).

### 2.2 Canonical Memory
The immutable foundation of Y-OS truth. Consists of:
- **Constitutional Core v1** (Articles I-V)
- **Accepted ADRs**
- **Organizational Directives**

### 2.3 Context Compiler
The engine that transforms raw artifacts into executable Context Packs.
- **Extraction:** Retrieves artifacts based on mission ID and lineage depth.
- **Filtering:** Removes obsolete or superseded artifact versions.
- **Relevance Scoring:** Ranks artifacts based on semantic proximity to the current task.
- **Compression:** Applies summarization to low-relevance artifacts.
- **Packaging:** Assembles the final YAML/Markdown Context Pack.

### 2.4 Context Router
The decision engine that selects the appropriate Context Mode (B, D, or E) based on capability requirements, governance risk scores, and token budgets.

### 2.5 Session Delta Layer
A high-efficiency replacement for raw session history. It captures only the *diff* of the current execution session:
- Unresolved decisions
- Recent state changes (last 3 turns)
- Pending actions

### 2.6 Provider Adapter
Formats the final Context Pack for the specific target LLM (e.g., Anthropic Claude, OpenAI GPT), handling token limits and system prompt structures.

### 2.7 Governance Layer (Lakshmi Hook)
Evaluates the compiled Context Pack before LLM execution to ensure it meets the `Score ≤ 55` threshold defined in ADR-0033.

## 3. Context Modes

### MODE-B: Context Pack Only
- **Trigger:** Default production mode for standard execution (e.g., code generation, standard reporting).
- **Routing:** Selected when Governance Risk is Low (< 20) and no constitutional elements are touched.
- **Token Budget:** ~500-800 tokens.
- **Governance:** Fast-path approval.

### MODE-D: Context Pack + Canonical Memory
- **Trigger:** Missions involving architectural decisions, governance reviews, or policy changes.
- **Routing:** Selected when Capability = `architecture`, `governance`, or `strategy`.
- **Token Budget:** ~1,000-1,500 tokens.
- **Governance:** Requires full Lakshmi review.

### MODE-E: Context Pack + Canonical Memory + Session Delta
- **Trigger:** Complex multi-step reasoning tasks requiring immediate prior context.
- **Routing:** Selected when the worker explicitly requests clarification or when a task spans multiple sequential LLM calls.
- **Token Budget:** ~1,200-1,800 tokens.
- **Governance:** Elevated risk; monitor for hallucination.

## 4. Session Delta Architecture

Raw session history is banned in production. The Session Delta schema captures only actionable state:

```yaml
session_delta:
  mission_id: MISS-011
  current_step: 4
  unresolved_decisions:
    - "Select database schema for artifact storage"
  recent_state_changes:
    - "Worker Brahma generated Architecture Draft v1"
  pending_actions:
    - "Review Draft v1 against Constitution Article I"
  temporary_context:
    user_preference: "Use PostgreSQL syntax"
```

## 5. Obsidian / Git Architecture

The future Canonical Memory transitions to a Git-backed Obsidian vault.

### 5.1 Folder Structure
```text
/y-os-vault
  /00_Constitution
  /01_ADRs
  /02_Artifact_Registry
  /03_Missions
  /04_Governance
```

### 5.2 Artifact Lifecycle
1. Worker generates Markdown file in `/03_Missions`.
2. Y-ORC updates YAML frontmatter (status, lineage).
3. File is committed to Git.
4. Obsidian indexes the file for local search and visualization.

## 6. Migration Plan

### Phase 1: Parallel Operation (Current)
- Notion remains the primary Artifact Registry.
- Git mirrors all Notion changes via a sync script.
- CCR reads from Git.

### Phase 2: Obsidian-First (Next 30 Days)
- Git becomes the primary Artifact Registry.
- Workers write directly to Markdown files.
- Obsidian is used for human oversight and graph visualization.
- Notion is used only for external publishing (read-only).

### Phase 3: Notion Optional (Long Term)
- Full deprecation of Notion as a required dependency.
- All Y-OS state lives in the Git repository.

## 7. CEO Recommendation

**What should be implemented next week?**
- Implement the Context Router to dynamically switch between MODE-B and MODE-D.
- Implement the Session Delta Layer to formally kill raw session history.

**What should wait?**
- Phase 2 Obsidian migration. Keep Notion running while stabilizing CCR v2.

**What should be removed?**
- MODE-A (Session History Only) and MODE-F (Full Hybrid). They are mathematically proven to reduce quality and ROI.

**Decision:** ADOPT CCR Runtime v2 Architecture.
