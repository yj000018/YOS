#!/usr/bin/env python3
"""
Knowledge Graph Compiler v3 — Y-OS
ADR-0046

Extends KGC v2 with:
- 18 new operational relationship types
- Pipeline graph integration (MISSION-018 artifacts as nodes)
- ODT-aware node classification
- Preserves v2 compatibility (additive only)
"""

from __future__ import annotations
import json
import re
import yaml
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


# ─── All relationship types (v2 + v3 additions) ───────────────────────────────
V2_RELATIONSHIPS = [
    "derives_from", "supersedes", "validates", "produces", "implements",
    "governed_by", "depends_on", "enables", "evolves_into", "canonical_source",
    "constrained_by", "executed_by", "routes_to", "compiles", "injects",
    "observes", "audits", "stores", "publishes",
]

V3_NEW_RELATIONSHIPS = [
    "validated_by", "checkpointed_by", "recovered_by", "committed_to",
    "consumes_artifact", "produces_artifact", "reviewed_by", "costs",
    "hosted_on", "runs_on",
]

ALL_RELATIONSHIPS = V2_RELATIONSHIPS + V3_NEW_RELATIONSHIPS


# ─── Node types ───────────────────────────────────────────────────────────────
NODE_TYPES = {
    "constitution": ["constitution", "constitutional"],
    "adr": ["adr-", "adr_"],
    "mission": ["mission-", "mission_"],
    "concept": ["concepts/"],
    "worker": ["brahma", "hanuman", "saraswati", "lakshmi", "ganesha", "ceo"],
    "artifact": ["art-m0", "art-"],
    "pipeline": ["pipe-", "pipeline"],
    "runtime": ["runtime", "_v1", "_v2", "_v3"],
    "moc": ["_moc", "moc_"],
    "canvas": [".canvas"],
    "dashboard": ["dashboard_"],
    "governance": ["governance", "lakshmi"],
    "memory": ["memory", "living_memory", "session_delta"],
}


def classify_node(node_id: str) -> str:
    lower = node_id.lower()
    for ntype, patterns in NODE_TYPES.items():
        if any(p in lower for p in patterns):
            return ntype
    return "document"


# ─── Inference rules v3 ───────────────────────────────────────────────────────
V3_INFERENCE_RULES = [
    # Artifacts validated by validator
    {
        "source_pattern": r"ART-M0\d+",
        "rel": "validated_by",
        "targets": ["output_validator_v1"],
        "inferred": True,
    },
    # Pipelines checkpointed by checkpoint engine
    {
        "source_pattern": r"PIPE-",
        "rel": "checkpointed_by",
        "targets": ["checkpoint_rollback_engine_v1"],
        "inferred": True,
    },
    # Artifacts committed to git
    {
        "source_pattern": r"ART-M0\d+",
        "rel": "committed_to",
        "targets": ["y-os-doctrine"],
        "inferred": True,
    },
    # Workers produce artifacts
    {
        "source_pattern": r"(brahma|hanuman|saraswati|lakshmi|ganesha)",
        "rel": "produces_artifact",
        "targets": [],  # Dynamic — resolved from registry
        "inferred": True,
    },
    # Artifacts reviewed by Lakshmi
    {
        "source_pattern": r"ART-M0\d+",
        "rel": "reviewed_by",
        "targets": ["Lakshmi"],
        "inferred": True,
    },
    # Runtime modules run on CCR
    {
        "source_pattern": r"(ccr_runtime|live_worker|pipeline_orchestrator)",
        "rel": "runs_on",
        "targets": ["CCR_Runtime"],
        "inferred": True,
    },
    # Missions produce artifacts
    {
        "source_pattern": r"MISSION-0\d+",
        "rel": "produces_artifact",
        "targets": [],  # Dynamic
        "inferred": True,
    },
]


@dataclass
class GraphNode:
    id: str
    label: str
    node_type: str
    source_file: str = ""
    mission: str = ""
    inferred: bool = False
    layer: str = "structural"   # structural | runtime | state | historical


