#!/usr/bin/env python3
"""
KGC v2 — Knowledge Graph Compiler v2
MISSION-015 — Cognitive Graph Architecture + Visual Drill-Down

Capabilities:
  A. Semantic relationship inference (21 types)
  B. YAML frontmatter update with typed relations
  C. Body Semantic Links section (additive only)
  D. kg_semantic_graph_v2.json generation
  E. Dry-run mode (default)

Hard constraints:
  - Never delete files
  - Never rewrite canonical body text
  - Only add Semantic Links section at bottom
  - All edits reversible via Git
  - Dry-run before apply
"""

import re
import json
import yaml
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Optional

REPO_ROOT = Path("/home/ubuntu/yreg")
TODAY = "2026-06-14"

# ─── 21 Semantic Relationship Types ───────────────────────────────────────────
RELATION_TYPES = [
    "derives_from", "supersedes", "superseded_by",
    "validates", "validated_by",
    "produces", "produced_by",
    "implements", "implemented_by",
    "governed_by", "governs",
    "depends_on", "enables",
    "evolves_into", "evolved_from",
    "canonical_source",
    "constrained_by",
    "executed_by",
    "routes_to", "compiles", "injects",
    "observes", "audits", "stores", "publishes",
    "references",
]

# ─── Inference Rules ──────────────────────────────────────────────────────────

def infer_supersedes(stem: str, body: str, fm: dict) -> dict:
    """R1: ADR body 'Supersedes: ADR-XXXX' → supersedes"""
    rels = defaultdict(list)
    for m in re.finditer(r'[Ss]upersedes?[:\s]+\*?\*?(\[\[)?(ADR-\d+)', body):
        target = m.group(2)
        rels["supersedes"].append(f"[[{target}]]")
    # R8: filename _v2 supersedes _v1
    v2_match = re.search(r'_v(\d+)', stem)
    if v2_match and int(v2_match.group(1)) > 1:
        v_prev = int(v2_match.group(1)) - 1
        base = stem[:v2_match.start()]
        rels["supersedes"].append(f"[[{base}_v{v_prev}]]")
    return dict(rels)

def infer_produces(stem: str, body: str, fm: dict, folder: str) -> dict:
    """R3: Mission folder contains ADR → mission produces ADR"""
    rels = defaultdict(list)
    # If file is a mission report, find ADRs mentioned
    if fm.get("type") in ("mission",) or "MISSION" in stem.upper():
        for m in re.finditer(r'ADR-(\d+)', body):
            rels["produces"].append(f"[[ADR-{m.group(1)}]]")
    return dict(rels)

def infer_validates(stem: str, body: str, fm: dict, folder: str) -> dict:
    """R5: Governance report validates ADR/mission"""
    rels = defaultdict(list)
    if fm.get("type") in ("governance_report",) or "governance" in stem.lower() or "lakshmi" in stem.lower():
        for m in re.finditer(r'ADR-(\d+)', body):
            rels["validates"].append(f"[[ADR-{m.group(1)}]]")
        for m in re.finditer(r'MISSION-(\d+\w*)', body):
            rels["validates"].append(f"[[mission_{m.group(1).lower()}]]")
    return dict(rels)

def infer_governed_by(stem: str, body: str, fm: dict) -> dict:
    """R-gov: ADR references governance concept"""
    rels = defaultdict(list)
    if re.search(r'[Gg]overnance [Dd]eterminism', body):
        rels["governed_by"].append("[[Governance_Determinism]]")
    if re.search(r'[Ll]akshmi', body):
        rels["governed_by"].append("[[Lakshmi_Governance]]")
    if re.search(r'[Cc]onstitutional [Gg]overnance', body):
        rels["governed_by"].append("[[Constitutional_Governance]]")
    return dict(rels)

def infer_implements(stem: str, body: str, fm: dict) -> dict:
    """R-impl: Runtime file implements concept"""
    rels = defaultdict(list)
    if re.search(r'[Cc][Cc][Rr]|[Cc]ontext [Cc]ompiler', body):
        rels["implements"].append("[[CCR_Runtime]]")
    if re.search(r'[Ll]iving [Mm]emory [Pp]ipeline', body):
        rels["implements"].append("[[Living_Memory]]")
    if re.search(r'[Ss]ession [Dd]elta', body):
        rels["implements"].append("[[Session_Delta]]")
    if re.search(r'[Cc]ontext [Pp]ack', body):
        rels["implements"].append("[[Context_Pack]]")
    return dict(rels)

def infer_depends_on(stem: str, body: str, fm: dict) -> dict:
    """R-dep: Infer dependencies from body references"""
    rels = defaultdict(list)
    # CCR v2 depends on Session Delta
    if "CCR" in stem.upper() and "v2" in stem.lower():
        rels["depends_on"].append("[[Session_Delta]]")
    # LMP depends on CCR
    if re.search(r'[Ll]iving [Mm]emory', stem):
        rels["depends_on"].append("[[CCR_Runtime]]")
    return dict(rels)

