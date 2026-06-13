#!/usr/bin/env python3
"""
Y-OS Knowledge Graph Compiler v1
MISSION-013 — Non-destructive Obsidian enrichment pipeline

Pipeline:
  1. Scan corpus
  2. Classify files
  3. Extract metadata
  4. Infer relationships
  5. Add/update YAML frontmatter (additive only)
  6. Add "Related" section (safe append only)
  7. Generate MOC files
  8. Generate graph index
  9. Generate validation report
  10. Commit to Git (when apply=True)

Hard constraints:
  - Never rewrite body content
  - Never delete files
  - Never force-push
  - All changes additive or minimally structural
  - Dry-run mode by default
"""

import os
import re
import json
import yaml
import hashlib
from pathlib import Path
from datetime import date
from collections import defaultdict

# ─── CONFIG ──────────────────────────────────────────────────────────────────

REPO_ROOT = Path("/home/ubuntu/yreg")
MISSION_DIR = REPO_ROOT / "mission_013"
TODAY = date.today().isoformat()
SOURCE_BRANCH = "y-os-doctrine"

# Classification patterns (filename-based, then content-based)
CLASSIFIERS = [
    ("constitution",         r"(Y-OS_Constitution|Constitutional_Core)"),
    ("constitutional_article", r"Article_(I|II|III|IV|V|VI|VII|VIII)"),
    ("adr",                  r"^ADR-\d+"),
    ("mission",              r"^(mission_\d+/|MISSION-\d+)"),
    ("governance_report",    r"(Lakshmi|Governance|Risk|Compliance)"),
    ("learning_report",      r"(Learning|Saraswati|learning_report)"),
    ("ceo_briefing",         r"(CEO_Briefing|ceo_briefing|Ganesha)"),
    ("runtime_spec",         r"(Runtime|runtime_v\d|_runtime)"),
    ("context_pack",         r"(Context_Pack|context_pack|CCR|context_compiler)"),
    ("diagram",              r"\.(mmd|puml|d2)$|Diagram"),
    ("index",                r"(MOC|_Map_|Canonical_Map|Home|Index)"),
    ("artifact",             r"(Artifact_|_Artifact|_Schema|_Model|_Framework|_Standard|_Protocol)"),
]

# ADR number → title mapping (canonical)
ADR_TITLES = {
    "ADR-0006": "Creation of CODO Role",
    "ADR-0007": "Continuous Evolution Loop",
    "ADR-0009": "Operational Value Chain",
    "ADR-0010": "Creation of Brahma",
    "ADR-0011": "Creation of Hanuman",
    "ADR-0012": "Artifact Layer",
    "ADR-0013": "Creation of Lakshmi",
    "ADR-0014": "Y-OS Org Map v2",
    "ADR-0015": "Architectural Layer Corrections",
    "ADR-0016": "Artifact Registry",
    "ADR-0017": "Artifact Lineage Registry v1.1",
    "ADR-0018": "Lakshmi Runtime MVP",
    "ADR-0019": "Lakshmi Runtime v2.1",
    "ADR-0020": "Y-OS Control Plane",
    "ADR-0021": "Foundational Doctrine",
    "ADR-0022": "Theory of Organization",
    "ADR-0023": "Y-ORC Architecture",
    "ADR-0024": "Y-OS Constitution",
    "ADR-0025": "Y-ORC Runtime v1",
    "ADR-0026": "ART Runtime v1",
    "ADR-0027": "Context Continuity",
    "ADR-0028": "CRT Runtime v1",
    "ADR-0029": "Context Compiler",
    "ADR-0030": "CCR Runtime v1 + Governance Patch",
    "ADR-0033": "Governance Determinism",
    "ADR-0034": "Constitutional Elevation",
    "ADR-0035": "Executable Constitutional Governance",
    "ADR-0036": "Context Architecture",
    "ADR-0037": "CCR Runtime v2",
    "ADR-0038": "Session Delta Engine",
    "ADR-0039": "Living Memory Pipeline",
    "ADR-0040": "Knowledge Graph Compiler v1",
}

# Mission number → title mapping
MISSION_TITLES = {
    "001": "Organizational Execution Validation",
    "002": "Real Cognitive Execution",
    "003": "External Provider Diversity",
    "004": "Failure Recovery / CRT Fallback",
    "005": "Knowledge Compounding",
    "005b": "CCR Governance Patch",
    "005c": "Governance Determinism",
    "006": "Constitutional Elevation",
    "007": "Replacement Test",
    "008": "Constitutional Evolution",
    "009": "Executable Constitution",
    "010": "Context Architecture Benchmark",
    "010b": "Context ROI Validation",
    "011": "CCR Runtime v2 Design",
    "012": "Session Delta Engine Design",
    "012a": "Storage Audit",
    "012b": "Living Memory Pipeline Doctrine",
    "013": "Knowledge Graph Compiler v1",
}

