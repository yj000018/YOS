#!/usr/bin/env python3
"""Fix lineage coverage by using body ADR references, not just frontmatter."""
import sys
import re
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "runtime"))

from kgc_v4_connectivity_engine import KGCv4ConnectivityEngine

# Check what mission files look like
mission_files = list(ROOT.rglob("MISSION-*.md"))[:5]
print("=== Sample mission files ===")
for f in mission_files:
    content = f.read_text(errors="ignore")[:600]
    body_adrs = re.findall(r"ADR-\d+", content)
    print(f"{f.name}: body_ADRs={body_adrs[:5]}")

# Rebuild engine and patch lineage using body ADR mentions
engine = KGCv4ConnectivityEngine(ROOT)
engine.scan()

# Fix: for each mission node, scan body for ADR mentions and add edges
added = 0
mission_nodes = {n: node for n, node in engine.nodes.items()
                 if node.node_type == "mission"}

for m_id, m_node in mission_nodes.items():
    fp = ROOT / m_node.file_path
    try:
        content = fp.read_text(errors="ignore")
        # Find all ADR references in body
        adrs_in_body = re.findall(r"ADR-(\d+)", content)
        for adr_num in set(adrs_in_body):
            adr_id = f"ADR-{int(adr_num):04d}"
            if adr_id in engine.nodes:
                if engine._add_edge(m_id, adr_id, "produces"):
                    added += 1
                if engine._add_edge(adr_id, m_id, "originates_from"):
                    added += 1
    except Exception as e:
        print(f"  Error {m_id}: {e}")

print(f"\nAdded {added} mission-ADR edges via body scan")

# Recompute lineage
mission_nodes_updated = {n: node for n, node in engine.nodes.items()
                         if node.node_type == "mission"}
missions_with_adr = sum(
    1 for m in mission_nodes_updated.values()
    if any(engine.nodes.get(t, type("", (), {"node_type": ""})()).node_type == "adr"
           for t in m.outbound)
)
total_missions = len(mission_nodes_updated)
lineage_cov = (missions_with_adr / total_missions * 100) if total_missions > 0 else 0
print(f"Missions with ADR links: {missions_with_adr}/{total_missions} = {lineage_cov:.1f}%")
