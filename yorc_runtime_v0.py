#!/usr/bin/env python3
"""
Y-ORC Runtime MVP v0
====================
Implements the first operational Y-ORC loop:
  Registry → Trigger → Route → Execute → Artifact

Components:
  - RegistryWatcher   : Detects artifacts with status "Ready For Execution"
  - CapabilityResolver: Maps capability → worker
  - WorkerExecutor    : Invokes the selected worker
  - ArtifactWriter    : Registers the new artifact + preserves lineage
  - RuntimeLogger     : Produces execution trace
"""

import json
import os
import uuid
import datetime
import subprocess
from pathlib import Path

# ─────────────────────────────────────────────
# REGISTRY (in-memory + JSON file persistence)
# ─────────────────────────────────────────────

REGISTRY_PATH = Path(__file__).parent / "yorc_registry.json"


def load_registry() -> dict:
    if REGISTRY_PATH.exists():
        with open(REGISTRY_PATH) as f:
            return json.load(f)
    return {"artifacts": {}, "lineage": {}}


def save_registry(reg: dict):
    with open(REGISTRY_PATH, "w") as f:
        json.dump(reg, f, indent=2)


# ─────────────────────────────────────────────
# CAPABILITY MAP (declarative, never hardcoded)
# ─────────────────────────────────────────────

CAPABILITY_MAP = {
    "generate_report": {
        "worker": "Ganesha",
        "description": "Generates a structured report artifact from an execution request.",
    },
    "summarize": {
        "worker": "Saraswati",
        "description": "Produces a summary artifact from source content.",
    },
    "review": {
        "worker": "Brahma",
        "description": "Reviews and validates an artifact against architectural standards.",
    },
}


# ─────────────────────────────────────────────
# RUNTIME LOGGER
# ─────────────────────────────────────────────

LOG_PATH = Path(__file__).parent / "yorc_execution_log.jsonl"


def log(event: str, data: dict):
    entry = {
        "ts": datetime.datetime.utcnow().isoformat() + "Z",
        "event": event,
        **data,
    }
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"  [{entry['ts']}] {event}: {json.dumps(data)}")


# ─────────────────────────────────────────────
# COMPONENT 1 — REGISTRY WATCHER
# ─────────────────────────────────────────────

def registry_watcher(registry: dict) -> list[dict]:
    """Return all artifacts with status 'Ready For Execution'."""
    eligible = [
        a for a in registry["artifacts"].values()
        if a.get("status") == "Ready For Execution"
    ]
    log("WATCHER_SCAN", {"eligible_count": len(eligible),
                          "ids": [a["id"] for a in eligible]})
    return eligible


# ─────────────────────────────────────────────
# COMPONENT 2 — CAPABILITY RESOLVER
# ─────────────────────────────────────────────

def capability_resolver(artifact: dict) -> dict | None:
    """Map artifact capability to a worker definition."""
    cap_key = artifact.get("capability", "").lower().replace(" ", "_")
    worker_def = CAPABILITY_MAP.get(cap_key)
    if worker_def:
        log("CAPABILITY_RESOLVED", {
            "artifact_id": artifact["id"],
            "capability": cap_key,
            "worker": worker_def["worker"],
        })
    else:
        log("CAPABILITY_UNRESOLVED", {
            "artifact_id": artifact["id"],
            "capability": cap_key,
        })
    return worker_def


# ─────────────────────────────────────────────
# COMPONENT 3 — WORKER EXECUTOR
# ─────────────────────────────────────────────

def worker_executor(artifact: dict, worker_def: dict) -> dict:
    """
    Invoke the worker. In MVP v0, workers are implemented as local Python
    functions keyed by worker name. In future versions, workers may be
    remote agents, LLM calls, or external APIs.
    """
    worker_name = worker_def["worker"]
    log("WORKER_INVOKED", {"worker": worker_name, "input_artifact": artifact["id"]})

    workers = {
        "Ganesha": worker_ganesha,
        "Saraswati": worker_saraswati,
        "Brahma": worker_brahma,
    }

    fn = workers.get(worker_name)
    if not fn:
        raise RuntimeError(f"Worker '{worker_name}' not registered in executor.")

    result = fn(artifact)
    log("WORKER_COMPLETED", {"worker": worker_name, "output": result})
    return result


# ─────────────────────────────────────────────
# WORKERS (pluggable, capability-bound)
# ─────────────────────────────────────────────

def worker_ganesha(artifact: dict) -> dict:
    """Generate Report worker — produces a structured report artifact."""
    return {
        "type": "Report",
        "title": f"Report for {artifact['id']}",
        "content": (
            f"## Execution Report\n\n"
            f"**Source Artifact:** {artifact['id']}\n"
            f"**Mission:** {artifact.get('mission_id', 'N/A')}\n"
            f"**Capability Executed:** {artifact.get('capability', 'N/A')}\n\n"
            f"### Summary\n"
            f"Artifact `{artifact['id']}` was processed by Ganesha (Generate Report worker).\n"
            f"All execution steps completed successfully.\n\n"
            f"### Status\n"
            f"Execution complete. New artifact registered in Registry with full lineage.\n"
        ),
        "status": "Draft",
    }