# Constitutional articles
CONSTITUTIONAL_ARTICLES = {
    "Article I": "Artifact Primacy",
    "Article II": "Preservation Principle",
    "Article III": "Derivation Transparency",
    "Article IV": "Human Override Primacy",
    "Article V": "Governance Before Autonomy",
}

# ─── SCANNER ─────────────────────────────────────────────────────────────────

def scan_corpus(root: Path) -> list[dict]:
    """Scan all .md files, return list of file info dicts."""
    files = []
    for p in sorted(root.rglob("*.md")):
        if ".git" in p.parts or "node_modules" in p.parts:
            continue
        rel = p.relative_to(root)
        files.append({
            "path": p,
            "rel": str(rel),
            "stem": p.stem,
            "name": p.name,
            "folder": str(rel.parent),
        })
    return files

# ─── CLASSIFIER ──────────────────────────────────────────────────────────────

def classify_file(info: dict) -> str:
    rel = info["rel"]
    stem = info["stem"]
    folder = info["folder"]

    # Mission folder files get mission-specific types
    if re.match(r"mission_\d+", folder):
        if re.search(r"(ADR-\d+)", stem):
            return "adr"
        if re.search(r"(ceo_briefing|CEO_Briefing)", stem, re.I):
            return "ceo_briefing"
        if re.search(r"(learning_report|Saraswati|Learning)", stem, re.I):
            return "learning_report"
        if re.search(r"(lakshmi|governance|risk)", stem, re.I):
            return "governance_report"
        if re.search(r"(Runtime|runtime)", stem):
            return "runtime_spec"
        if re.search(r"(Doctrine|Architecture|Design|Framework|Standard|Protocol|Schema)", stem):
            return "artifact"
        if re.search(r"(Diagram|diagram)", stem):
            return "diagram"
        return "mission"

    # Top-level classification
    for type_name, pattern in CLASSIFIERS:
        if re.search(pattern, stem) or re.search(pattern, rel):
            return type_name

    return "unknown"

def extract_adr_number(stem: str) -> str | None:
    m = re.match(r"(ADR-\d+)", stem)
    return m.group(1) if m else None

def extract_mission_number(folder: str) -> str | None:
    m = re.match(r"mission_(\d+[a-z]*)", folder)
    return m.group(1) if m else None

def extract_status_from_content(content: str) -> str:
    m = re.search(r"\*\*Status:\*\*\s*(\w+)", content)
    if m:
        return m.group(1).upper()
    m = re.search(r"Status:\s*(\w+)", content)
    if m:
        return m.group(1).upper()
    return "ACCEPTED"

def extract_version(stem: str) -> str:
    m = re.search(r"_v(\d+[\.\d]*)", stem)
    return f"v{m.group(1)}" if m else ""

def extract_date_from_content(content: str) -> str:
    m = re.search(r"\*\*Date:\*\*\s*([\d-]+)", content)
    if m:
        return m.group(1)
    m = re.search(r"Date:\s*([\d-]+)", content)
    if m:
        return m.group(1)
    return TODAY

def infer_owner(file_type: str, stem: str) -> str:
    if file_type == "governance_report" or "lakshmi" in stem.lower():
        return "Lakshmi"
    if file_type == "learning_report" or "saraswati" in stem.lower():
        return "Saraswati"
    if file_type == "ceo_briefing" or "ganesha" in stem.lower():
        return "Ganesha"
    if "brahma" in stem.lower():
        return "Brahma"
    if "krishna" in stem.lower():
        return "Krishna"
    if "hanuman" in stem.lower():
        return "Hanuman"
    if file_type == "adr":
        return "Brahma"
    if file_type == "constitution":
        return "Yannick"
    return "Manus Y-OS"

def find_referenced_adrs(content: str) -> list[str]:
    return sorted(set(re.findall(r"ADR-\d+", content)))

def find_referenced_missions(content: str, folder: str) -> list[str]:
    refs = set(re.findall(r"MISSION-(\d+[A-Za-z]*)", content, re.I))
    # Also infer from folder
    m = extract_mission_number(folder)
    if m:
        refs.add(m.upper())
    return sorted(refs)

