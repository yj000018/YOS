#!/usr/bin/env python3
import subprocess, json, time

def read_file(path):
    with open(path) as f:
        return f.read()

def publish(title, content, icon="⚖️"):
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
    print(f"\n=== {title} ===")
    print(r.stdout[-400:] if len(r.stdout) > 400 else r.stdout)
    return r.returncode == 0

docs = [
    ("Y-OS Constitution v1", "/home/ubuntu/yreg/Y-OS_Constitution_v1.md", "⚖️"),
    ("ADR-0024: Y-OS Constitution", "/home/ubuntu/yreg/ADR-0024_Y-OS_Constitution.md", "📋"),
]

for title, path, icon in docs:
    ok = publish(title, read_file(path), icon)
    print("OK" if ok else "FAILED")
    time.sleep(2)

print("\nDone.")
