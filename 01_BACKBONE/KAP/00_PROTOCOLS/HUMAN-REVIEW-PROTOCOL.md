# HUMAN-REVIEW-PROTOCOL

> Y-OS / KAP Cognitive Architecture
> Gate: PROCESS-DOCS-RUNBOOK-GATE
> Last Updated: 2026-07-03

## 1. Mandatory Guardian Architect Review

Manus MUST halt execution and request Guardian Architect review when:
1. Attempting to transition between major Gates (e.g., from Metadata Pilot to Content Pilot).
2. A contradiction is detected between two `active_doctrine` Claims.
3. Reconstructing a Decision Thread that alters the fundamental YOS/KAP architecture.
4. Splitting or merging existing Thought Lines.
5. Generating a Current Best Synthesis.

## 2. Mandatory User Review

Manus MUST halt execution and request explicit User review when:
1. A Source Object contains potentially sensitive personal, financial, or security-related information.
2. A deletion operation is required (per `Deletion Confirmation Policy`).
3. Source Instance mapping is ambiguous and requires human clarification.

## 3. Red Flags (Stop Execution Immediately)

If Manus encounters any of the following, it must stop and log a blocker:
- **Unclear Provenance:** A Claim cannot be traced to a specific Source Fragment.
- **LLM Internal Knowledge Used as Evidence:** An LLM's memory is cited as the primary source instead of a verifiable document.
- **Mem0 Used as Source Authority:** Mem0 is used for facts rather than as a signal/routing aid.
- **Generated Site/App Without Code Provenance:** Attempting to extract content from a generated site without first mapping it to its source code repository.
- **Unsupported Active Decision:** A Decision Thread is marked `active` but lacks supporting Claims.
- **Missing Source Object/Fragment:** A registry entry references an ID that does not exist.

## 4. Review Statuses

When an item is flagged for review, its status should be updated to `requires_review`. Upon completion, the reviewer will update the status to `approved`, `rejected`, or `needs_revision`.

## 5. Escalation Rules

If Manus is unsure whether a situation requires review, it must default to halting execution and requesting Guardian Architect guidance. It is always better to pause for clarification than to proceed with ambiguous or potentially destructive actions.

## 6. Minimal Review Checklist

Before approving an item, the reviewer should verify:
- [ ] Provenance is clear and traceable to L0.
- [ ] No unauthorized synthesis has occurred.
- [ ] No internal LLM knowledge is treated as canonical truth.
- [ ] Git/Markdown persistence is maintained.