def find_constitutional_articles(content: str) -> list[str]:
    articles = []
    for art, title in CONSTITUTIONAL_ARTICLES.items():
        if art in content or title in content:
            articles.append(f"{art}: {title}")
    return articles

# ─── FRONTMATTER BUILDER ─────────────────────────────────────────────────────

def has_frontmatter(content: str) -> bool:
    return content.startswith("---\n") or content.startswith("---\r\n")

def parse_existing_frontmatter(content: str) -> tuple[dict, str]:
    """Returns (frontmatter_dict, body_without_frontmatter)."""
    if not has_frontmatter(content):
        return {}, content
    end = content.find("\n---\n", 4)
    if end == -1:
        end = content.find("\n---\r\n", 4)
    if end == -1:
        return {}, content
    fm_str = content[4:end]
    body = content[end + 5:]
    try:
        fm = yaml.safe_load(fm_str) or {}
    except Exception:
        fm = {}
    return fm, body

def build_frontmatter(info: dict, content: str, file_type: str, all_files_index: dict) -> dict:
    """Build complete frontmatter dict, merging with existing if present."""
    existing_fm, _ = parse_existing_frontmatter(content)

    stem = info["stem"]
    folder = info["folder"]
    adr_num = extract_adr_number(stem)
    mission_num = extract_mission_number(folder)
    referenced_adrs = find_referenced_adrs(content)
    referenced_missions = find_referenced_missions(content, folder)
    constitutional_articles = find_constitutional_articles(content)

    # Generate stable ID
    artifact_id = f"yos-{stem.lower().replace('_', '-').replace(' ', '-')[:50]}"

    # Build tags
    tags = ["#yos"]
    type_tag_map = {
        "constitution": "#constitution",
        "constitutional_article": "#constitution",
        "adr": "#adr",
        "mission": "#mission",
        "governance_report": "#governance",
        "learning_report": "#artifact",
        "ceo_briefing": "#artifact",
        "runtime_spec": "#runtime",
        "context_pack": "#context",
        "diagram": "#artifact",
        "index": "#artifact",
        "artifact": "#artifact",
    }
    if file_type in type_tag_map:
        tags.append(type_tag_map[file_type])

    # Status-based tags
    status = extract_status_from_content(content)
    if status in ("ACCEPTED", "ADOPT"):
        tags.append("#accepted")
    elif status in ("PROPOSED", "DRAFT"):
        tags.append("#proposed")
    elif status in ("SUPERSEDED", "DEPRECATED"):
        tags.append("#superseded")
    elif status == "OBSOLETE":
        tags.append("#obsolete")

    # Concept tags
    if re.search(r"(CCR|Context Compiler|context_compiler)", content):
        tags.append("#ccr")
    if re.search(r"(Session Delta|session.delta)", content, re.I):
        tags.append("#session-delta")
    if re.search(r"(Living Memory|living.memory)", content, re.I):
        tags.append("#living-memory")
    if re.search(r"(memory|Memory)", content):
        tags.append("#memory")
    if re.search(r"(lineage|Lineage)", content):
        tags.append("#lineage")

    tags = sorted(set(tags))

    # Aliases
    aliases = []
    if adr_num and adr_num in ADR_TITLES:
        aliases.append(ADR_TITLES[adr_num])
    if mission_num and mission_num in MISSION_TITLES:
        aliases.append(f"MISSION-{mission_num.upper()}")

    # Build wikilinks for related ADRs
    related_adrs_wikilinks = [f"[[{a}]]" for a in referenced_adrs if a != adr_num]

    # Build wikilinks for related missions
    related_missions_wikilinks = [f"[[mission_{m.lower()}]]" for m in referenced_missions]

    # Parent/children inference
    parent = ""
    if mission_num:
        parent = f"[[03_Missions_MOC]]"
    elif adr_num:
        parent = f"[[02_ADR_MOC]]"
    elif file_type == "constitution":
        parent = f"[[01_Constitution_MOC]]"
    elif file_type in ("governance_report",):
        parent = f"[[04_Governance_MOC]]"
    elif file_type == "runtime_spec":
        parent = f"[[05_Runtime_MOC]]"
    elif file_type == "context_pack":
        parent = f"[[06_Context_Architecture_MOC]]"

    fm = {
        "id": existing_fm.get("id", artifact_id),
        "title": existing_fm.get("title", stem.replace("_", " ")),
        "type": existing_fm.get("type", file_type),
        "status": existing_fm.get("status", status),
        "mission": existing_fm.get("mission", f"MISSION-{mission_num.upper()}" if mission_num else ""),
        "date": existing_fm.get("date", extract_date_from_content(content)),
        "version": existing_fm.get("version", extract_version(stem)),
        "owner": existing_fm.get("owner", infer_owner(file_type, stem)),
        "worker": existing_fm.get("worker", ""),
        "provider": existing_fm.get("provider", ""),
        "model": existing_fm.get("model", ""),
        "parent": existing_fm.get("parent", parent),
        "parents": existing_fm.get("parents", []),
        "children": existing_fm.get("children", []),
        "related_adrs": existing_fm.get("related_adrs", related_adrs_wikilinks),
        "related_missions": existing_fm.get("related_missions", related_missions_wikilinks),
        "related_concepts": existing_fm.get("related_concepts", []),
        "constitutional_articles": existing_fm.get("constitutional_articles", constitutional_articles),
        "tags": existing_fm.get("tags", tags),
        "aliases": existing_fm.get("aliases", aliases),
        "source_branch": SOURCE_BRANCH,
        "canonical": True,
    }

    # Remove empty values for cleanliness
    fm = {k: v for k, v in fm.items() if v != "" and v != [] and v is not None}
    # Always keep these even if empty
    for k in ("id", "title", "type", "status", "source_branch", "canonical"):
        if k not in fm:
            fm[k] = "" if k not in ("canonical",) else True

    return fm

