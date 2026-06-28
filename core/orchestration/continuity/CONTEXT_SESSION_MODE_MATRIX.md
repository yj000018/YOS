# Context / Session Mode Matrix

This document defines the canonical mode fields and the resolution system for yOS Context Continuity.

## 1. Required Mode Fields

The following fields define the exact continuity mode for any given task or session:

| Field | Allowed Values |
|---|---|
| `session_mode` | `same_session`, `stateless_context_pack_only`, `context_pack_plus_short_session`, `canonical_memory_plus_context_pack`, `canonical_memory_plus_context_pack_plus_short_session` |
| `canonical_memory_mode` | `none`, `on_demand`, `required`, `auto_if_high_risk` |
| `context_pack_depth` | `none`, `minimal` (T0 Nano), `standard` (T1 Standard), `full_lineage` (T2 Full Lineage), `emergency_recovery` (T3 Emergency Recovery) |
| `session_continuity_mode` | `none`, `current_chat_context`, `previous_response_id`, `bounded_thread`, `human_curated_summary` |
| `handoff_mode` | `none`, `lightweight_handoff`, `standard_context_pack`, `governed_context_pack`, `recovery_context_pack` |
| `confirmation_policy` | `none`, `inform_only`, `ask_user`, `chief_architect_required`, `founder_required` |
| `enforcement_level` | `advisory`, `warning`, `blocking`, `hard_stop` |

## 2. Mode Resolution System

The continuity mode is resolved from four sources, in order of authority:

1. **Founder / User explicit instruction** (Overrides all generic defaults)
2. **Chief Architect / L3 approved workflow**
3. **Programmatic mission parameters** (Overrides generic defaults when provided by an approved workflow)
4. **yOS LLM & Tool Routing Matrix defaults**
5. **Manus proactive suggestion** (When prompt semantics imply a higher context need)
6. **Runtime fallback rules**

**Escalation Policy:**
* Manus may propose escalation when prompt semantics imply a higher context need.
* Manus may not silently escalate to costly/heavy canonical-memory modes unless the matrix explicitly allows auto-escalation for that task class.
* Chief Architect or Founder confirmation is required for major mode escalation.

## 3. Routing Matrix Integration

The continuity behavior must be defined as defaults within the canonical `YOS/core/orchestration/registries/LLM_AND_TOOL_ROUTING_MATRIX.md`.

**Required continuity-related fields in the Routing Matrix:**
* `default_session_mode`
* `default_canonical_memory_mode`
* `default_context_pack_depth`
* `default_session_continuity_mode`
* `default_handoff_mode`
* `default_confirmation_policy`
* `default_enforcement_level`
* `auto_escalation_allowed`
* `escalation_triggers`
* `user_confirmation_required_when`
* `chief_architect_required_when`
* `founder_required_when`

*Note: Adaptive templates by `task_class` are supported within the Routing Matrix to optimize context pack generation.*