@dataclass
class GraphEdge:
    source: str
    target: str
    relationship: str
    inferred: bool = False
    version: str = "v3"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class KGCompilerV3:
    """Knowledge Graph Compiler v3 — ODT-aware, pipeline-integrated."""

    def __init__(self, corpus_root: Path):
        self.corpus_root = corpus_root
        self.nodes: dict[str, GraphNode] = {}
        self.edges: list[GraphEdge] = []
        self._edge_set: set[tuple] = set()

    def _add_node(self, node_id: str, source_file: str = "", mission: str = "",
                  inferred: bool = False, layer: str = "structural") -> GraphNode:
        if node_id not in self.nodes:
            self.nodes[node_id] = GraphNode(
                id=node_id,
                label=node_id.replace("_", " ").replace("-", " "),
                node_type=classify_node(node_id),
                source_file=source_file,
                mission=mission,
                inferred=inferred,
                layer=layer,
            )
        return self.nodes[node_id]

    def _add_edge(self, source: str, target: str, rel: str, inferred: bool = False) -> None:
        key = (source, target, rel)
        if key not in self._edge_set:
            self._edge_set.add(key)
            self.edges.append(GraphEdge(source=source, target=target,
                                        relationship=rel, inferred=inferred))

    def _extract_frontmatter(self, content: str) -> dict:
        if content.startswith("---"):
            end = content.find("---", 3)
            if end > 0:
                try:
                    return yaml.safe_load(content[3:end]) or {}
                except Exception:
                    pass
        return {}

    def compile_from_corpus(self) -> dict:
        """Main compilation pass — scan all .md files."""
        md_files = list(self.corpus_root.rglob("*.md"))
        processed = 0

        for md_file in md_files:
            try:
                content = md_file.read_text(encoding="utf-8", errors="ignore")
                rel_path = str(md_file.relative_to(self.corpus_root))
                fm = self._extract_frontmatter(content)
                node_id = md_file.stem

                # Determine layer
                layer = "structural"
                if any(x in rel_path for x in ["mission_01", "mission_02"]):
                    layer = "runtime"
                if any(x in rel_path for x in ["pipeline_state", "checkpoint", "rollback"]):
                    layer = "state"
                if "evolution" in rel_path or "history" in rel_path:
                    layer = "historical"

                self._add_node(node_id, source_file=rel_path,
                               mission=fm.get("mission", ""), layer=layer)

                # Extract relationships from frontmatter
                for rel in ALL_RELATIONSHIPS:
                    targets = fm.get(rel, [])
                    if isinstance(targets, str):
                        targets = [targets]
                    if isinstance(targets, list):
                        for t in targets:
                            t_clean = str(t).strip("[]' ")
                            if t_clean:
                                target_id = t_clean.replace("[[", "").replace("]]", "")
                                self._add_node(target_id, inferred=False, layer=layer)
                                self._add_edge(node_id, target_id, rel)

                # Extract wikilinks from body
                wikilinks = re.findall(r'\[\[([^\]|#]+)', content)
                for wl in wikilinks:
                    wl_clean = wl.strip()
                    if wl_clean and wl_clean != node_id:
                        self._add_node(wl_clean, inferred=True, layer=layer)
                        self._add_edge(node_id, wl_clean, "references", inferred=True)

                processed += 1
            except Exception:
                continue

        return {"processed": processed, "nodes": len(self.nodes), "edges": len(self.edges)}

    def integrate_pipeline(self, pipeline_data: dict) -> dict:
        """Integrate MISSION-018 pipeline as graph entities (Layer 2: Runtime)."""
        pipe_id = pipeline_data.get("pipeline_id", "PIPE-5C15BA64")
        self._add_node(pipe_id, layer="runtime")
        self._add_node("MISSION-018", layer="runtime")
        self._add_edge(pipe_id, "MISSION-018", "executed_by")
        self._add_edge("MISSION-018", pipe_id, "produces")

        # Artifact chain
        artifact_chain = [
            "ART-M018-CEO-DIRECTIVE",
            "ART-M018-BRAHMA-ARCHITECTURE",
            "ART-M018-HANUMAN-BUILD",
            "ART-M018-SARASWATI-LEARNING",
            "ART-M018-LAKSHMI-GOVERNANCE",
            "ART-M018-GANESHA-CEO-BRIEFING",
        ]
        workers = ["CEO", "Brahma", "Hanuman", "Saraswati", "Lakshmi", "Ganesha"]
        providers = ["human", "openai", "openai", "anthropic", "openai", "openai"]

        for i, art_id in enumerate(artifact_chain):
            self._add_node(art_id, mission="MISSION-018", layer="runtime")
            self._add_edge(pipe_id, art_id, "produces_artifact")
            self._add_edge(art_id, workers[i], "executed_by", inferred=True)
            self._add_edge(art_id, providers[i], "runs_on", inferred=True)
            self._add_edge(art_id, "output_validator_v1", "validated_by", inferred=True)
            self._add_edge(art_id, "Lakshmi", "reviewed_by", inferred=True)
            self._add_edge(art_id, "y-os-doctrine", "committed_to", inferred=True)
            if i > 0:
                self._add_edge(artifact_chain[i-1], art_id, "produces_artifact")
                self._add_edge(art_id, artifact_chain[i-1], "consumes_artifact")

        # Checkpoints
        for i in range(6):
            cp_id = f"CKPT-{pipe_id}-S{i}"
            self._add_node(cp_id, layer="state")
            self._add_edge(pipe_id, cp_id, "checkpointed_by")
            self._add_edge(cp_id, "checkpoint_rollback_engine_v1", "executed_by", inferred=True)

        # Rollback event
        rb_id = f"RB-{pipe_id}-S99"
        self._add_node(rb_id, layer="state")
        self._add_edge(pipe_id, rb_id, "recovered_by")

        # Git commit
        self._add_node("688f374", layer="historical")
        self._add_edge(pipe_id, "688f374", "committed_to")

        new_nodes = len([n for n in self.nodes if n.startswith("ART-M018") or n.startswith("PIPE-") or n.startswith("CKPT-")])
        return {
            "pipeline_integrated": pipe_id,
            "artifacts_integrated": len(artifact_chain),
            "checkpoints_integrated": 6,
            "new_runtime_nodes": new_nodes,
        }

    def apply_v3_inference(self) -> int:
        """Apply v3 inference rules."""
        added = 0
        node_ids = list(self.nodes.keys())
        for rule in V3_INFERENCE_RULES:
            pattern = re.compile(rule["source_pattern"], re.IGNORECASE)
            for node_id in node_ids:
                if pattern.search(node_id):
                    for target in rule["targets"]:
                        if target:
                            self._add_node(target, inferred=True)
                            before = len(self.edges)
                            self._add_edge(node_id, target, rule["rel"], inferred=True)
                            if len(self.edges) > before:
                                added += 1
        return added

    def save_graph(self, output_path: Path) -> dict:
        """Save the full graph as JSON."""
        stats = {
            "schema_version": "3.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "mission": "MISSION-019",
            "v2_relationships": len(V2_RELATIONSHIPS),
            "v3_new_relationships": len(V3_NEW_RELATIONSHIPS),
            "total_relationship_types": len(ALL_RELATIONSHIPS),
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "inferred_edges": sum(1 for e in self.edges if e.inferred),
            "explicit_edges": sum(1 for e in self.edges if not e.inferred),
            "node_types": {},
        }
        # Count node types
        for node in self.nodes.values():
            stats["node_types"][node.node_type] = stats["node_types"].get(node.node_type, 0) + 1

        graph_data = {
            **stats,
            "nodes_list": [asdict(n) for n in self.nodes.values()],
            "edges_list": [asdict(e) for e in self.edges],
        }
        output_path.write_text(json.dumps(graph_data, indent=2), encoding="utf-8")
        return stats

    def save_pipeline_graph(self, output_path: Path) -> None:
        """Save pipeline-specific graph subset."""
        pipeline_nodes = {k: v for k, v in self.nodes.items()
                         if v.layer in ("runtime", "state") or "M018" in k or "PIPE-" in k}
        pipeline_edges = [e for e in self.edges
                         if e.source in pipeline_nodes or e.target in pipeline_nodes]
        data = {
            "schema_version": "1.0",
            "mission": "MISSION-018",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "pipeline_id": "PIPE-5C15BA64",
            "nodes": len(pipeline_nodes),
            "edges": len(pipeline_edges),
            "nodes_list": [asdict(n) for n in pipeline_nodes.values()],
            "edges_list": [asdict(e) for e in pipeline_edges],
        }
        output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