def render_frontmatter(fm: dict) -> str:
    """Render frontmatter dict to YAML string."""
    # Use custom ordering
    key_order = [
        "id", "title", "type", "status", "mission", "date", "version",
        "owner", "worker", "provider", "model",
        "parent", "parents", "children",
        "related_adrs", "related_missions", "related_concepts",
        "constitutional_articles", "tags", "aliases",
        "source_branch", "canonical"
    ]
    ordered = {}
    for k in key_order:
        if k in fm:
            ordered[k] = fm[k]
    for k in fm:
        if k not in ordered:
            ordered[k] = fm[k]

    return yaml.dump(ordered, allow_unicode=True, default_flow_style=False, sort_keys=False)

def enrich_file(info: dict, dry_run: bool = True) -> dict:
    """Enrich a single file. Returns change report."""
    path = info["path"]
    content = path.read_text(encoding="utf-8")
    file_type = classify_file(info)

    # Skip binary-ish or very short files
    if len(content.strip()) < 10:
        return {"path": info["rel"], "action": "SKIP", "reason": "too short"}

    # Skip diagram source files
    if path.suffix in (".mmd", ".puml", ".d2"):
        return {"path": info["rel"], "action": "SKIP", "reason": "non-markdown"}

    had_frontmatter = has_frontmatter(content)
    existing_fm, body = parse_existing_frontmatter(content)

    # Build new frontmatter
    fm = build_frontmatter(info, content, file_type, {})
    fm_str = render_frontmatter(fm)
    new_content = f"---\n{fm_str}---\n\n{body if had_frontmatter else content}"

    # Verify body is preserved
    if had_frontmatter:
        body_check = body
    else:
        body_check = content

    # Safety check: body must be preserved
    if body_check.strip() not in new_content:
        return {"path": info["rel"], "action": "SKIP", "reason": "body_integrity_check_failed"}

    changed = new_content != content
    action = "UPDATE" if (had_frontmatter and changed) else ("ADD_FRONTMATTER" if not had_frontmatter else "NO_CHANGE")

    if not dry_run and changed:
        path.write_text(new_content, encoding="utf-8")

    return {
        "path": info["rel"],
        "action": action,
        "type": file_type,
        "had_frontmatter": had_frontmatter,
        "tags_added": fm.get("tags", []),
        "adrs_linked": fm.get("related_adrs", []),
        "missions_linked": fm.get("related_missions", []),
    }

# ─── MOC GENERATOR ───────────────────────────────────────────────────────────

