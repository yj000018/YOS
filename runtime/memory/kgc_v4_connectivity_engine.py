#!/usr/bin/env python3
"""
KGC v4 Connectivity Engine — Y-OS MISSION-021
Semantic Connectivity Layer

Capabilities:
- Orphan detection
- Backlink inference
- Semantic body wikilinks (additive only)
- Lineage reconstruction
- Digital Thread relationship types (15)
- Graph scoring
- Connectivity scoring
- Traversal validation
"""

from __future__ import annotations
import re
import json
import yaml
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from collections import defaultdict
from typing import Optional


# ─── Digital Thread Relationship Types ──────────────────────────────────────

DIGITAL_THREAD_RELS = [
    "originates_from", "created_by", "creates", "executed_by",
    "reviewed_by", "approved_by", "consumes", "produces",
    "stores", "observes", "reports_to", "measured_by",
    "published_to", "promotes_to", "superseded_by",
]

# All relationship types (v3 + v4 additions)
ALL_REL_TYPES = [
    # v2/v3 types
    "derives_from", "supersedes", "validates", "produces", "implements",
    "governed_by", "depends_on", "enables", "evolves_into", "canonical_source",
    "constrained_by", "executed_by", "routes_to", "compiles", "injects",
    "observes", "audits", "stores", "publishes", "references", "contradicts",
    # v4 Digital Thread types
    "originates_from", "created_by", "creates", "reviewed_by", "approved_by",
    "consumes", "reports_to", "measured_by", "published_to", "promotes_to",
    "superseded_by",
]

# ─── File type classification ────────────────────────────────────────────────

TYPE_PATTERNS = {
    "adr": re.compile(r"ADR-\d+", re.IGNORECASE),
    "mission": re.compile(r"MISSION-\d+", re.IGNORECASE),
    "concept": re.compile(r"concepts/", re.IGNORECASE),
    "governance": re.compile(r"(governance|constitution|lakshmi|ganesha)", re.IGNORECASE),
    "dashboard": re.compile(r"(Dashboard|Cockpit|MOC)", re.IGNORECASE),
    "worker": re.compile(r"workers/", re.IGNORECASE),
    "artifact": re.compile(r"ART-", re.IGNORECASE),
    "pipeline": re.compile(r"PIPE-", re.IGNORECASE),
    "canvas": re.compile(r"\.canvas$"),
    "runtime": re.compile(r"runtime/", re.IGNORECASE),
    "moc": re.compile(r"\d+_.*MOC", re.IGNORECASE),
}

# ─── Inference rules ─────────────────────────────────────────────────────────

# (pattern_in_filename_or_content, rel_type, target_pattern)
INFERENCE_RULES = [
    # ADR supersession chain
    (r"ADR-(\d+)", "supersedes", r"ADR-{prev}"),
    # Mission → ADR
    (r"mission_(\d+)", "produces", r"ADR-\d+"),
    # ADR → Mission
    (r"ADR-(\d+)", "originates_from", r"MISSION-\d+"),
    # Governance docs → Constitution
    (r"(governance|lakshmi|ganesha)", "governed_by", "Y-OS_Constitution_v1"),
    # Dashboards → Missions
    (r"Dashboard", "reports_to", r"MISSION-\d+"),
    # Concepts → ADRs
    (r"concepts/", "canonical_source", r"ADR-\d+"),
    # Workers → Missions
    (r"workers/", "executed_by", r"MISSION-\d+"),
    # Artifacts → Workers
    (r"ART-M(\d+)-(\w+)", "created_by", r"workers/\2"),
]


@dataclass
class GraphNode:
    node_id: str
    file_path: str
    node_type: str
    title: str
    inbound: list[str] = field(default_factory=list)
    outbound: list[str] = field(default_factory=list)
    is_orphan: bool = False
    hops_to_hub: int = -1
    connectivity_score: float = 0.0


@dataclass
class GraphEdge:
    source: str
    target: str
    rel_type: str
    inferred: bool = True
    weight: float = 1.0


@dataclass
class GraphMetrics:
    total_nodes: int
    total_edges: int
    orphan_count: int
    orphan_rate: float
    avg_inbound: float
    avg_outbound: float
    density: float
    graph_quality_score: float
    connectivity_score: float
    lineage_coverage: float
    digital_thread_coverage: float
    relationship_types: int


@dataclass
class ConnectivityReport:
    generated_at: str
    mission: str
    before: GraphMetrics
    after: GraphMetrics
    orphans_resolved: int
    edges_added: int
    files_enriched: int
    digital_thread_complete: bool


