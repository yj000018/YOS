#!/usr/bin/env python3
import sys
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "runtime"))

from kgc_v4_connectivity_engine import KGCv4ConnectivityEngine

engine = KGCv4ConnectivityEngine(ROOT)
engine.scan()

missions = [(n, v.file_path) for n, v in engine.nodes.items() if v.node_type == "mission"][:8]
adrs = [(n, v.file_path) for n, v in engine.nodes.items() if v.node_type == "adr"][:8]
print("Missions:", missions)
print("ADRs:", adrs)

# Check if ADR-0040 is in nodes
print("\nADR-0040 in nodes:", "ADR-0040" in engine.nodes)
print("ADR-0040_Knowledge_Graph_Compiler in nodes:", "ADR-0040_Knowledge_Graph_Compiler" in engine.nodes)

# Check mission node outbound
m_sample = missions[0] if missions else None
if m_sample:
    m_id = m_sample[0]
    node = engine.nodes[m_id]
    print(f"\nMission {m_id} outbound: {node.outbound[:10]}")
    print(f"Mission {m_id} node_type: {node.node_type}")

    # Try body ADR scan
    fp = ROOT / node.file_path
    content = fp.read_text(errors="ignore")
    body_adrs = re.findall(r"ADR-(\d+)", content)
    print(f"Body ADRs in {m_id}: {body_adrs[:5]}")

    # Check if those ADR IDs exist in nodes
    for adr_num in body_adrs[:3]:
        # Try different ID formats
        for fmt in [f"ADR-{int(adr_num):04d}", f"ADR-{adr_num}"]:
            print(f"  {fmt} in nodes: {fmt in engine.nodes}")
        # Try finding by partial match
        matches = [k for k in engine.nodes if f"ADR-{adr_num}" in k or f"ADR-0{adr_num}" in k]
        print(f"  Partial matches for ADR-{adr_num}: {matches[:3]}")