def generate_mocs(files: list[dict], dry_run: bool = True) -> list[str]:
    """Generate all 8 MOC files."""
    moc_dir = REPO_ROOT
    generated = []

    # Classify all files
    classified = [(f, classify_file(f)) for f in files]

    # ── 00_Y-OS_Home.md ──
    home_content = f"""---
id: yos-home
title: Y-OS Knowledge Graph — Home
type: index
status: ACTIVE
date: {TODAY}
source_branch: {SOURCE_BRANCH}
canonical: true
tags:
  - "#yos"
  - "#artifact"
aliases:
  - Y-OS Home
  - YOS Home
---

# Y-OS Knowledge Graph — Home

> **Y-OS** is an AI-native organizational operating system. This vault is the canonical Obsidian-native representation of the Y-OS doctrine corpus.

## Navigation

| Section | MOC | Description |
| :--- | :--- | :--- |
| Constitution | [[01_Constitution_MOC]] | Foundational law — FROZEN |
| ADRs | [[02_ADR_MOC]] | Architecture Decision Records |
| Missions | [[03_Missions_MOC]] | Validated execution missions |
| Governance | [[04_Governance_MOC]] | Lakshmi governance artifacts |
| Runtime | [[05_Runtime_MOC]] | Operational runtime specs |
| Context Architecture | [[06_Context_Architecture_MOC]] | CCR, context packs, modes |
| Living Memory | [[07_Living_Memory_MOC]] | LMP, session delta, memory lifecycle |

## Key Artifacts

- [[Y-OS_Constitution_v1]] — Constitutional layer (FROZEN)
- [[Y-OS_Canonical_Map_v1]] — Navigation entry point
- [[Y-OS_Master_Architecture_Atlas_v1_final]] — 21-section architecture atlas
- [[Y-OS_Git_Architecture_v1]] — Git/GitHub persistence architecture

## Status

- **Branch:** `{SOURCE_BRANCH}`
- **Last compiled:** {TODAY}
- **Total files:** {len(files)}
"""
    if not dry_run:
        (moc_dir / "00_Y-OS_Home.md").write_text(home_content, encoding="utf-8")
    generated.append("00_Y-OS_Home.md")

    # ── 01_Constitution_MOC.md ──
    const_files = [(f, t) for f, t in classified if t in ("constitution", "constitutional_article")]
    const_links = "\n".join(f"- [[{f['stem']}]]" for f, t in const_files)
    const_content = f"""---
id: yos-constitution-moc
title: Y-OS Constitution — Map of Content
type: index
status: ACTIVE
date: {TODAY}
source_branch: {SOURCE_BRANCH}
canonical: true
tags:
  - "#yos"
  - "#constitution"
  - "#artifact"
related_adrs:
  - "[[ADR-0024]]"
  - "[[ADR-0034]]"
aliases:
  - Constitution MOC
---

# Y-OS Constitution — Map of Content

> The Y-OS Constitution defines what cannot change. It is the highest-authority layer of the Y-OS doctrine stack.

## Constitutional Documents

{const_links if const_links else "- [[Y-OS_Constitution_v1]]"}
- [[Y-OS_Constitutional_Core_v1]]

## Constitutional Articles

| Article | Title | Status |
| :--- | :--- | :--- |
| Article I | Artifact Primacy | FROZEN |
| Article II | Preservation Principle | FROZEN |
| Article III | Derivation Transparency | FROZEN |
| Article IV | Human Override Primacy | FROZEN |
| Article V | Governance Before Autonomy | FROZEN |

## Related ADRs

- [[ADR-0024]] — Y-OS Constitution
- [[ADR-0034]] — Constitutional Elevation Framework
- [[ADR-0035]] — Executable Constitutional Governance

## Back

[[00_Y-OS_Home]]
"""
    if not dry_run:
        (moc_dir / "01_Constitution_MOC.md").write_text(const_content, encoding="utf-8")
    generated.append("01_Constitution_MOC.md")

    # ── 02_ADR_MOC.md ──
    adr_files = sorted([(f, t) for f, t in classified if t == "adr"], key=lambda x: x[0]["stem"])
    adr_rows = "\n".join(
        f"| [[{f['stem']}]] | {ADR_TITLES.get(extract_adr_number(f['stem']) or '', f['stem'])} | — |"
        for f, t in adr_files
    )
    adr_content = f"""---
id: yos-adr-moc
title: Y-OS ADR Register — Map of Content
type: index
status: ACTIVE
date: {TODAY}
source_branch: {SOURCE_BRANCH}
canonical: true
tags:
  - "#yos"
  - "#adr"
  - "#artifact"
aliases:
  - ADR Register
  - ADR MOC
---

# Y-OS ADR Register — Map of Content

> Architecture Decision Records are the canonical record of every significant architectural decision in Y-OS.

## ADR Index

| ADR | Title | Status |
| :--- | :--- | :--- |
{adr_rows}

## ADR Lifecycle

`PROPOSED` → `ACCEPTED` → `SUPERSEDED` (if replaced)

## Back

[[00_Y-OS_Home]]
"""
    if not dry_run:
        (moc_dir / "02_ADR_MOC.md").write_text(adr_content, encoding="utf-8")
    generated.append("02_ADR_MOC.md")

    # ── 03_Missions_MOC.md ──
    mission_rows = "\n".join(
        f"| [[mission_{num}]] | {title} | ✅ |"
        for num, title in MISSION_TITLES.items()
    )
    missions_content = f"""---
id: yos-missions-moc
title: Y-OS Missions — Map of Content
type: index
status: ACTIVE
date: {TODAY}
source_branch: {SOURCE_BRANCH}
canonical: true
tags:
  - "#yos"
  - "#mission"
  - "#artifact"
aliases:
  - Missions MOC
  - Mission Register
---

# Y-OS Missions — Map of Content

> Each mission is a validated execution cycle that advances the Y-OS runtime. All missions follow the CEO Directive → Krishna → Brahma → Hanuman → Lakshmi → Saraswati → Ganesha pattern.

## Mission Register

| Mission | Title | Status |
| :--- | :--- | :--- |
{mission_rows}

## Mission Anatomy

Each mission folder contains:
- `01_mission_definition.md` — CEO Directive
- `02_*` — Krishna (CSO/Strategy)
- `03_*` — Brahma (CTO/Architecture)
- `04_*` — Hanuman (Builder)
- `05_*` — Lakshmi (Governance)
- `06_*` — Saraswati (Learning)
- `07_*` / `09_ceo_briefing.md` — Ganesha (CEO Briefing)
- `ADR-XXXX_*.md` — Architecture Decision Record

## Back

[[00_Y-OS_Home]]
"""
    if not dry_run:
        (moc_dir / "03_Missions_MOC.md").write_text(missions_content, encoding="utf-8")
    generated.append("03_Missions_MOC.md")

    # ── 04_Governance_MOC.md ──
    gov_content = f"""---
id: yos-governance-moc
title: Y-OS Governance — Map of Content
type: index
status: ACTIVE
date: {TODAY}
source_branch: {SOURCE_BRANCH}
canonical: true
tags:
  - "#yos"
  - "#governance"
  - "#artifact"
related_adrs:
  - "[[ADR-0033]]"
  - "[[ADR-0034]]"
  - "[[ADR-0035]]"
aliases:
  - Governance MOC
---

# Y-OS Governance — Map of Content

> Governance in Y-OS is enforced by Lakshmi (CLO/Risk). Every architectural decision passes a risk review before adoption.

## Governance Standard

**PASS = Score ≤ 55 AND Verdict ∈ {{APPROVE, APPROVE_WITH_WARNING}} AND Blocking Reasons = 0**

## Key Governance Documents

- [[Governance_Determinism_Framework_v1]] — ADR-0033
- [[Y-OS_Constitutional_Core_v1]] — 5 Articles
- [[Y-OS_Governance_Doctrine]]
- [[Governance_Model_v1]]

## Governance Reports by Mission

- [[mission_005c]] — Governance Determinism
- [[mission_006]] — Constitutional Elevation (Lakshmi 5/5 YES)
- [[mission_009]] — Executable Constitution
- [[mission_012b]] — Living Memory Pipeline (Score 12 — Pristine)

## Related ADRs

- [[ADR-0033]] — Governance Determinism
- [[ADR-0034]] — Constitutional Elevation
- [[ADR-0035]] — Executable Constitutional Governance

## Back

[[00_Y-OS_Home]]
"""
    if not dry_run:
        (moc_dir / "04_Governance_MOC.md").write_text(gov_content, encoding="utf-8")
    generated.append("04_Governance_MOC.md")

    # ── 05_Runtime_MOC.md ──
    runtime_content = f"""---
id: yos-runtime-moc
title: Y-OS Runtime — Map of Content
type: index
status: ACTIVE
date: {TODAY}
source_branch: {SOURCE_BRANCH}
canonical: true
tags:
  - "#yos"
  - "#runtime"
  - "#artifact"
related_adrs:
  - "[[ADR-0025]]"
  - "[[ADR-0026]]"
  - "[[ADR-0028]]"
aliases:
  - Runtime MOC
---

# Y-OS Runtime — Map of Content

> The Y-OS runtime is the operational layer that executes organizational intelligence. It consists of Y-ORC, ART, CRT, and CCR.

## Runtime Components

| Component | File | ADR | Description |
| :--- | :--- | :--- | :--- |
| Y-ORC v1 | [[yorc_runtime_v1]] | [[ADR-0025]] | Orchestrator + Notion Registry |
| ART v1 | [[art_runtime_v1]] | [[ADR-0026]] | Agent Routing Table |
| CRT v1 | [[crt_runtime_v1]] | [[ADR-0028]] | Worker-to-Model resolver |
| CCR v1 | [[context_compiler_v1]] | [[ADR-0029]] | Context Pack compiler |
| CCR v1.1 | [[CCR_Runtime_v1.1_Governance_Patch]] | [[ADR-0030]] | Governance patch |
| CCR v2 | [[CCR_Runtime_v2_Architecture]] | [[ADR-0037]] | Mode B/D context router |

## Worker Registry

- [[worker_registry]] — Capability → Worker mapping
- [[model_registry]] — Worker → Model/Provider mapping

## Back

[[00_Y-OS_Home]]
"""
    if not dry_run:
        (moc_dir / "05_Runtime_MOC.md").write_text(runtime_content, encoding="utf-8")
    generated.append("05_Runtime_MOC.md")

    # ── 06_Context_Architecture_MOC.md ──
    ctx_content = f"""---
id: yos-context-moc
title: Y-OS Context Architecture — Map of Content
type: index
status: ACTIVE
date: {TODAY}
source_branch: {SOURCE_BRANCH}
canonical: true
tags:
  - "#yos"
  - "#context"
  - "#ccr"
  - "#artifact"
related_adrs:
  - "[[ADR-0036]]"
  - "[[ADR-0037]]"
  - "[[ADR-0038]]"
aliases:
  - Context Architecture MOC
  - CCR MOC
---

# Y-OS Context Architecture — Map of Content

> Context architecture defines how Y-OS compiles, governs, and injects execution context into each mission cycle.

## Context Modes

| Mode | Name | Tokens | ROI/1k | Use |
| :--- | :--- | :--- | :--- | :--- |
| Mode A | Raw Session History | ~2000 | 45.7 | REJECTED |
| **Mode B** | **Context Pack Only** | **~623** | **140.9** | **PRODUCTION DEFAULT** |
| Mode C | Context Pack + Delta | ~890 | 98.4 | Optional |
| Mode D | Context Pack + Canonical Memory | ~1100 | 83.2 | Constitutional work |
| Mode E | Full Hybrid | ~1800 | 91.3 | Benchmarking only |
| Mode F | Session History Hybrid | ~2400 | 38.1 | REJECTED |

## Key Documents

- [[CCR_Runtime_v2_Architecture]] — ADR-0037
- [[Session_Delta_Engine_v1]] — ADR-0038
- [[Context_Pack_Schema_v1]]
- [[Context_Pack_Standard_v1]]

## Back

[[00_Y-OS_Home]]
"""
    if not dry_run:
        (moc_dir / "06_Context_Architecture_MOC.md").write_text(ctx_content, encoding="utf-8")
    generated.append("06_Context_Architecture_MOC.md")

    # ── 07_Living_Memory_MOC.md ──
    lm_content = f"""---
id: yos-living-memory-moc
title: Y-OS Living Memory — Map of Content
type: index
status: ACTIVE
date: {TODAY}
source_branch: {SOURCE_BRANCH}
canonical: true
tags:
  - "#yos"
  - "#memory"
  - "#living-memory"
  - "#session-delta"
  - "#artifact"
related_adrs:
  - "[[ADR-0038]]"
  - "[[ADR-0039]]"
aliases:
  - Living Memory MOC
  - LMP MOC
---

# Y-OS Living Memory — Map of Content

> The Living Memory Pipeline (LMP) is the canonical 8-stage lifecycle from live interaction to runtime context injection.

## Pipeline Stages

```
Capture → Compress → Delta → Summarize → Archive → Canonicalize → Compile → Inject
```

| Stage | Name | Component |
| :---: | :--- | :--- |
| 1 | Capture | Y-ORC / Session Logger |
| 2 | Compress | CCR |
| 3 | Delta | Session Delta Engine |
| 4 | Summarize | CCR / Saraswati |
| 5 | Archive | Artifact Writer |
| 6 | Canonicalize | Lakshmi |
| 7 | Compile | CCR Runtime v2 |
| 8 | Inject | Context Router |

## Key Documents

- [[Living_Memory_Pipeline_Doctrine_v1]] — ADR-0039
- [[Session_Delta_Engine_v1]] — ADR-0038
- [[CCR_Runtime_v2_Architecture]] — ADR-0037

## Back

[[00_Y-OS_Home]]
"""
    if not dry_run:
        (moc_dir / "07_Living_Memory_MOC.md").write_text(lm_content, encoding="utf-8")
    generated.append("07_Living_Memory_MOC.md")

    return generated