class KGCv4ConnectivityEngine:
    def __init__(self, root: Path):
        self.root = root
        self.nodes: dict[str, GraphNode] = {}
        self.edges: list[GraphEdge] = []
        self.edge_set: set[tuple] = set()  # (source, target, rel_type)
        self._wikilink_re = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
        self._frontmatter_re = re.compile(r"^---\n(.*?)\n---", re.DOTALL)

    # ── Phase 1: Scan corpus ─────────────────────────────────────────────────

    def scan(self) -> None:
        """Scan all Markdown files and build initial node registry."""
        md_files = list(self.root.rglob("*.md"))
        for f in md_files:
            rel = str(f.relative_to(self.root))
            # Skip __pycache__, .git
            if any(x in rel for x in ["__pycache__", ".git", "node_modules"]):
                continue
            node_id = f.stem
            node_type = self._classify(rel)
            title = self._extract_title(f)
            self.nodes[node_id] = GraphNode(
                node_id=node_id, file_path=rel,
                node_type=node_type, title=title,
            )

        # Extract existing wikilinks
        for node_id, node in self.nodes.items():
            f = self.root / node.file_path
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for match in self._wikilink_re.finditer(content):
                target_id = match.group(1).strip()
                if target_id in self.nodes:
                    node.outbound.append(target_id)
                    self.nodes[target_id].inbound.append(node_id)
                    self._add_edge(node_id, target_id, "references", inferred=False)

    def _classify(self, rel_path: str) -> str:
        for t, pat in TYPE_PATTERNS.items():
            if pat.search(rel_path):
                return t
        return "document"

    def _extract_title(self, f: Path) -> str:
        try:
            first_lines = f.read_text(encoding="utf-8", errors="ignore").split("\n")[:20]
            for line in first_lines:
                if line.startswith("# "):
                    return line[2:].strip()[:80]
            return f.stem
        except Exception:
            return f.stem

    def _add_edge(self, src: str, tgt: str, rel: str, inferred: bool = True) -> bool:
        key = (src, tgt, rel)
        if key in self.edge_set or src == tgt:
            return False
        if tgt not in self.nodes:
            return False
        self.edge_set.add(key)
        self.edges.append(GraphEdge(src, tgt, rel, inferred))
        if tgt not in self.nodes[src].outbound:
            self.nodes[src].outbound.append(tgt)
        if src not in self.nodes[tgt].inbound:
            self.nodes[tgt].inbound.append(src)
        return True

    # ── Phase 2: Orphan detection ────────────────────────────────────────────

    def detect_orphans(self) -> list[str]:
        orphans = []
        for node_id, node in self.nodes.items():
            node.is_orphan = (len(node.inbound) == 0 and len(node.outbound) == 0)
            if node.is_orphan:
                orphans.append(node_id)
        return orphans

    def _build_adr_lookup(self) -> dict:
        """Build prefix lookup: 'ADR-0040' -> 'ADR-0040_Knowledge_Graph_Compiler'"""
        lookup = {}
        for node_id in self.nodes:
            m = re.match(r"(ADR-\d+)", node_id, re.IGNORECASE)
            if m:
                lookup[m.group(1)] = node_id
        return lookup

    # ── Phase 3: Backlink inference ──────────────────────────────────────────

    def infer_backlinks(self) -> int:
        added = 0
        node_ids = list(self.nodes.keys())
        adr_lookup = self._build_adr_lookup()

        for node_id in node_ids:
            node = self.nodes[node_id]
            fp = node.file_path

            # ADR supersession chain: ADR-0030 supersedes ADR-0029
            adr_match = re.search(r"ADR-(\d+)", node_id, re.IGNORECASE)
            if adr_match:
                num = int(adr_match.group(1))
                if num > 1:
                    prev_key = f"ADR-{num-1:04d}"
                    prev_id = adr_lookup.get(prev_key)
                    if prev_id:
                        if self._add_edge(node_id, prev_id, "supersedes"):
                            added += 1

            # Mission → ADR: scan body for ADR-XXXX references
            if node.node_type == "mission":
                try:
                    content = (self.root / fp).read_text(encoding="utf-8", errors="ignore")
                    # Frontmatter adr field
                    fm = self._parse_frontmatter(content)
                    adr_ref = fm.get("adr", "")
                    if adr_ref:
                        ref_clean = adr_ref.replace("[[", "").replace("]]", "").strip()
                        target = ref_clean if ref_clean in self.nodes else adr_lookup.get(ref_clean)
                        if target:
                            if self._add_edge(node_id, target, "produces"):
                                added += 1
                            if self._add_edge(target, node_id, "originates_from"):
                                added += 1
                    # Body ADR scan (primary method)
                    body_adrs = re.findall(r"ADR-(\d+)", content)
                    for adr_num in set(body_adrs):
                        adr_key = f"ADR-{int(adr_num):04d}"
                        target = adr_lookup.get(adr_key)
                        if target:
                            if self._add_edge(node_id, target, "produces"):
                                added += 1
                            if self._add_edge(target, node_id, "originates_from"):
                                added += 1
                except Exception:
                    pass

            # Concept → canonical ADR
            if node.node_type == "concept":
                try:
                    content = (self.root / fp).read_text(encoding="utf-8", errors="ignore")
                    fm = self._parse_frontmatter(content)
                    for rel in ["canonical_source", "governed_by", "implements"]:
                        refs = fm.get(rel, [])
                        if isinstance(refs, str):
                            refs = [refs]
                        for ref in refs:
                            target = ref.replace("[[", "").replace("]]", "").strip()
                            if target in self.nodes:
                                if self._add_edge(node_id, target, rel):
                                    added += 1

                except Exception:
                    pass

            # Governance docs → Constitution
            if node.node_type in ("governance", "adr"):
                const_id = "Y-OS_Constitution_v1"
                if const_id in self.nodes:
                    if self._add_edge(node_id, const_id, "governed_by"):
                        added += 1

            # Dashboard → Mission
            if node.node_type in ("dashboard", "moc"):
                # Link to Home MOC
                home_id = "00_Y-OS_Home"
                if home_id in self.nodes and node_id != home_id:
                    if self._add_edge(home_id, node_id, "publishes"):
                        added += 1

            # MOC → all nodes of its type
            if node.node_type == "moc":
                moc_lower = node_id.lower()
                for other_id, other in self.nodes.items():
                    if other_id == node_id:
                        continue
                    if other.node_type in moc_lower or (
                        "mission" in moc_lower and other.node_type == "mission"
                    ) or (
                        "adr" in moc_lower and other.node_type == "adr"
                    ) or (
                        "concept" in moc_lower and other.node_type == "concept"
                    ):
                        if self._add_edge(node_id, other_id, "publishes"):
                            added += 1

        return added

    def _parse_frontmatter(self, content: str) -> dict:
        m = self._frontmatter_re.match(content)
        if not m:
            return {}
        try:
            return yaml.safe_load(m.group(1)) or {}
        except Exception:
            return {}

    # ── Phase 4: Digital Thread inference ───────────────────────────────────

    def infer_digital_thread(self) -> int:
        """
        Establish CEO→Mission→ADR→Worker→Artifact→Governance→Dashboard chain.
        """
        added = 0

        # CEO directive → all missions
        ceo_nodes = [n for n in self.nodes if "CEO" in n or "ceo" in n.lower()]
        mission_nodes = [n for n in self.nodes if self.nodes[n].node_type == "mission"]
        for ceo in ceo_nodes:
            for m in mission_nodes:
                if self._add_edge(ceo, m, "creates"):
                    added += 1

        # Mission → ADR (via produces — already done in backlinks)
        # ADR → Concept (via enables)
        adr_nodes = [n for n in self.nodes if self.nodes[n].node_type == "adr"]
        concept_nodes = [n for n in self.nodes if self.nodes[n].node_type == "concept"]
        for adr in adr_nodes:
            for concept in concept_nodes:
                # Link if concept name appears in ADR content
                try:
                    content = (self.root / self.nodes[adr].file_path).read_text(
                        encoding="utf-8", errors="ignore")
                    if concept.replace("_", " ").replace("-", " ").lower() in content.lower():
                        if self._add_edge(adr, concept, "enables"):
                            added += 1
                except Exception:
                    pass

        # Artifact → Mission (via created_by)
        artifact_nodes = [n for n in self.nodes if self.nodes[n].node_type == "artifact"
                          or "ART-" in n]
        for art in artifact_nodes:
            # Extract mission number from artifact ID
            m_match = re.search(r"M(\d+)", art)
            if m_match:
                m_num = int(m_match.group(1))
                for m_node in mission_nodes:
                    if f"0{m_num:02d}" in m_node or f"-{m_num}" in m_node:
                        if self._add_edge(art, m_node, "originates_from"):
                            added += 1

        # Dashboard → Mission (reports_to)
        dashboard_nodes = [n for n in self.nodes if self.nodes[n].node_type in ("dashboard", "moc")]
        for dash in dashboard_nodes:
            for m in mission_nodes[-3:]:  # link to recent missions
                if self._add_edge(dash, m, "reports_to"):
                    added += 1

        # Governance reports → ADRs (reviewed_by)
        gov_nodes = [n for n in self.nodes if self.nodes[n].node_type == "governance"]
        for gov in gov_nodes:
            for adr in adr_nodes[-5:]:  # recent ADRs
                if self._add_edge(gov, adr, "reviewed_by"):
                    added += 1

        return added

    # ── Phase 5: Body wikilinks pass ─────────────────────────────────────────

    def add_body_wikilinks(self, dry_run: bool = False) -> tuple[int, int]:
        """
        Append ## Semantic Links section to files that lack it.
        Additive only — never modifies existing content.
        Returns (files_enriched, links_added).
        """
        files_enriched = 0
        links_added = 0

        target_types = {"adr", "mission", "concept", "governance", "dashboard", "moc"}

        for node_id, node in self.nodes.items():
            if node.node_type not in target_types:
                continue

            fp = self.root / node.file_path
            try:
                content = fp.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            # Skip if already has Semantic Links section
            if "## Semantic Links" in content:
                continue

            # Collect outbound edges for this node
            outbound_edges: dict[str, list[str]] = defaultdict(list)
            for edge in self.edges:
                if edge.source == node_id and edge.rel_type != "references":
                    outbound_edges[edge.rel_type].append(edge.target)

            if not outbound_edges:
                continue

            # Build section
            lines = ["\n\n## Semantic Links\n"]
            for rel_type, targets in sorted(outbound_edges.items()):
                unique_targets = list(dict.fromkeys(targets))[:5]  # max 5 per rel
                links = ", ".join(f"[[{t}]]" for t in unique_targets)
                lines.append(f"- **{rel_type}:** {links}")
                links_added += len(unique_targets)

            section = "\n".join(lines)

            if not dry_run:
                try:
                    with fp.open("a", encoding="utf-8") as f:
                        f.write(section)
                    files_enriched += 1
                except Exception:
                    pass
            else:
                files_enriched += 1  # count as would-be enriched

        return files_enriched, links_added

    # ── Phase 6: Scoring ─────────────────────────────────────────────────────

    def compute_metrics(self) -> GraphMetrics:
        n = len(self.nodes)
        e = len(self.edges)
        orphans = sum(1 for node in self.nodes.values() if node.is_orphan)
        orphan_rate = (orphans / n * 100) if n > 0 else 0

        avg_in = sum(len(node.inbound) for node in self.nodes.values()) / n if n > 0 else 0
        avg_out = sum(len(node.outbound) for node in self.nodes.values()) / n if n > 0 else 0

        max_edges = n * (n - 1)
        density = (e / max_edges * 100) if max_edges > 0 else 0

        # Graph Quality Score (0-100)
        # Penalize orphan rate, reward edges and types
        rel_types = len(set(edge.rel_type for edge in self.edges))
        gq = max(0, min(100,
            100
            - orphan_rate * 1.5          # orphan penalty
            + min(20, rel_types * 0.5)   # relationship diversity bonus
            + min(10, avg_in * 2)        # inbound link bonus
        ))

        # Connectivity Score (0-100)
        nodes_with_inbound = sum(1 for node in self.nodes.values() if len(node.inbound) > 0)
        connectivity = (nodes_with_inbound / n * 100) if n > 0 else 0

        # Lineage Coverage: missions with ADR links
        mission_nodes = [node for node in self.nodes.values() if node.node_type == "mission"]
        missions_with_adr = sum(
            1 for m in mission_nodes
            if any(self.nodes.get(t, GraphNode("", "", "", "")).node_type == "adr"
                   for t in m.outbound)
        )
        lineage_cov = (missions_with_adr / len(mission_nodes) * 100) if mission_nodes else 100

        # Digital Thread Coverage: nodes reachable within 3 hops from CEO/home
        dt_coverage = self._compute_dt_coverage()

        return GraphMetrics(
            total_nodes=n,
            total_edges=e,
            orphan_count=orphans,
            orphan_rate=round(orphan_rate, 1),
            avg_inbound=round(avg_in, 2),
            avg_outbound=round(avg_out, 2),
            density=round(density, 4),
            graph_quality_score=round(gq, 1),
            connectivity_score=round(connectivity, 1),
            lineage_coverage=round(lineage_cov, 1),
            digital_thread_coverage=round(dt_coverage, 1),
            relationship_types=rel_types,
        )

    def _compute_dt_coverage(self) -> float:
        """BFS from hub nodes — what % of nodes reachable within 3 hops?"""
        hub_ids = [n for n in self.nodes if n in (
            "00_Y-OS_Home", "Y-OS_Constitution_v1", "01_Missions_MOC",
            "02_ADR_MOC", "10_Concepts_MOC"
        )]
        if not hub_ids:
            hub_ids = list(self.nodes.keys())[:3]

        reachable = set(hub_ids)
        frontier = set(hub_ids)
        for _ in range(3):
            next_frontier = set()
            for node_id in frontier:
                for edge in self.edges:
                    if edge.source == node_id and edge.target not in reachable:
                        next_frontier.add(edge.target)
                    elif edge.target == node_id and edge.source not in reachable:
                        next_frontier.add(edge.source)
            reachable |= next_frontier
            frontier = next_frontier

        return (len(reachable) / len(self.nodes) * 100) if self.nodes else 0

    # ── Phase 7: Save graph ──────────────────────────────────────────────────

    def save_graph(self, path: Path, metrics: GraphMetrics) -> None:
        data = {
            "version": "v4",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "mission": "MISSION-021",
            "metrics": asdict(metrics),
            "nodes": [
                {
                    "id": n.node_id,
                    "type": n.node_type,
                    "title": n.title,
                    "inbound_count": len(n.inbound),
                    "outbound_count": len(n.outbound),
                    "is_orphan": n.is_orphan,
                }
                for n in self.nodes.values()
            ],
            "edges": [
                {"source": e.source, "target": e.target,
                 "rel_type": e.rel_type, "inferred": e.inferred}
                for e in self.edges
            ],
        }
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    # ── Phase 8: Mission Lineage Registry ────────────────────────────────────

    def build_lineage_registry(self, path: Path) -> dict:
        registry = {}
        mission_nodes = {n: node for n, node in self.nodes.items()
                         if node.node_type == "mission"}

        for m_id, m_node in mission_nodes.items():
            adrs = [t for t in m_node.outbound
                    if self.nodes.get(t, GraphNode("", "", "", "")).node_type == "adr"]
            artifacts = [t for t in m_node.outbound if "ART-" in t]
            dashboards = [t for t in m_node.outbound
                          if self.nodes.get(t, GraphNode("", "", "", "")).node_type in ("dashboard", "moc")]
            gov_events = [t for t in m_node.outbound
                          if self.nodes.get(t, GraphNode("", "", "", "")).node_type == "governance"]

            # Forward: what missions depend on this one?
            forward = [n for n, node in self.nodes.items()
                       if m_id in node.outbound and node.node_type == "mission"]
            # Backward: what missions does this depend on?
            backward = [t for t in m_node.outbound
                        if self.nodes.get(t, GraphNode("", "", "", "")).node_type == "mission"]

            registry[m_id] = {
                "mission_id": m_id,
                "title": m_node.title,
                "adrs": adrs,
                "artifacts": artifacts,
                "dashboards": dashboards,
                "governance_events": gov_events,
                "forward_missions": forward,
                "backward_missions": backward,
            }

        path.write_text(json.dumps(registry, indent=2), encoding="utf-8")
        return registry

    # ── Full pipeline ─────────────────────────────────────────────────────────

    def run(self, dry_run: bool = False) -> ConnectivityReport:
        print(f"  Scanning corpus...")
        self.scan()
        print(f"  Nodes: {len(self.nodes)}")

        # Before metrics
        self.detect_orphans()
        before = self.compute_metrics()
        print(f"  Before — Orphans: {before.orphan_count} ({before.orphan_rate}%) | "
              f"Edges: {before.total_edges} | GQ: {before.graph_quality_score}")

        print(f"  Inferring backlinks...")
        bl_added = self.infer_backlinks()
        print(f"  Backlinks inferred: {bl_added}")

        print(f"  Inferring Digital Thread...")
        dt_added = self.infer_digital_thread()
        print(f"  Digital Thread edges: {dt_added}")

        print(f"  Adding body wikilinks (dry_run={dry_run})...")
        files_enriched, links_added = self.add_body_wikilinks(dry_run=dry_run)
        print(f"  Files enriched: {files_enriched} | Links added: {links_added}")

        # After metrics
        self.detect_orphans()
        after = self.compute_metrics()
        print(f"  After  — Orphans: {after.orphan_count} ({after.orphan_rate}%) | "
              f"Edges: {after.total_edges} | GQ: {after.graph_quality_score}")

        orphans_resolved = before.orphan_count - after.orphan_count
        edges_added = after.total_edges - before.total_edges

        return ConnectivityReport(
            generated_at=datetime.now(timezone.utc).isoformat(),
            mission="MISSION-021",
            before=before,
            after=after,
            orphans_resolved=orphans_resolved,
            edges_added=edges_added,
            files_enriched=files_enriched,
            digital_thread_complete=(after.digital_thread_coverage >= 90.0),
        )