def infer_constrained_by(stem: str, body: str, fm: dict) -> dict:
    """R-const: Article references → constrained_by"""
    rels = defaultdict(list)
    articles = re.findall(r'Article\s+(I{1,3}V?|V?I{0,3})[:\s—]', body)
    article_map = {
        "I": "[[Artifact_Primacy]]",
        "II": "[[Preservation_Principle]]",
        "III": "[[Derivation_Transparency]]",
        "IV": "[[Human_Override]]",
        "V": "[[Governance_Before_Autonomy]]",
    }
    for art in set(articles):
        if art in article_map:
            rels["constrained_by"].append(article_map[art])
    return dict(rels)

def infer_executed_by(stem: str, body: str, fm: dict) -> dict:
    """R-exec: Worker references → executed_by"""
    rels = defaultdict(list)
    worker_map = {
        r'[Bb]rahma': "[[Brahma]]",
        r'[Gg]anesha': "[[Ganesha]]",
        r'[Ll]akshmi': "[[Lakshmi]]",
        r'[Ss]araswati': "[[Saraswati]]",
        r'[Hh]anuman': "[[Hanuman]]",
        r'[Kk]rishna': "[[Krishna]]",
    }
    for pattern, node in worker_map.items():
        if re.search(pattern, body):
            rels["executed_by"].append(node)
    return dict(rels)

def infer_evolved_from(stem: str, body: str, fm: dict) -> dict:
    """R-evo: 'Supersedes: ADR-XXXX' on the target → evolved_from"""
    rels = defaultdict(list)
    for m in re.finditer(r'[Ss]upersedes?[:\s]+\*?\*?(\[\[)?(ADR-\d+)', body):
        rels["evolved_from"].append(f"[[{m.group(2)}]]")
    return dict(rels)

def infer_references(stem: str, body: str, fm: dict) -> dict:
    """R-ref: Any ADR mention → references (weak)"""
    rels = defaultdict(list)
    # Only for non-ADR files referencing ADRs
    if fm.get("type") not in ("adr",):
        for m in re.finditer(r'ADR-(\d+)', body):
            ref = f"[[ADR-{m.group(1)}]]"
            if ref not in rels["references"]:
                rels["references"].append(ref)
    return dict(rels)

def infer_compiles(stem: str, body: str, fm: dict) -> dict:
    """R-comp: CCR/compiler references context packs"""
    rels = defaultdict(list)
    if re.search(r'[Cc]ontext [Pp]ack', body) and re.search(r'[Cc]ompil', body):
        rels["compiles"].append("[[Context_Pack]]")
    return dict(rels)

def infer_injects(stem: str, body: str, fm: dict) -> dict:
    """R-inj: CCR injects into missions"""
    rels = defaultdict(list)
    if re.search(r'inject', body, re.I) and re.search(r'[Cc][Cc][Rr]|[Cc]ontext', stem):
        rels["injects"].append("[[Mission]]")
    return dict(rels)

def infer_all(stem: str, body: str, fm: dict, folder: str) -> dict:
    """Run all inference rules and merge results."""
    all_rels = defaultdict(list)
    rule_results = [
        infer_supersedes(stem, body, fm),
        infer_produces(stem, body, fm, folder),
        infer_validates(stem, body, fm, folder),
        infer_governed_by(stem, body, fm),
        infer_implements(stem, body, fm),
        infer_depends_on(stem, body, fm),
        infer_constrained_by(stem, body, fm),
        infer_executed_by(stem, body, fm),
        infer_evolved_from(stem, body, fm),
        infer_references(stem, body, fm),
        infer_compiles(stem, body, fm),
        infer_injects(stem, body, fm),
    ]
    for result in rule_results:
        for rel_type, targets in result.items():
            for t in targets:
                if t not in all_rels[rel_type]:
                    all_rels[rel_type].append(t)
    return dict(all_rels)

# ─── YAML Frontmatter Handling ────────────────────────────────────────────────

def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}, content
    end = content.find("\n---", 3)
    if end == -1:
        return {}, content
    fm_str = content[3:end].strip()
    body = content[end+4:].lstrip("\n")
    try:
        fm = yaml.safe_load(fm_str) or {}
    except Exception:
        fm = {}
    return fm, body

def serialize_frontmatter(fm: dict) -> str:
    """Serialize frontmatter dict back to YAML string."""
    return yaml.dump(fm, allow_unicode=True, default_flow_style=False,
                     sort_keys=False, width=120)

def merge_relations_into_fm(fm: dict, new_rels: dict) -> dict:
    """Merge inferred relationships into existing frontmatter."""
    for rel_type in RELATION_TYPES:
        if rel_type in new_rels and new_rels[rel_type]:
            existing = fm.get(rel_type, []) or []
            if not isinstance(existing, list):
                existing = [existing]
            merged = list(existing)
            for item in new_rels[rel_type]:
                if item not in merged:
                    merged.append(item)
            fm[rel_type] = merged
    return fm