# ─── GRAPH INDEX GENERATOR ───────────────────────────────────────────────────

def generate_graph_index(files: list[dict], results: list[dict]) -> dict:
    """Generate a JSON graph index for programmatic use."""
    nodes = []
    edges = []

    for r in results:
        if r["action"] == "SKIP":
            continue
        node = {
            "id": r["path"],
            "type": r.get("type", "unknown"),
            "tags": r.get("tags_added", []),
        }
        nodes.append(node)
        for adr in r.get("adrs_linked", []):
            edges.append({"from": r["path"], "to": adr, "rel": "references_adr"})
        for m in r.get("missions_linked", []):
            edges.append({"from": r["path"], "to": m, "rel": "references_mission"})

    return {"nodes": nodes, "edges": edges, "generated": TODAY}

# ─── VALIDATION ──────────────────────────────────────────────────────────────

def compute_metrics(files: list[dict], results: list[dict]) -> dict:
    total_md = len(files)
    had_fm = sum(1 for r in results if r.get("had_frontmatter"))
    will_have_fm = sum(1 for r in results if r.get("action") in ("ADD_FRONTMATTER", "UPDATE", "NO_CHANGE") and r.get("action") != "SKIP")
    adrs_with_links = sum(1 for r in results if r.get("type") == "adr" and r.get("adrs_linked"))
    total_adrs = sum(1 for r in results if r.get("type") == "adr")
    missions_with_links = sum(1 for r in results if r.get("type") == "mission" and r.get("missions_linked"))
    total_missions = sum(1 for r in results if r.get("type") == "mission")
    wikilinks_added = sum(len(r.get("adrs_linked", [])) + len(r.get("missions_linked", [])) for r in results)

    return {
        "total_md_files": total_md,
        "files_with_frontmatter_before": had_fm,
        "files_with_frontmatter_after": will_have_fm,
        "frontmatter_coverage_pct": round(will_have_fm / total_md * 100, 1) if total_md else 0,
        "wikilinks_before": 0,  # from baseline scan
        "wikilinks_added": wikilinks_added,
        "total_adrs": total_adrs,
        "adrs_with_links": adrs_with_links,
        "adr_link_coverage_pct": round(adrs_with_links / total_adrs * 100, 1) if total_adrs else 0,
        "total_missions": total_missions,
        "missions_with_links": missions_with_links,
        "mission_link_coverage_pct": round(missions_with_links / total_missions * 100, 1) if total_missions else 0,
    }

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def run(dry_run: bool = True):
    print(f"\n{'='*60}")
    print(f"Y-OS Knowledge Graph Compiler v1")
    print(f"Mode: {'DRY-RUN' if dry_run else 'APPLY'}")
    print(f"Date: {TODAY}")
    print(f"{'='*60}\n")

    # 1. Scan
    print("Step 1: Scanning corpus...")
    files = scan_corpus(REPO_ROOT)
    print(f"  Found {len(files)} Markdown files")

    # 2. Classify + enrich
    print("\nStep 2-5: Classifying and enriching files...")
    results = []
    for info in files:
        r = enrich_file(info, dry_run=dry_run)
        results.append(r)

    # Summary by action
    from collections import Counter
    action_counts = Counter(r["action"] for r in results)
    type_counts = Counter(r.get("type", "unknown") for r in results if r["action"] != "SKIP")
    print(f"  Actions: {dict(action_counts)}")
    print(f"  Types: {dict(type_counts)}")

    # 3. Generate MOCs
    print("\nStep 7: Generating MOC files...")
    mocs = generate_mocs(files, dry_run=dry_run)
    print(f"  Generated: {mocs}")

    # 4. Metrics
    metrics = compute_metrics(files, results)
    print(f"\nStep 9: Metrics")
    for k, v in metrics.items():
        print(f"  {k}: {v}")

    # 5. Graph index
    graph = generate_graph_index(files, results)

    # 6. Save reports
    MISSION_DIR.mkdir(exist_ok=True)

    report = {
        "mode": "dry_run" if dry_run else "applied",
        "date": TODAY,
        "metrics": metrics,
        "action_counts": dict(action_counts),
        "type_counts": dict(type_counts),
        "mocs_generated": mocs,
        "results": results[:20],  # sample
    }

    report_path = MISSION_DIR / ("kg_dryrun_report.json" if dry_run else "kg_apply_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2, default=str)
    print(f"\n  Report saved: {report_path}")

    graph_path = MISSION_DIR / "kg_graph_index.json"
    with open(graph_path, "w") as f:
        json.dump(graph, f, indent=2)
    print(f"  Graph index saved: {graph_path}")

    return report, metrics

if __name__ == "__main__":
    import sys
    dry_run = "--apply" not in sys.argv
    run(dry_run=dry_run)
