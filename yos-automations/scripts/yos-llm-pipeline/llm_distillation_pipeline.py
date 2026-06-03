#!/usr/bin/env python3.11
"""
LLM Chat Export → Knowledge Distillation Pipeline
===================================================
Version: 1.3
Architecture: 9-layer Knowledge OS (Add6 — Full Spec)

Layer 1 — Ingestion      : Chat_Export_Sessions (via chatgpt2notion extension)
Layer 2 — Distillation   : Sessions → Knowledge items (LLM)
Layer 3 — Merge Logic    : Canonical Keys + 6-case conservative merge
Layer 3.5 — Signal Scoring : Importance + Confidence + Freshness per item
Layer 4 — Concept Groups : Concept_Clusters (active when Knowledge > 150 items)
Layer 5 — Graph Layer    : Typed relations between Knowledge items
Layer 6 — Working Memory : Active_Context (context_builder — always active)
Layer 7 — Synthesis      : Project_Synthesis (synthesis_engine — manual trigger)
Layer 8 — Embeddings     : Semantic similarity (active when Knowledge > 3000 items)

Merge cases (Appendix v1.1):
  A. Exact/near duplicate (sim ≥ 0.72)  → merge evidence, update Last_Seen
  B. Reformulation (sim 0.45–0.72)      → merge, optionally improve wording
  C. Meaningful extension (sim 0.45–0.72) → update existing item
  D. Replacement decision               → create new, mark old superseded
  E. Contradiction                      → create Open_Question, Conflict_Flag=true
  F. Low-value repetition (<30 chars)   → ignore

Operational Rules (Addendum 2):
  append first, merge carefully, rewrite rarely
  Preserve history. Never silently overwrite. Maintain traceability.

Canonical Key Strategy (Addendum 3):
  domain_object_action format. First filter before semantic comparison.

Concept Clusters (Addendum 4): active when CLUSTERS_ENABLED=true in config.
Graph Layer (Addendum 5): active when GRAPH_ENABLED=true in config.

Schedule: Daily at 05:00 (2h after chatgpt2notion Auto-Sync at 03:00)

Usage:
    python3.11 llm_distillation_pipeline.py [--dry-run] [--force-all]
"""

import os
import sys
import json
import subprocess
import argparse
import logging
import re
from datetime import datetime, timezone
from typing import Optional

# ─── Load Configuration ────────────────────────────────────────────────────────

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "yos_config.json")

def load_config() -> dict:
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {}

CFG = load_config()

def cfg(path: str, default=None):
    """Dot-path config accessor. e.g. cfg('llm.model')"""
    parts = path.split(".")
    node = CFG
    for p in parts:
        if isinstance(node, dict):
            node = node.get(p, default)
        else:
            return default
    return node if node is not None else default

# ─── Configuration ─────────────────────────────────────────────────────────────

PIPELINE_NAME        = cfg("pipeline.pipeline_name", "llm_ingestion")
DB_CHAT_SESSIONS_DS  = cfg("notion.databases.chat_sessions.data_source_id",
                            "13633cbd-7c08-475e-b610-a5377fbdfa91")
DB_KNOWLEDGE_DS      = cfg("notion.databases.knowledge.data_source_id",
                            "1895910b-b8d4-4773-85b6-300d01a8d53d")
DB_PIPELINE_STATE_DS = cfg("notion.databases.pipeline_state.data_source_id",
                            "cb53fe34-b848-4375-aa90-6a74db18375b")
DB_CLUSTERS_DS       = cfg("notion.databases.concept_clusters.data_source_id", "")
DB_ACTIVE_CONTEXT_DS = cfg("notion.databases.active_context.data_source_id",
                            "17a975d7-4d8e-489e-a859-43ca872d7c5b")

OPENAI_API_KEY  = os.environ.get("OPENAI_API_KEY", "")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE",
                  cfg("llm.api_base", "https://api.openai.com/v1"))
DISTILL_MODEL   = cfg("llm.model", "gpt-4o-mini")
MAX_CONTENT_CHARS = cfg("llm.max_content_chars", 12000)
LLM_TEMPERATURE   = cfg("llm.temperature", 0.2)
LLM_MAX_TOKENS    = cfg("llm.max_tokens", 2000)

SIM_DUPLICATE  = cfg("merge.similarity_threshold_duplicate", 0.72)
SIM_EXTENSION  = cfg("merge.similarity_threshold_extension", 0.45)
MIN_CONTENT_LEN = cfg("merge.min_content_length_chars", 30)

