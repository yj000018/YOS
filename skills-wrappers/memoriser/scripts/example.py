#!/usr/bin/env python3
"""
Memoriser — Y-OS Memory Phase 3 Wrapper
Delegates to yos_memory.MemoryIntake for canonical Git + Mem0 ingestion.
"""
import os
import sys
import argparse
from pathlib import Path

# Add YOS repo path to sys.path
YOS_REPO = os.environ.get("YOS_REPO_PATH", "/tmp/yos_audit_clone")
PIPELINE_DIR = Path(YOS_REPO) / "yos-automations" / "scripts" / "yos-llm-pipeline"
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

try:
    from yos_memory.memory_intake import MemoryIntake
except ImportError:
    print("ERROR: yos_memory package not found. Ensure YOS_REPO_PATH is correct.")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Ingest memory to Y-OS")
    parser.add_argument("--title", required=True, help="Memory title")
    parser.add_argument("--source", default="manual", help="Source of memory")
    parser.add_argument("--tags", help="Comma-separated tags")
    parser.add_argument("--file", required=True, help="Path to content file")
    args = parser.parse_args()

    if not Path(args.file).exists():
        print(f"ERROR: File not found: {args.file}")
        sys.exit(1)

    with open(args.file, 'r', encoding='utf-8') as f:
        content = f.read()

    tags = [t.strip() for t in args.tags.split(",")] if args.tags else []

    print(f"Ingesting memory: {args.title}")
    
    intake = MemoryIntake()
    result = intake.ingest(
        title=args.title,
        content=content,
        source=args.source,
        tags=tags
    )

    print("\n=== Ingestion Complete ===")
    print(f"Status: {result.get('status')}")
    print(f"Memory ID: {result.get('memory_id')}")
    print(f"Git Path: {result.get('path')}")
    print(f"Mem0 Status: {result.get('mem0_status')}")

if __name__ == "__main__":
    main()
