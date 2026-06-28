# Continuity Decision Flow

This document outlines the decision tree for resolving context continuity modes and details the proactive escalation triggers for Manus.

## 1. Core Decision Tree

The following flow determines the appropriate continuity mechanism for a given task:

1. **Is there an explicit Founder/User instruction?**
   * **Yes:** Override defaults and follow instruction.
   * **No:** Proceed to step 2.
2. **Is this a Chief Architect or L3 approved workflow?**
   * **Yes:** Apply the workflow's defined programmatic parameters.
   * **No:** Proceed to step 3.
3. **Does the task cross a boundary (LLM, tool, agent, session, phase)?**
   * **Yes:** A Context Pack is **mandatory**. Determine depth based on task class.
   * **No:** Proceed to step 4.
4. **Is the task governance-heavy, canonical, or a full-project recovery?**
   * **Yes:** `canonical_memory_mode` is `required`. A full lineage Context Pack (T2) may be necessary.
   * **No:** Proceed to step 5.
5. **Is the task a bounded, local continuation of the current thread?**
   * **Yes:** Local session continuity or `previous_response_id` may be used.
   * **No:** Apply the default mode from the yOS LLM & Tool Routing Matrix.

## 2. Proactive Manus Escalation

Manus must detect implicit context needs based on prompt semantics and propose mode escalations.

### 2.1 Escalation Triggers

Manus should suggest escalation when encountering phrases such as:

* “reprenons tout le projet depuis le début”
* “base-toi sur tout le projet”
* “reprends depuis le début”
* “audit complet”
* “gate final”
* “décision canonique”
* “avant de continuer, vérifie tout”
* “compare avec toutes les décisions précédentes”
* “ne rate rien”
* “architecture globale”
* “programme entier”
* “mémoire du projet”
* “transmets à Claude / ChatGPT API / Manus”
* “handoff”
* “nouvelle session”
* “reprise après interruption”

### 2.2 Escalation Example

**User Prompt:** “reprenons tout le projet depuis le début”

**Detected Intent:** Full project recovery / canonical recap

**Suggested Mode:**
* `canonical_memory_mode`: `required`
* `context_pack_depth`: `full_lineage`
* `session_mode`: `canonical_memory_plus_context_pack`
* `confirmation_policy`: `ask_user`

**Manus Response Protocol:**
"This request implies full canonical recovery. I recommend `canonical_memory_mode=required` and `context_pack_depth=full_lineage` before execution. Please confirm."

## 3. Pack Preview Policy

Before injecting a heavy, complex, or costly Context Pack (e.g., T2 Full Lineage), Manus must provide a pack preview to the user. This ensures the injected context is accurate and not stale, allowing the Founder to confirm or abort the injection.