def worker_saraswati(artifact: dict) -> dict:
    return {
        "type": "Summary",
        "title": f"Summary for {artifact['id']}",
        "content": f"Summary produced by Saraswati for artifact {artifact['id']}.",
        "status": "Draft",
    }


def worker_brahma(artifact: dict) -> dict:
    return {
        "type": "Review",
        "title": f"Review for {artifact['id']}",
        "content": f"Architectural review by Brahma for artifact {artifact['id']}.",
        "status": "Draft",
    }


# ─────────────────────────────────────────────
# COMPONENT 4 — ARTIFACT WRITER
# ─────────────────────────────────────────────

def artifact_writer(registry: dict, parent: dict, worker_result: dict) -> dict:
    """
    Register the new artifact in the Registry.
    Lineage: new artifact records parent_id.
    Mission graph: new artifact inherits mission_id.
    """
    new_id = f"ART-{uuid.uuid4().hex[:6].upper()}"
    new_artifact = {
        "id": new_id,
        "type": worker_result["type"],
        "title": worker_result["title"],
        "content": worker_result["content"],
        "status": worker_result["status"],
        "mission_id": parent.get("mission_id", "MISS-UNKNOWN"),
        "parent_id": parent["id"],
        "producer": "Y-ORC Runtime v0",
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
    }

    # Write artifact to registry
    registry["artifacts"][new_id] = new_artifact

    # Write lineage record
    registry["lineage"][new_id] = {
        "parent": parent["id"],
        "mission": new_artifact["mission_id"],
        "produced_by": "Y-ORC Runtime v0",
        "ts": new_artifact["created_at"],
    }

    # Update parent status to Consumed
    registry["artifacts"][parent["id"]]["status"] = "Consumed"

    log("ARTIFACT_WRITTEN", {
        "new_artifact_id": new_id,
        "parent_id": parent["id"],
        "mission_id": new_artifact["mission_id"],
        "lineage_recorded": True,
    })

    return new_artifact


# ─────────────────────────────────────────────
# MAIN ORCHESTRATION LOOP
# ─────────────────────────────────────────────

def run_yorc():
    print("\n" + "="*60)
    print("  Y-ORC Runtime MVP v0 — Starting")
    print("="*60 + "\n")

    registry = load_registry()

    # Step 1: Scan registry
    eligible = registry_watcher(registry)
    if not eligible:
        print("\n  No eligible artifacts found. Y-ORC idle.\n")
        save_registry(registry)
        return

    processed = 0
    for artifact in eligible:
        print(f"\n  Processing: {artifact['id']} — {artifact.get('title', '')}")

        # Step 2: Resolve capability
        worker_def = capability_resolver(artifact)
        if not worker_def:
            log("SKIPPED", {"artifact_id": artifact["id"], "reason": "capability_unresolved"})
            continue

        # Step 3: Execute worker
        try:
            worker_result = worker_executor(artifact, worker_def)
        except Exception as e:
            log("WORKER_ERROR", {"artifact_id": artifact["id"], "error": str(e)})
            continue

        # Step 4: Write new artifact + lineage
        new_artifact = artifact_writer(registry, artifact, worker_result)

        print(f"\n  ✅ New artifact created: {new_artifact['id']}")
        print(f"     Type    : {new_artifact['type']}")
        print(f"     Parent  : {new_artifact['parent_id']}")
        print(f"     Mission : {new_artifact['mission_id']}")
        print(f"     Status  : {new_artifact['status']}")
        processed += 1

    save_registry(registry)

    print(f"\n{'='*60}")
    print(f"  Y-ORC Runtime MVP v0 — Cycle complete")
    print(f"  Artifacts processed : {processed}")
    print(f"  Registry saved      : {REGISTRY_PATH}")
    print(f"  Execution log       : {LOG_PATH}")
    print(f"{'='*60}\n")


# ─────────────────────────────────────────────
# SEED HELPER — create ART-TEST-001
# ─────────────────────────────────────────────

def seed_test_artifact():
    """Create ART-TEST-001 in the registry for validation scenario."""
    registry = load_registry()
    registry["artifacts"]["ART-TEST-001"] = {
        "id": "ART-TEST-001",
        "type": "Execution Request",
        "title": "Test Execution Request — Generate Report",
        "content": "Validate Y-ORC Runtime MVP v0 by generating a report artifact.",
        "status": "Ready For Execution",
        "capability": "generate_report",
        "mission_id": "MISS-YORC-MVP-V0",
        "parent_id": None,
        "producer": "Yannick (Manual Seed)",
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
    }
    save_registry(registry)
    print("  Seeded ART-TEST-001 → status: Ready For Execution")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "seed":
        seed_test_artifact()
    else:
        run_yorc()