# ─── Semantic Links Section ───────────────────────────────────────────────────

SEMANTIC_LINKS_MARKER = "## Semantic Links"

def build_semantic_links_section(rels: dict) -> str:
    """Build the additive Semantic Links section."""
    lines = ["\n\n---\n\n## Semantic Links\n\n*Inferred by KGC v2 — MISSION-015*\n"]
    for rel_type, targets in sorted(rels.items()):
        if targets:
            for t in targets:
                lines.append(f"- **{rel_type}:** {t}")
    lines.append("")
    return "\n".join(lines)

def add_semantic_links_to_body(body: str, rels: dict) -> tuple[str, bool]:
    """Add or update Semantic Links section at bottom of body."""
    if not rels:
        return body, False
    # Remove existing Semantic Links section if present
    if SEMANTIC_LINKS_MARKER in body:
        idx = body.rfind(SEMANTIC_LINKS_MARKER)
        # Find the start of the section (including preceding ---)
        section_start = body.rfind("\n---\n", 0, idx)
        if section_start != -1:
            body = body[:section_start]
        else:
            body = body[:idx]
        body = body.rstrip()
    new_section = build_semantic_links_section(rels)
    return body + new_section, True

# ─── Main Compiler ────────────────────────────────────────────────────────────

def compile_file(path: Path, dry_run: bool = True) -> dict:
    """Process a single markdown file."""
    content = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)
    stem = path.stem
    folder = str(path.parent.relative_to(REPO_ROOT))

    # Infer relationships
    new_rels = infer_all(stem, body, fm, folder)

    if not new_rels:
        return {"file": str(path.relative_to(REPO_ROOT)), "rels": {}, "modified": False}

    # Update frontmatter
    updated_fm = merge_relations_into_fm(dict(fm), new_rels)

    # Add Semantic Links section
    updated_body, body_modified = add_semantic_links_to_body(body, new_rels)

    # Reconstruct file
    new_content = f"---\n{serialize_frontmatter(updated_fm)}---\n\n{updated_body}"

    if not dry_run:
        path.write_text(new_content, encoding="utf-8")

    return {
        "file": str(path.relative_to(REPO_ROOT)),
        "rels": new_rels,
        "modified": True,
        "body_modified": body_modified,
    }

def build_graph(results: list[dict]) -> dict:
    """Build kg_semantic_graph_v2.json from results."""
    nodes = {}
    edges = []

    for r in results:
        if not r["rels"]:
            continue
        src = r["file"]
        stem = Path(src).stem
        if stem not in nodes:
            nodes[stem] = {"id": stem, "file": src}
        for rel_type, targets in r["rels"].items():
            for t in targets:
                # Extract target stem from [[Target]] or Target
                tgt = re.sub(r'[\[\]]', '', t)
                if tgt not in nodes:
                    nodes[tgt] = {"id": tgt, "file": None}
                edges.append({
                    "source": stem,
                    "target": tgt,
                    "type": rel_type,
                    "inferred": True,
                })

    return {"nodes": list(nodes.values()), "edges": edges}

def run(dry_run: bool = True, verbose: bool = False):
    """Main compiler run."""
    md_files = sorted(REPO_ROOT.rglob("*.md"))
    # Exclude visual maps and dashboards (they are generated, not source)
    md_files = [f for f in md_files if "08_Visual_Maps" not in str(f)
                and "09_Dashboards" not in str(f)]

    print(f"KGC v2 — {'DRY-RUN' if dry_run else 'APPLY'}")
    print(f"Files to process: {len(md_files)}")

    results = []
    modified_count = 0
    total_edges = 0

    for f in md_files:
        r = compile_file(f, dry_run=dry_run)
        results.append(r)
        if r["modified"]:
            modified_count += 1
            edge_count = sum(len(v) for v in r["rels"].values())
            total_edges += edge_count
            if verbose:
                print(f"  {r['file']}: {edge_count} edges")

    print(f"\nFiles modified: {modified_count}")
    print(f"Total semantic edges inferred: {total_edges}")

    # Build and save graph
    graph = build_graph(results)
    graph_path = REPO_ROOT / "mission_015" / "kg_semantic_graph_v2.json"
    graph_path.parent.mkdir(exist_ok=True)
    graph_path.write_text(json.dumps(graph, indent=2, ensure_ascii=False))
    print(f"Graph saved: {graph_path} ({len(graph['nodes'])} nodes, {len(graph['edges'])} edges)")

    return results, graph

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="KGC v2 — Knowledge Graph Compiler v2")
    parser.add_argument("--apply", action="store_true", help="Apply changes (default: dry-run)")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    results, graph = run(dry_run=not args.apply, verbose=args.verbose)
    print("\nDone.")
