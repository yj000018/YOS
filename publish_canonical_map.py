#!/usr/bin/env python3
"""Publish Canonical Map and append navigation footer to all 9 foundational docs."""
import subprocess, json, time

NAV_FOOTER = """

---

## Navigation — Y-OS Canonical Map

> **Foundation frozen.** See [Y-OS Canonical Map v1](Y-OS_Canonical_Map_v1.md) for the complete doctrine index.

```text
Constitution → First Principles → Identity → Operational Cycle
→ Organization → Governance → Control Plane → Orchestration → Execution
```
"""

DOCS_TO_LINK = [
    "Y-OS_Constitution_v1.md",
    "Y-OS_First_Principles_v1.md",
    "Y-OS_Definition_v1.md",
    "Y-OS_Continuity_Doctrine_v2.md",
    "Y-OS_Artifact-Centric_Manifesto_v2.md",
    "Y-OS_Operational_Cycle_v1.md",
    "Y-OS_Theory_of_Organization_v1.md",
    "Y-OS_Governance_Doctrine.md",
    "Y-OS_Control_Plane_v1.md",
    "Y-ORC_Architecture_v1.md",
]

def read_file(path):
    with open(path) as f:
        return f.read()

def append_nav(path):
    content = read_file(path)
    if "Y-OS Canonical Map" in content:
        print(f"  skip (already linked): {path}")
        return
    with open(path, 'a') as f:
        f.write(NAV_FOOTER)
    print(f"  linked: {path}")

def publish(title, content, icon="🗺️"):
    lines = content.split('\n')
    if lines and lines[0].startswith('# '):
        lines = lines[1:]
        while lines and lines[0].strip() == '':
            lines = lines[1:]
        content = '\n'.join(lines)
    payload = {"pages": [{"properties": {"title": title}, "content": content, "icon": icon}]}
    r = subprocess.run(
        ["manus-mcp-cli", "tool", "call", "notion-create-pages",
         "--server", "notion", "--input", json.dumps(payload)],
        capture_output=True, text=True
    )
    print(r.stdout[-400:] if len(r.stdout) > 400 else r.stdout)
    return r.returncode == 0

# 1. Publish Canonical Map
print("=== Publishing Y-OS Canonical Map v1 ===")
ok = publish("Y-OS Canonical Map v1", read_file("/home/ubuntu/yreg/Y-OS_Canonical_Map_v1.md"), "🗺️")
print("OK" if ok else "FAILED")
time.sleep(2)

# 2. Append nav footer to all 9 foundational docs
print("\n=== Cross-linking foundational docs ===")
for doc in DOCS_TO_LINK:
    append_nav(f"/home/ubuntu/yreg/{doc}")

print("\nDone.")
