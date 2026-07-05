# SOURCE-ID-NORMALIZATION-POLICY

> Y-OS / KAP Cognitive Architecture
> Gate: SOURCE-FRAGMENT-ID-NORMALIZATION-PATCH
> Date: 2026-07-03

---

## 1. Purpose
This policy normalizes identifiers across the validated KAP source architecture (L0→L3) to ensure stability before metadata and extraction pilots begin. It removes ambiguous symbolic IDs, preserves them as legacy aliases, and establishes strict rules for assigning canonical IDs without collision.

## 2. Four-Level Taxonomy Definitions
- **L0 Source Channel**: Access family / connector class (e.g., Git, Obsidian, Notion, ChatGPT).
- **L1 Source Instance**: Concrete container under a channel (e.g., one Git repo, one Obsidian vault).
- **L2 Source Object**: Internal object inside a source instance (e.g., file, folder, commit, Notion page).
- **L3 Source Fragment**: Bounded traceable cognitive unit created from a Source Object only after approved intake.

## 3. Canonical ID Formats

### 3.1 L0 — Source Channel ID
- **Format**: `CH-XXX`
- **Example**: `CH-001` (Git / GitHub), `CH-002` (ChatGPT)
- **Rule**: Do not renumber existing channels unless there is a duplicate or error.

### 3.2 L1 — Source Instance ID
- **Format**: `<CHANNELCODE>-XXX`
- **Example**: `GIT-001`, `GPT-001`, `MAN-001`
- **Rule**: Instance IDs identify concrete containers and remain stable even if names, paths, or URLs change.

### 3.3 L2 — Source Object ID
- **Format**: `SO-<CHANNELCODE>-<INSTANCESEQ>-<OBJECTSEQ>`
- **Example**: `SO-GIT-001-0001`
- **Rule**: Assigned during metadata scan or pre-registration. Does not imply content ingestion or fragment existence. Must link to exactly one Source Instance. Preserves path/title/URL as mutable metadata, not as identity.

### 3.4 L3 — Source Fragment ID
- **Format**: `SF-<CHANNELCODE>-<INSTANCESEQ>-<OBJECTSEQ>-<FRAGMENTSEQ>`
- **Example**: `SF-GIT-001-0001-001`
- **Rule**: Created only after approved intake. Must link to exactly one Source Object. A Source Object may generate many Source Fragments. IDs are stable and must not be reused. Superseded fragments are not deleted.

## 4. Legacy ID Preservation
Existing IDs (e.g., `FRAG-20260703-CP01`, `SF-001`) must not be deleted. They must be preserved as:
- `legacy_fragment_id`
- `legacy_alias`
- `previous_id`

A crosswalk mapping (`legacy_id` → `canonical_id`) is maintained in `SOURCE-FRAGMENT-ID-CROSSWALK.md`.

## 5. ID Assignment Rules & Collision Prevention
1. **Sequential Assignment**: `OBJECTSEQ` and `FRAGMENTSEQ` are sequentially assigned within their parent scope (Instance and Object, respectively).
2. **Central Registry**: `SOURCE-OBJECT-REGISTRY.md` and `SOURCE-FRAGMENT-REGISTRY.md` act as the single source of truth for the next available sequence number.
3. **No ID Reuse**: Once assigned, an ID is never reassigned, even if the underlying object/fragment is deleted or superseded.

## 6. ID Stability & Path/Title/URL Changes
- **Immutable Identity**: IDs (L0→L3) are immutable.
- **Mutable Metadata**: Changes to a file's path, a page's title, or a site's URL are recorded as metadata updates on the corresponding Source Object. The `SO-*` and `SF-*` IDs do not change.

## 7. Relationship to Source Fragment Model
This policy enforces the `fragment_id` format defined in `SOURCE-FRAGMENT-MODEL.md` and `source_fragment.schema.json`. It guarantees that every fragment can be deterministically traced back to its Source Object and Source Instance.

## 8. Relationship to KAP Source Matrix
The KAP Source Matrix tracks readiness at the L0 (Channel) and L1 (Instance) levels. This policy ensures that when pipelines move to L2 (Metadata Scan) and L3 (Content Extraction), the generated IDs are universally understood and structurally sound.

## 9. Examples
- A Markdown file in the `yos-cognitive-os` repo:
  - L0: `CH-001` (Git)
  - L1: `GIT-001` (yos-cognitive-os repo)
  - L2: `SO-GIT-001-0004` (The file `README.md`)
  - L3: `SF-GIT-001-0004-001` (A specific extracted section from `README.md`)

## 10. Open Questions
- How to handle ID assignment for highly dynamic sources (e.g., fast-moving chat channels) if they are ever brought into scope? (Deferred for Phase 2).