CLUSTERS_ENABLED        = cfg("features.clusters_enabled", False)
GRAPH_ENABLED           = cfg("features.graph_enabled", False)
CLUSTERS_THRESHOLD      = cfg("features.clusters_activation_threshold", 150)
CONTEXT_BUILDER_ENABLED = cfg("features.context_builder_enabled", True)
SYNTHESIS_ENABLED       = cfg("features.synthesis_engine_enabled", False)
SIGNAL_SCORING_ENABLED  = cfg("features.signal_scoring_enabled", True)

LOG_FILE = os.path.join(os.path.dirname(__file__), cfg("pipeline.log_file", "pipeline.log"))

# ─── Logging ──────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ]
)
log = logging.getLogger("pipeline")

# ─── MCP Helpers ──────────────────────────────────────────────────────────────

def mcp_call(tool: str, input_data: dict) -> dict:
    cmd = [
        "manus-mcp-cli", "tool", "call", tool,
        "--server", "notion",
        "--input", json.dumps(input_data),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        raise RuntimeError(f"MCP call failed [{tool}]: {result.stderr.strip()}")
    output = result.stdout.strip()
    if "Tool execution result:" in output:
        json_part = output.split("Tool execution result:\n", 1)[-1].strip()
    else:
        json_part = output
    try:
        return json.loads(json_part)
    except json.JSONDecodeError:
        return {"raw": json_part}


def notion_search_db(data_source_id: str, query: str = "knowledge", filters: dict = None) -> list:
    payload = {
        "query": query or "knowledge",
        "query_type": "internal",
        "data_source_url": f"collection://{data_source_id}",
    }
    if filters:
        payload["filters"] = filters
    result = mcp_call("notion-search", payload)
    return result.get("results", [])


def notion_fetch(url_or_id: str) -> dict:
    return mcp_call("notion-fetch", {"id": url_or_id})


def notion_create_page(data_source_id: str, properties: dict, content: str = "") -> dict:
    page_obj = {"properties": properties}
    if content:
        page_obj["content"] = content
    return mcp_call("notion-create-pages", {
        "parent": {"data_source_id": data_source_id},
        "pages": [page_obj],
    })


def notion_update_page(page_url: str, properties: dict) -> dict:
    return mcp_call("notion-update-page", {
        "id": page_url,
        "properties": properties,
    })

# ─── Pipeline State ───────────────────────────────────────────────────────────

def get_pipeline_state() -> dict:
    results = notion_search_db(DB_PIPELINE_STATE_DS, query=PIPELINE_NAME)
    for r in results:
        if r.get("title", "").strip() == PIPELINE_NAME:
            return r
    raise RuntimeError(f"Pipeline_State row '{PIPELINE_NAME}' not found.")


def update_pipeline_state(page_url: str, last_processed: Optional[str],
                           status: str, notes: str, count: int, dry_run: bool):
    if dry_run:
        log.info(f"[DRY-RUN] Would update Pipeline_State: status={status}, count={count}")
        return
    props = {
        "Last_Run_Status": status,
        "Last_Run_Notes": notes,
        "Processed_Count": count,
    }
    if last_processed:
        props["date:Last_Processed:start"] = last_processed
        props["date:Last_Processed:is_datetime"] = 1
    notion_update_page(page_url, props)
    log.info(f"Pipeline_State updated: {status} | {count} sessions | last_processed={last_processed}")

# ─── Session Fetching ─────────────────────────────────────────────────────────

def get_new_sessions(last_processed: Optional[str], force_all: bool) -> list:
    log.info(f"Fetching sessions (last_processed={last_processed}, force_all={force_all})")
    filters = {}
    if last_processed and not force_all:
        if len(last_processed) >= 10 and last_processed[4] == "-":
            filters["created_date_range"] = {"start_date": last_processed}
    results = notion_search_db(DB_CHAT_SESSIONS_DS, query="session",
                               filters=filters if filters else None)
    log.info(f"Found {len(results)} candidate sessions.")
    return results

# ─── LLM System Prompt ────────────────────────────────────────────────────────

DISTILL_SYSTEM_PROMPT = """You are a knowledge distillation engine for Y-OS, a personal cognitive operating system.

ROLE: careful research assistant, not a creative writer.
PRIORITY: preserve existing knowledge > add evidence carefully > merge conservatively > rewrite rarely.
RULE: append first, merge carefully, rewrite rarely.

OPERATIONAL RULES (mandatory):
1. Never rewrite entire project syntheses — update only affected sections.
2. Avoid knowledge duplication — always check for similar existing items first.
3. Preserve historical decisions — never overwrite; mark old as superseded, create new.
4. Distinguish: Idea (exploratory) vs Hypothesis (tentative) vs Decision (confirmed) vs Action_Item (concrete task) vs Issue (known problem). Do not label speculation as a decision.
5. Prefer fewer, stronger knowledge items — merge multiple small items representing the same concept.
6. Do not assume newer information is better — only replace if it clearly contradicts and supersedes.
7. Ignore low-value repetition — only create items if content provides new insight, decision, issue, action, or meaningful clarification.
8. Handle conflicts explicitly — create Open_Question with Conflict_Flag=true, never silently merge contradictory information.
9. Maintain traceability — every item must link back to source sessions.
10. Prefer stability over creativity — precise statements, minimal wording changes, incremental updates.

CANONICAL KEY RULES:
- Every knowledge item MUST have a canonical_key.
- Format: domain_object_action (lowercase, underscores, max 5 tokens).
- Good: knowledge_merge_conservative | pipeline_state_storage_notion | ingestion_batch_interval
- Bad: we_should_merge_items_conservatively_to_avoid_duplication
- The canonical_key is the primary deduplication identifier. It must represent the core concept, not the phrasing.

ITEM TYPES: Insight | Decision | Action_Item | Issue | Open_Question | Hypothesis | Principle | Idea | Constraint | Resource | Next_Step | Summary_Block

PROJECTS: yOS | CasaTAO | OneOS-Home Stack | AI Workflows | Notion-Memory | Manus Orchestration | Personal Knowledge System | Hardware Infra | Creative-TouchDesigner | Unknown

SUBPROJECTS: Memory architecture | Model routing | Distillation pipeline | Server automation | Notion sync | Home assistant integration | null

Analyze the raw LLM chat session and extract structured knowledge items.

Output a JSON object with this EXACT structure (no markdown, no explanation, valid JSON only):
{
  "language": "FR|EN|IT|Mixed",
  "keywords": ["keyword1", "keyword2"],
  "project": "<one of the projects above>",
  "subproject": "<one of the subprojects above or null>",
  "short_summary": "2-3 sentence summary of the session",
  "quality_flag": "clean|partial|noisy",
  "knowledge_items": [
    {
      "title": "Short clear title (max 10 words)",
      "canonical_key": "domain_object_action",
      "item_type": "<one of the item types above>",
      "content": "Full distilled content — precise, minimal wording, no speculation",
      "short_summary": "One sentence summary",
      "status": "open|active|resolved",
      "priority": "low|medium|high|critical",
      "confidence": "low|medium|high",
      "importance": "critical|high|medium|low",
      "confidence": "confirmed|likely|uncertain",
      "graph_hints": {
        "parent_concept": "canonical_key of broader concept if obvious, else null",
        "supports": "canonical_key of item this reinforces, else null",
        "contradicts": "canonical_key of item this conflicts with, else null"
      }
    }
  ]
}
"""

# ─── LLM Call ─────────────────────────────────────────────────────────────────

def call_llm(session_content: str, session_title: str) -> Optional[dict]:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)
        truncated = session_content[:MAX_CONTENT_CHARS]
        user_msg = f"Session title: {session_title}\n\nSession content:\n{truncated}"
        response = client.chat.completions.create(
            model=DISTILL_MODEL,
            messages=[
                {"role": "system", "content": DISTILL_SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS,
        )
        raw = response.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1]
            raw = raw.rsplit("```", 1)[0]
        return json.loads(raw)
    except Exception as e:
        log.error(f"LLM call failed: {e}")
        return None

# ─── Canonical Key & Similarity ───────────────────────────────────────────────

def normalize_key(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9\s_]', '', text)
    text = re.sub(r'[\s]+', '_', text)
    return text[:80]


def canonical_key_similarity(key_a: str, key_b: str) -> float:
    """Token overlap on canonical key tokens (split by underscore)."""
    if not key_a or not key_b:
        return 0.0
    tokens_a = set(key_a.lower().split("_"))
    tokens_b = set(key_b.lower().split("_"))
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = tokens_a & tokens_b
    union = tokens_a | tokens_b
    return len(intersection) / len(union)


def text_similarity(a: str, b: str) -> float:
    """Jaccard token overlap on word tokens."""
    if not a or not b:
        return 0.0
    tokens_a = set(a.lower().split())
    tokens_b = set(b.lower().split())
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = tokens_a & tokens_b
    union = tokens_a | tokens_b
    return len(intersection) / len(union)


def combined_similarity(candidate: dict, result: dict) -> float:
    """
    Combined similarity score using canonical key (primary), title, and content.
    Canonical key is the first filter per Addendum 3.
    """
    r_title = result.get("title", "")
    r_highlight = result.get("highlight", "")
    r_canonical = normalize_key(r_title)

    # Primary: canonical key similarity
    key_sim = canonical_key_similarity(
        candidate.get("canonical_key", ""),
        r_canonical
    )
    # Secondary: title similarity
    title_sim = text_similarity(candidate.get("title", ""), r_title)
    # Tertiary: content overlap
    content_sim = text_similarity(candidate.get("content", ""), r_highlight)

    # Canonical key is the primary signal
    return max(key_sim * 1.0, title_sim * 0.85, content_sim * 0.6)

# ─── Knowledge Search ─────────────────────────────────────────────────────────

def find_similar_knowledge_items(candidate: dict, project: str) -> list:
    """
    Search Knowledge database for items similar to the candidate.
    Uses canonical key as primary search vector (Addendum 3).
    Returns list sorted by similarity descending.
    """
    # Use canonical key as primary search query
    canonical = candidate.get("canonical_key", "")
    search_query = canonical.replace("_", " ")[:100] if canonical else candidate.get("title", "")[:100]

    try:
        results = notion_search_db(DB_KNOWLEDGE_DS, query=search_query)
    except Exception as e:
        log.warning(f"Knowledge search failed: {e}")
        return []

    scored = []
    for r in results:
        sim = combined_similarity(candidate, r)
        if sim >= 0.25:
            scored.append({"result": r, "similarity": sim})

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored

# ─── Merge Decision Tree ──────────────────────────────────────────────────────

def apply_merge_decision(candidate: dict, similar_items: list,
                          project: str, today_iso: str, dry_run: bool) -> str:
    """
    Apply the 6-case merge decision tree (Appendix v1.1 + Addendum 2).
    Returns: 'created' | 'merged' | 'updated' | 'superseded' | 'conflict' | 'ignored'
    """
    # Case F: Low-value repetition
    if len(candidate.get("content", "")) < MIN_CONTENT_LEN:
        log.info(f"    [F-ignore] Too short/weak: {candidate.get('title')}")
        return "ignored"

    if not similar_items:
        log.info(f"    [new] No similar item found → creating")
        return _create_knowledge_item(candidate, project, today_iso, dry_run, merge_status="new")

    best = similar_items[0]
    sim = best["similarity"]
    existing_url = best["result"].get("url", "")
    existing_title = best["result"].get("title", "")

    log.info(f"    Best match: '{existing_title}' (sim={sim:.2f})")

    # Case A: Exact / near duplicate
    if sim >= SIM_DUPLICATE:
        log.info(f"    [A-merge] Near duplicate → merging evidence")
        if not dry_run:
            _merge_evidence(existing_url, today_iso)
        return "merged"

    # Cases B/C/D: Moderate similarity
    if sim >= SIM_EXTENSION:
        candidate_type = candidate.get("item_type", "")

        # Case D: Replacement decision
        if candidate_type == "Decision":
            existing_highlight = best["result"].get("highlight", "").lower()
            if "decision" in existing_highlight or "decided" in existing_highlight:
                log.info(f"    [D-supersede] New decision replaces old")
                if not dry_run:
                    _supersede_item(existing_url, candidate, project, today_iso)
                return "superseded"

        # Case C: Meaningful extension
        log.info(f"    [C-update] Meaningful extension → updating existing")
        if not dry_run:
            _update_existing_item(existing_url, candidate, today_iso)
        return "updated"

    # Case E: Contradiction detection
    candidate_type = candidate.get("item_type", "")
    if candidate_type in ("Decision", "Principle") and sim >= 0.25:
        candidate_content = candidate.get("content", "").lower()
        existing_highlight = best["result"].get("highlight", "").lower()
        negation_words = {"not", "never", "unnecessary", "avoid", "instead", "rather", "opposite", "no"}
        candidate_negated = bool(negation_words & set(candidate_content.split()))
        existing_negated = bool(negation_words & set(existing_highlight.split()))
        if candidate_negated != existing_negated:
            log.info(f"    [E-conflict] Contradiction detected → creating Open_Question")
            if not dry_run:
                _create_conflict_item(candidate, existing_url, project, today_iso)
            return "conflict"

    # Default: New meaningful concept
    log.info(f"    [new] Low similarity ({sim:.2f}) → creating new item")
    return _create_knowledge_item(candidate, project, today_iso, dry_run, merge_status="new")

# ─── Knowledge Item Operations ────────────────────────────────────────────────

VALID_PROJECTS = {
    "yOS", "CasaTAO", "OneOS-Home Stack", "AI Workflows",
    "Notion-Memory", "Manus Orchestration", "Personal Knowledge System",
    "Hardware Infra", "Creative-TouchDesigner"
}
VALID_SUBPROJECTS = {
    "Memory architecture", "Model routing", "Distillation pipeline",
    "Server automation", "Notion sync", "Home assistant integration"
}


def _create_knowledge_item(candidate: dict, project: str, today_iso: str,
                            dry_run: bool, merge_status: str = "new") -> str:
    props = {
        "Title": candidate.get("title", "Untitled")[:200],
        "Item_Type": candidate.get("item_type", "Insight"),
        "Content": candidate.get("content", "")[:2000],
        "Short_Summary": candidate.get("short_summary", "")[:500],
        "Status": candidate.get("status", "open"),
        "Priority": candidate.get("priority", "medium"),
        "Confidence": candidate.get("confidence", "medium"),
        "Canonical_Key": candidate.get("canonical_key", "")[:200],
        "Evidence_Count": 1,
        "Merge_Status": merge_status,
        "Validity": "active",
        "Conflict_Flag": "__NO__",
        "date:First_Seen:start": today_iso,
        "date:First_Seen:is_datetime": 0,
        "date:Last_Seen:start": today_iso,
        "date:Last_Seen:is_datetime": 0,
        "date:Last_AI_Update:start": today_iso,
        "date:Last_AI_Update:is_datetime": 0,
    }
    if project in VALID_PROJECTS:
        props["Project"] = project

    # Signal Scoring (Add6 — Layer 3.5)
    if SIGNAL_SCORING_ENABLED:
        importance = candidate.get("importance", "medium")
        if importance in ("critical", "high", "medium", "low"):
            props["Importance"] = importance

    if not dry_run:
        try:
            notion_create_page(DB_KNOWLEDGE_DS, props, content=candidate.get("content", ""))
            log.info(f"    → Created: [{candidate.get('item_type')}] {candidate.get('title')} [{candidate.get('canonical_key')}]")
        except Exception as e:
            log.error(f"    → Failed to create: {e}")
    else:
        log.info(f"    [DRY-RUN] Would create: [{candidate.get('item_type')}] {candidate.get('title')} [{candidate.get('canonical_key')}]")

    return "created"


def _merge_evidence(existing_url: str, today_iso: str):
    """Case A: Merge evidence — update Last_Seen, increment Evidence_Count."""
    try:
        full = notion_fetch(existing_url)
        text = full.get("text", "")
        count_match = re.search(r'"Evidence_Count"[^0-9]*([0-9]+)', text)
        current_count = int(count_match.group(1)) if count_match else 1
        notion_update_page(existing_url, {
            "date:Last_Seen:start": today_iso,
            "date:Last_Seen:is_datetime": 0,
            "date:Last_AI_Update:start": today_iso,
            "date:Last_AI_Update:is_datetime": 0,
            "Evidence_Count": current_count + 1,
            "Merge_Status": "merged",
        })
        log.info(f"    → Evidence merged (count: {current_count + 1})")
    except Exception as e:
        log.error(f"    → Merge failed: {e}")


def _update_existing_item(existing_url: str, candidate: dict, today_iso: str):
    """Case C: Update existing item with new content extension."""
    try:
        notion_update_page(existing_url, {
            "date:Last_Seen:start": today_iso,
            "date:Last_Seen:is_datetime": 0,
            "date:Last_AI_Update:start": today_iso,
            "date:Last_AI_Update:is_datetime": 0,
            "Merge_Status": "updated",
        })
        new_detail = candidate.get("content", "")
        if new_detail:
            mcp_call("notion-update-page", {
                "id": existing_url,
                "insert_content_after": f"\n\n**Update ({today_iso}):** {new_detail[:500]}",
            })
        log.info(f"    → Item updated with extension")
    except Exception as e:
        log.error(f"    → Update failed: {e}")


def _supersede_item(existing_url: str, candidate: dict, project: str, today_iso: str):
    """Case D: Mark old item superseded, create new item."""
    try:
        notion_update_page(existing_url, {
            "Validity": "superseded",
            "Merge_Status": "updated",
            "date:Last_AI_Update:start": today_iso,
            "date:Last_AI_Update:is_datetime": 0,
        })
        log.info(f"    → Old item marked as superseded")
    except Exception as e:
        log.error(f"    → Could not mark superseded: {e}")
    _create_knowledge_item(candidate, project, today_iso, dry_run=False, merge_status="new")


def _create_conflict_item(candidate: dict, conflicting_url: str, project: str, today_iso: str):
    """Case E: Create Open_Question to surface contradiction."""
    conflict_title = f"Conflict: {candidate.get('title', 'Unknown')[:150]}"
    conflict_content = (
        f"Contradiction detected.\n\n"
        f"New statement: {candidate.get('content', '')[:500]}\n\n"
        f"Conflicts with: {conflicting_url}"
    )
    props = {
        "Title": conflict_title[:200],
        "Item_Type": "Open_Question",
        "Content": conflict_content[:2000],
        "Short_Summary": f"Unresolved contradiction on: {candidate.get('title', '')}",
        "Status": "open",
        "Priority": "high",
        "Confidence": "low",
        "Conflict_Flag": "__YES__",
        "Merge_Status": "conflicted",
        "Validity": "active",
        "Canonical_Key": normalize_key(f"conflict_{candidate.get('canonical_key', conflict_title)}")[:200],
        "date:First_Seen:start": today_iso,
        "date:First_Seen:is_datetime": 0,
        "date:Last_Seen:start": today_iso,
        "date:Last_Seen:is_datetime": 0,
        "date:Last_AI_Update:start": today_iso,
        "date:Last_AI_Update:is_datetime": 0,
    }
    if project in VALID_PROJECTS:
        props["Project"] = project
    try:
        notion_create_page(DB_KNOWLEDGE_DS, props, content=conflict_content)
        log.info(f"    → Conflict item created: {conflict_title}")
    except Exception as e:
        log.error(f"    → Failed to create conflict item: {e}")

# ─── Context Builder (Layer 6 — Working Memory) ─────────────────────────────

def update_active_context(project: str, processed_count: int, dry_run: bool):
    """
    Refresh Active_Context (working memory) after pipeline run.
    Pulls top active decisions and open issues for the current project.
    Add6 — Layer 3.4.
    """
    if not CONTEXT_BUILDER_ENABLED or not DB_ACTIVE_CONTEXT_DS:
        return
    if dry_run:
        log.info("[DRY-RUN] Would update Active_Context")
        return

    today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    context_title = f"Active — {project} — {today_iso}"
    max_decisions = cfg("active_context.max_active_decisions", 10)
    max_issues    = cfg("active_context.max_active_issues", 10)

    # Fetch recent decisions and open issues from Knowledge
    try:
        decisions = notion_search_db(DB_KNOWLEDGE_DS, query="decision active")
        issues    = notion_search_db(DB_KNOWLEDGE_DS, query="issue open")

        decision_summary = "\n".join(
            f"- {r.get('title', '?')}" for r in decisions[:max_decisions]
        )
        issue_summary = "\n".join(
            f"- {r.get('title', '?')}" for r in issues[:max_issues]
        )

        notes = (
            f"Pipeline run: {today_iso} | Sessions processed: {processed_count}\n\n"
            f"Active Decisions:\n{decision_summary or 'None'}\n\n"
            f"Open Issues:\n{issue_summary or 'None'}"
        )

        props = {
            "Context": context_title[:200],
            "Project": project if project in VALID_PROJECTS else "yOS",
            "Reasoning_Notes": notes[:2000],
            "date:Last_Update:start": today_iso,
            "date:Last_Update:is_datetime": 0,
        }
        notion_create_page(DB_ACTIVE_CONTEXT_DS, props, content=notes)
        log.info(f"Active_Context updated: {context_title}")
    except Exception as e:
        log.warning(f"context_builder failed: {e}")


# ─── Synthesis Engine (Layer 7 — stub, manual trigger) ────────────────────────

def run_synthesis_engine(project: str, dry_run: bool):
    """
    Synthesis engine stub (Add6 — Layer 7).
    Updates only affected sections of project synthesis pages.
    Mapping: Decision→Active_Decisions, Issue→Active_Issues,
             Action_Item→Action_Items, Open_Question→Open_Questions,
             Constraint→Constraints, Next_Step→Next_Steps, Insight→Current_State.
    Activated when features.synthesis_engine_enabled = true.
    """
    if not SYNTHESIS_ENABLED:
        return
    log.info(f"[synthesis_engine] Would update synthesis for project: {project}")
    # TODO: implement section-level synthesis update
    # Fetch Knowledge items by project + item_type
    # Map to synthesis sections
    # Update only affected sections (never regenerate full synthesis)


# ─── Cluster Assignment (Layer 4, optional) ───────────────────────────────────

def assign_to_cluster(canonical_key: str, knowledge_page_url: str, project: str):
    """
    Attempt to assign a knowledge item to an existing Concept_Cluster.
    Only active when CLUSTERS_ENABLED=true and DB_CLUSTERS_DS is set.
    Clusters are created manually or when 3+ items converge (future automation).
    """
    if not CLUSTERS_ENABLED or not DB_CLUSTERS_DS:
        return
    try:
        search_q = canonical_key.replace("_", " ")[:80]
        clusters = notion_search_db(DB_CLUSTERS_DS, query=search_q)
        for cluster in clusters:
            cluster_key = normalize_key(cluster.get("title", ""))
            sim = canonical_key_similarity(canonical_key, cluster_key)
            if sim >= 0.5:
                log.info(f"    → Assigned to cluster: {cluster.get('title')} (sim={sim:.2f})")
                # Update cluster Evidence_Count
                cluster_url = cluster.get("url", "")
                if cluster_url:
                    notion_update_page(cluster_url, {
                        "date:Last_Update:start": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                        "date:Last_Update:is_datetime": 0,
                    })
                return
        log.debug(f"    → No matching cluster for: {canonical_key}")
    except Exception as e:
        log.warning(f"    → Cluster assignment failed: {e}")

# ─── Session Processing ───────────────────────────────────────────────────────

def process_session(session_result: dict, dry_run: bool) -> Optional[str]:
    """
    Process one session through all pipeline layers:
    1. Fetch full page content
    2. Call LLM to distill candidate items (with canonical keys + graph hints)
    3. Apply merge decision tree for each candidate (6 cases)
    4. Optionally assign to Concept_Clusters (Layer 4)
    5. Update session metadata
    Returns session timestamp if processed, else None.
    """
    page_url = session_result.get("url", "")
    title = session_result.get("title", "Untitled")
    log.info(f"Processing: {title}")

    try:
        full = notion_fetch(page_url)
    except Exception as e:
        log.warning(f"Could not fetch page {page_url}: {e}")
        return None

    page_text = full.get("text", "")

    # Skip if already processed
    if '"Processed": "__YES__"' in page_text or '"Processed":true' in page_text:
        log.info(f"  → Already processed, skipping.")
        return None

    if not page_text or len(page_text.strip()) < 50:
        log.warning(f"  → No usable content, skipping.")
        return None

    # Call LLM
    distilled = call_llm(page_text, title)
    if not distilled:
        log.warning(f"  → LLM distillation failed for: {title}")
        return None

    today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    project = distilled.get("project", "")
    subproject = distilled.get("subproject")

    valid_keywords = {
        "yOS", "Memory", "Pipeline", "Notion", "LLM", "Knowledge",
        "Distillation", "Merge", "Canonical", "Cluster", "Graph",
        "Architecture", "Hardware", "Creative"
    }
    kw = [k for k in distilled.get("keywords", []) if k in valid_keywords]

    # Process each candidate knowledge item
    knowledge_items = distilled.get("knowledge_items", [])
    merge_log = []

    for item in knowledge_items:
        item["_project"] = project

        # Layer 3: Find similar items (canonical key first filter)
        similar = find_similar_knowledge_items(item, project)

        # Layer 3: Apply merge decision tree
        action = apply_merge_decision(item, similar, project, today_iso, dry_run)
        merge_log.append(f"{action}: [{item.get('item_type')}] {item.get('title')} [{item.get('canonical_key')}]")

        # Layer 4: Cluster assignment (if enabled)
        if action == "created" and not dry_run:
            assign_to_cluster(item.get("canonical_key", ""), page_url, project)

    # Update session metadata
    if not dry_run:
        session_props = {
            "Processed": "__YES__",
            "date:Processed_Date:start": today_iso,
            "date:Processed_Date:is_datetime": 0,
            "Short_Summary": distilled.get("short_summary", "")[:2000],
            "Language": distilled.get("language", "Mixed"),
            "Quality_Flag": distilled.get("quality_flag", "partial"),
        }
        if kw:
            session_props["Keywords"] = json.dumps(kw)
        if project in VALID_PROJECTS:
            session_props["Projects"] = json.dumps([project])
        if subproject and subproject in VALID_SUBPROJECTS:
            session_props["Subprojects"] = json.dumps([subproject])
        try:
            notion_update_page(page_url, session_props)
            log.info(f"  → Session updated: {title}")
        except Exception as e:
            log.error(f"  → Failed to update session: {e}")
    else:
        log.info(f"  [DRY-RUN] Merge log for '{title}':")
        for entry in merge_log:
            log.info(f"    {entry}")

    return session_result.get("timestamp")

# ─── Main Pipeline Loop ───────────────────────────────────────────────────────

def run_pipeline(dry_run: bool = False, force_all: bool = False):
    log.info("=" * 60)
    log.info(f"LLM Distillation Pipeline v1.3 — {'DRY RUN' if dry_run else 'LIVE'}")
    log.info(f"Model: {DISTILL_MODEL} | Clusters: {CLUSTERS_ENABLED} | Graph: {GRAPH_ENABLED} | Context: {CONTEXT_BUILDER_ENABLED} | Signals: {SIGNAL_SCORING_ENABLED}")
    log.info("=" * 60)

    # Step 1: Read pipeline state
    try:
        state = get_pipeline_state()
    except RuntimeError as e:
        log.error(f"Cannot read pipeline state: {e}")
        sys.exit(1)

    state_url = state.get("url", "")
    last_processed = None
    try:
        state_full = notion_fetch(state_url)
        state_text = state_full.get("text", "")
        match = re.search(r'"Last_Processed"[^"]*"([0-9]{4}-[0-9]{2}-[0-9]{2}[^"]*?)"', state_text)
        if match:
            last_processed = match.group(1)
        log.info(f"Last_Processed: {last_processed}")
    except Exception as e:
        log.warning(f"Could not parse Last_Processed: {e}")
    log.info(f"Pipeline state loaded. URL: {state_url}")

    # Step 2: Fetch new sessions
    sessions = get_new_sessions(last_processed, force_all)

    if not sessions:
        log.info("No new sessions found. Pipeline complete.")
        update_pipeline_state(state_url, None, "success", "No new sessions found.", 0, dry_run)
        return

    log.info(f"Processing {len(sessions)} sessions...")

    # Step 3: Process each session
    processed_timestamps = []
    processed_count = 0
    errors = 0

    for session in sessions:
        try:
            ts = process_session(session, dry_run)
            if ts:
                processed_timestamps.append(ts)
                processed_count += 1
        except Exception as e:
            log.error(f"Error processing session {session.get('title', '?')}: {e}")
            errors += 1

    # Step 4: Update pipeline state
    newest_ts = None
    if processed_timestamps:
        valid_ts = [t for t in processed_timestamps if t]
        if valid_ts:
            newest_ts = max(valid_ts)

    status = "success" if errors == 0 else ("partial" if processed_count > 0 else "failed")
    notes = f"Processed {processed_count} sessions. Errors: {errors}."
    update_pipeline_state(state_url, newest_ts, status, notes, processed_count, dry_run)

    # Step 5: Update Active_Context (Working Memory — Layer 6)
    if processed_count > 0:
        # Use most common project from processed sessions
        active_project = "yOS"  # default; future: derive from sessions
        update_active_context(active_project, processed_count, dry_run)

    # Step 6: Synthesis engine (Layer 7 — only if enabled)
    if SYNTHESIS_ENABLED and processed_count > 0:
        run_synthesis_engine("yOS", dry_run)

    log.info("=" * 60)
    log.info(f"Pipeline complete. Processed: {processed_count} | Errors: {errors}")
    log.info("=" * 60)


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="LLM Chat → Knowledge Distillation Pipeline v1.3"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Analyze without writing to Notion")
    parser.add_argument("--force-all", action="store_true",
                        help="Reprocess all sessions (bootstrap mode)")
    args = parser.parse_args()
    run_pipeline(dry_run=args.dry_run, force_all=args.force_all)
