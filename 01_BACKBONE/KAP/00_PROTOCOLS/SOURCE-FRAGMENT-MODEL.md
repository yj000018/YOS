# Source Fragment Model

> Y-OS / KAP Cognitive Architecture
> Gate: SOURCE-FRAGMENT-MODEL-GATE
> Status: ACTIVE

---

## 1. Definition

A **Source Fragment** is a traceable, bounded unit of source material preserved with provenance, timestamps, source-system metadata, extraction context, and future linkage capacity. 

It is the smallest traceable source unit that YOS/KAP may later ingest, classify, link, score, review, and eventually use as evidence.

## 2. Purpose

The Source Fragment Model prevents premature synthesis. By separating the *capture of raw evidence* from the *synthesis of knowledge*, YOS/KAP can evolve its understanding without destroying historical context, rationale, or original provenance.

## 3. What is / is not a Source Fragment

**A Source Fragment MAY BE:**
- Notion page or database row
- Manus report, MPM, or durable output
- ChatGPT session capture pack or conversation segment
- Obsidian note or Markdown file
- Git commit or Git file
- Gate report, registry entry, or architecture decision record
- Uploaded report or web reference
- Google Drive document or Mem0 memory item
- Tool output

**A Source Fragment IS NOT:**
- Canonical synthesis
- Final truth
- Deduplicated conclusion
- Merged knowledge
- Current-best understanding
- A claim automatically treated as true
- A decision automatically treated as active

## 4. Field Model

Every Source Fragment must preserve the following metadata:

- `fragment_id`: Unique identifier (e.g., `FRAG-20260703-ABCD`)
- `fragment_title`: Human-readable title
- `source_system`: Origin system
- `source_type`: Format of the source
- `source_subtype`: Specific format variation
- `source_path_or_url`: Location in the origin system
- `source_repo`: Git repo (if applicable)
- `source_branch`: Git branch (if applicable)
- `source_commit`: Git commit (if applicable)
- `source_created_at`: Original creation timestamp
- `source_modified_at`: Original modification timestamp
- `source_observed_at`: When KAP observed the fragment
- `extracted_at`: When KAP extracted the fragment
- `captured_by`: Agent or user who captured it
- `capture_method`: Pipeline or tool used
- `content_boundary`: Scope of extraction (e.g., full, snippet, metadata_only)
- `content_hash`: Cryptographic hash of the content for deduplication
- `language`: Primary language
- `project_scope`: Associated project (if known)
- `domain_tags`: Array of thematic tags
- `candidate_thought_lines`: Array of thought lines this fragment might belong to
- `candidate_claims`: Array of claims this fragment might support
- `candidate_decisions`: Array of decisions this fragment might inform
- `candidate_impasses`: Array of impasses this fragment might document
- `maturity_hint`: Expected maturity level
- `authority_hint`: Expected authority level
- `provenance_confidence`: Confidence in the source's origin
- `sensitivity_level`: Privacy/security flag
- `canonical_status`: Status within the YOS control plane
- `review_status`: Human/AI review state
- `merge_status`: Integration state
- `supersession_status`: Temporal validity state
- `related_fragments`: Array of linked fragment IDs
- `notes`: Operational notes

## 5. Controlled Vocabularies

### 5.1 `source_system`
`ChatGPT`, `Manus`, `Notion`, `Obsidian`, `Markdown`, `Git`, `Google_Drive`, `Mem0`, `Web`, `Uploaded_File`, `Manual_Note`, `Unknown`

### 5.2 `source_type`
`conversation`, `session_capture_pack`, `mpm`, `gate_report`, `architecture_doc`, `decision_log`, `registry`, `notion_page`, `notion_database`, `obsidian_note`, `markdown_file`, `git_file`, `git_commit`, `web_reference`, `memory_item`, `tool_output`, `report`, `unknown`

### 5.3 `canonical_status`
`not_canonical`, `candidate_evidence`, `active_control_plane`, `historical_source`, `implementation_evidence`, `superseded_source`, `requires_review`

### 5.4 `review_status`
`unreviewed`, `metadata_reviewed`, `content_reviewed`, `approved_for_claim_extraction`, `approved_for_decision_threading`, `rejected`, `needs_human_review`

### 5.5 `merge_status`
`not_merged`, `staged`, `linked_to_claim`, `linked_to_thought_line`, `linked_to_decision_thread`, `linked_to_impasse`, `merged_into_synthesis`, `merge_blocked`

### 5.6 `supersession_status`
`unknown`, `active`, `historical`, `superseded`, `supersedes_other`, `contradicted`, `needs_supersession_review`

### 5.7 `maturity_hint`
`raw`, `rough_note`, `exploratory`, `proposal`, `validated_gate_output`, `implementation_evidence`, `active_doctrine`, `canonical_candidate`, `deprecated`, `unknown`

### 5.8 `authority_hint`
`user_directive`, `guardian_architect_decision`, `manus_execution_report`, `git_commit_evidence`, `source_document`, `memory_hint`, `external_reference`, `unknown`

### 5.9 `provenance_confidence`
`high`, `medium`, `low`, `unknown`

### 5.10 `sensitivity_level`
`public`, `internal`, `private`, `sensitive`, `secret_reference_only`, `unknown` *(Note: Secrets themselves must never be stored in a Source Fragment).*

## 6. Lifecycle

1. `discovered`: Fragment identified but not yet processed.
2. `registered`: ID assigned, basic metadata captured.
3. `metadata_captured`: Full metadata available.
4. `content_captured`: Full content available.
5. `reviewed`: Assessed by AI or Human.
6. `linked`: Connected to other fragments or entities.
7. `claim_extraction_ready`: Approved for claim generation.
8. `decision_thread_ready`: Approved for decision threading.
9. `synthesis_ready`: Approved for current-best synthesis.
10. `archived_or_superseded`: Replaced or no longer active (but history preserved).

## 7. Relationship Model

How Source Fragments connect to the broader cognitive architecture:

| Relationship | Cardinality | Rule |
|---|---|---|
| Fragment ↔ Claim | **N:N** | One fragment may support many claims; one claim may be supported by many fragments |
| Fragment ↔ Thought Line | N:N | One fragment may belong to several candidate thought lines |
| Fragment → Decision | N:N | One fragment may provide implementation evidence for a decision |
| Fragment → Impasse | N:N | One fragment may document an impasse |
| Synthesis → Fragment | N:N | Synthesis must point back to source fragments |

**Immutability rules:**
- One fragment must never be erased by synthesis.
- Fragments may contradict each other without either being deleted.
- Source chronology must be preserved.
- Later fragments are not automatically more correct.

## 8. Human Review Implications

Fragments must remain human-readable (Markdown format for text, JSON for metadata) to allow the Guardian Architect or user to audit the exact source material that led to a specific claim or decision.

## 9. AI Retrieval Implications

AI agents will use the JSON schema and `source_fragment_index.json` to filter fragments by `project_scope`, `domain_tags`, `canonical_status`, and `supersession_status` before attempting to generate current-best synthesis. This prevents hallucinations and enforces evidence-based reasoning.

## 10. Examples

See `SOURCE-FRAGMENT-EXAMPLES.md`.

## 11. Validation Rules

- Extraction is forbidden if the source system is not in the controlled vocabulary.
- Fragments must have a `content_hash` to detect duplicates.
- Timestamps must be preserved; if original creation time is unknown, `source_observed_at` must be used.

## 12. Open Questions

- How granular should a ChatGPT conversation fragment be? (Per prompt/response, per session, or per project pack?)
- Should large Git commits be split into multiple fragments per file?
