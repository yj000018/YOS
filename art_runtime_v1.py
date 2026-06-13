#!/usr/bin/env python3
"""
ART Runtime v1 — Agent Routing Table
=====================================
Separates capability resolution from worker selection.

Architecture:
  Y-ORC  → knows: capabilities
  ART    → knows: workers
  Worker → knows: execution

Y-ORC NEVER references agent names directly.
ART is the only layer that maps capability → worker.
Workers are replaceable without modifying Y-ORC.

Full stack:
  Artifact → Y-ORC → Capability → ART → Worker → Artifact
"""

import json
import subprocess
import datetime
from pathlib import Path

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

NOTION_DB_ID = "8cd17557-340e-4346-9850-7291face328e"
DATA_SOURCE_ID = "4ae2fa35-d24f-4c44-be88-dbb808ea14cd"
WORKER_REGISTRY_PATH = Path(__file__).parent / "worker_registry.json"
LOG_PATH = Path(__file__).parent / "art_v1_execution_log.jsonl"


def load_worker_registry() -> dict:
    with open(WORKER_REGISTRY_PATH) as f:
        return json.load(f)

# ─────────────────────────────────────────────
# NOTION MCP HELPERS (same as v1)
# ─────────────────────────────────────────────

def notion_call(tool: str, payload: dict) -> dict:
    for attempt in range(2):
        try:
            r = subprocess.run(
                ["manus-mcp-cli", "tool", "call", tool,
                 "--server", "notion", "--input", json.dumps(payload)],
                capture_output=True, text=True, timeout=45
            )
            break
        except subprocess.TimeoutExpired:
            if attempt == 1:
                return {"error": f"timeout after 2 attempts for {tool}"}
            import time; time.sleep(3)
    raw = r.stdout
    if "Tool execution result:\n" in raw:
        raw = raw.split("Tool execution result:\n", 1)[-1].strip()
    try:
        return json.loads(raw)
    except Exception:
        return {"raw": raw, "error": r.stderr}


def notion_search(query: str, page_size: int = 10) -> list[dict]:
    result = notion_call("notion-search", {
        "query": query,
        "search_type": "internal",
        "page_size": page_size
    })
    return result.get("results", [])


def notion_fetch(page_id: str) -> dict:
    return notion_call("notion-fetch", {"id": page_id})


def notion_update_page(page_id: str, properties: dict) -> dict:
    return notion_call("notion-update-page", {"id": page_id, "properties": properties})


def notion_create_in_registry(title: str, artifact_type: str, producer: str,
                               mission_id: str, capability: str,
                               parent_url: str, content: str) -> dict:
    return notion_call("notion-create-pages", {
        "parent": {"data_source_id": DATA_SOURCE_ID},
        "pages": [{
            "properties": {
                "Name": title,
                "Status": "Not started",
                "Artifact Type": artifact_type,
                "Producer": producer,
                "Consumer": "System",
                "Mission ID": mission_id,
                "Acceptance Notes": capability,
                "URI": parent_url,
                "Version": "v1.0"
            },
            "content": content,
            "icon": "📄"
        }]
    })

# ─────────────────────────────────────────────
# LOGGER
# ─────────────────────────────────────────────

def log(event: str, data: dict):
    entry = {"ts": datetime.datetime.now(datetime.UTC).isoformat(), "event": event, **data}
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"  [{entry['ts']}] {event}: {json.dumps(data)}")

# ─────────────────────────────────────────────
# COMPONENT 1 — Y-ORC WATCHER (capability-aware, worker-blind)
# ─────────────────────────────────────────────

def yorc_watcher(registry: dict) -> list[dict]:
    """
    Y-ORC polls Notion for artifacts with:
      Status = Not started
      Consumer = System
      Acceptance Notes = known capability

    Y-ORC only knows capabilities — never worker names.
    """
    known_capabilities = set(registry["capabilities"].keys())
    log("YORC_WATCHER_POLL", {"known_capabilities": sorted(known_capabilities)})

    results = notion_search("ART-RESEARCH-001 MISS-ART-V1-DEMO", page_size=5)

    seen = set()
    all_results = []
    for r in results:
        if r["id"] not in seen:
            seen.add(r["id"])
            all_results.append(r)

    eligible = []
    for page in all_results:
        # Use search result snippet + title to detect capability — avoid slow fetch when possible
        title = page.get("title", "").lower()
        highlight = page.get("highlight", "").lower()
        combined = title + " " + highlight

        # Quick capability scan from search snippet
        detected_cap = None
        for cap in known_capabilities:
            if cap in combined:
                detected_cap = cap
                break

        # Only fetch full page if we need to confirm Status/Consumer
        if detected_cap:
            full = notion_fetch(page["id"])
            text = full.get("text", "")
            is_not_started = "Not started" in text
            is_system = "System" in text
            if is_not_started and is_system:
                eligible.append({
                    "id": page["id"],
                    "title": page.get("title", ""),
                    "url": page.get("url", ""),
                    "text": text,
                    "detected_capability": detected_cap
                })

    log("YORC_WATCHER_RESULT", {
        "eligible_count": len(eligible),
        "ids": [e["id"] for e in eligible]
    })
    return eligible

# ─────────────────────────────────────────────
# COMPONENT 2 — ART CAPABILITY RESOLUTION ENGINE
# ─────────────────────────────────────────────

class ART:
    """
    Agent Routing Table.
    The ONLY component that knows worker names.
    Y-ORC calls ART.resolve(capability) — never selects workers directly.
    """

    def __init__(self, registry: dict):
        self.registry = registry["capabilities"]

    def resolve(self, capability: str) -> dict | None:
        """
        Resolve a capability to a worker.
        Returns: {worker, output_type, capability, all_workers}
        Returns None if capability unknown.
        """
        cap_def = self.registry.get(capability)
        if not cap_def:
            return None

        # Selection strategy: primary worker (future: load balancing, availability check)
        selected_worker = cap_def["primary"]

        return {
            "capability": capability,
            "worker": selected_worker,
            "output_type": cap_def["output_type"],
            "all_workers": cap_def["workers"],
            "description": cap_def.get("description", "")
        }

    def replace_worker(self, capability: str, new_worker: str):
        """
        Replace the primary worker for a capability.
        Y-ORC is never touched. Only the registry changes.
        """
        if capability in self.registry:
            old = self.registry[capability]["primary"]
            self.registry[capability]["primary"] = new_worker
            if new_worker not in self.registry[capability]["workers"]:
                self.registry[capability]["workers"].append(new_worker)
            return old
        return None

# ─────────────────────────────────────────────
# COMPONENT 3 — WORKER EXECUTOR (pluggable)
# ─────────────────────────────────────────────

def execute_worker(worker_name: str, capability: str, artifact: dict) -> dict:
    """
    Pluggable worker execution.
    Workers are identified by name only — implementation is swappable.
    """
    title = artifact.get("title", "")
    url = artifact.get("url", "")
    ts = datetime.datetime.now(datetime.UTC).isoformat()

    templates = {
        "Krishna": {
            "prefix": "Research Output",
            "body": (
                f"## Research Output\n\n"
                f"**Source Artifact:** [{title}]({url})\n"
                f"**Capability:** {capability}\n"
                f"**Worker:** Krishna (Research Agent)\n"
                f"**Routing:** Artifact → Y-ORC → `{capability}` → ART → Krishna\n"
                f"**Timestamp:** {ts}\n\n"
                f"### Research Findings\n\n"
                f"This artifact was produced by Y-OS ART Runtime v1.\n\n"
                f"The routing chain executed without human intervention:\n"
                f"1. Y-ORC detected `{title}` (Status=Not started, Consumer=System)\n"
                f"2. Y-ORC identified capability: `{capability}`\n"
                f"3. Y-ORC called ART.resolve('{capability}')\n"
                f"4. ART resolved: `{capability}` → `Krishna` (from worker_registry.json)\n"
                f"5. Y-ORC invoked Krishna\n"
                f"6. Krishna produced this artifact\n"
                f"7. ART Writer registered this artifact in the Notion Registry\n\n"
                f"### Key Validation\n\n"
                f"Y-ORC never referenced 'Krishna' directly.\n"
                f"Y-ORC only called `ART.resolve(capability)`.\n"
                f"Krishna can be replaced in worker_registry.json without modifying Y-ORC.\n\n"
                f"### Lineage\n\n"
                f"Parent: [{title}]({url})\n"
            )
        },
        "Brahma": {
            "prefix": "Architecture Review",
            "body": f"## Architecture Review\n\nProduced by Brahma via ART Runtime v1.\n\n**Source:** [{title}]({url})\n**Capability:** {capability}\n**Routing:** Y-ORC → `{capability}` → ART → Brahma\n"
        },
        "Ganesha": {
            "prefix": "Execution Report",
            "body": f"## Execution Report\n\nProduced by Ganesha via ART Runtime v1.\n\n**Source:** [{title}]({url})\n**Capability:** {capability}\n**Routing:** Y-ORC → `{capability}` → ART → Ganesha\n"
        },
        "Lakshmi": {
            "prefix": "Governance Report",
            "body": f"## Governance Report\n\nProduced by Lakshmi via ART Runtime v1.\n\n**Source:** [{title}]({url})\n**Capability:** {capability}\n**Routing:** Y-ORC → `{capability}` → ART → Lakshmi\n"
        },
        "Saraswati": {
            "prefix": "Summary",
            "body": f"## Summary\n\nProduced by Saraswati via ART Runtime v1.\n\n**Source:** [{title}]({url})\n**Capability:** {capability}\n"
        },
        "Hanuman": {
            "prefix": "Delivery",
            "body": f"## Delivery Report\n\nProduced by Hanuman via ART Runtime v1.\n\n**Source:** [{title}]({url})\n**Capability:** {capability}\n"
        },
    }

    template = templates.get(worker_name, templates["Ganesha"])
    return {
        "title": f"{template['prefix']} — {title}",
        "content": template["body"],
        "worker": worker_name,
        "capability": capability,
    }

# ─────────────────────────────────────────────
# COMPONENT 4 — ARTIFACT WRITER
# ─────────────────────────────────────────────

def artifact_writer(parent: dict, worker_result: dict, output_type: str) -> dict:
    mission_id = "MISS-ART-V1-DEMO"
    for line in parent.get("text", "").split("\n"):
        if "MISS-" in line:
            parts = [p.strip() for p in line.split() if p.startswith("MISS-")]
            if parts:
                mission_id = parts[0]
                break

    create_result = notion_create_in_registry(
        title=worker_result["title"],
        artifact_type=output_type,
        producer=worker_result["worker"],
        mission_id=mission_id,
        capability=worker_result["capability"],
        parent_url=parent.get("url", ""),
        content=worker_result["content"]
    )

    pages = create_result.get("pages", [])
    new_page = pages[0] if pages else {}
    new_id = new_page.get("id", "UNKNOWN")
    new_url = new_page.get("url", "")

    log("ARTIFACT_WRITTEN", {
        "new_id": new_id,
        "new_url": new_url,
        "parent_id": parent["id"],
        "mission_id": mission_id,
        "lineage": True
    })

    notion_update_page(parent["id"], {"Status": "Done"})
    log("PARENT_CONSUMED", {"parent_id": parent["id"], "status": "Done"})

    return {"id": new_id, "url": new_url, "title": worker_result["title"],
            "parent_id": parent["id"], "mission_id": mission_id}

# ─────────────────────────────────────────────
# MAIN ORCHESTRATION LOOP
# ─────────────────────────────────────────────

def run_art_v1():
    print("\n" + "="*65)
    print("  Y-ORC + ART Runtime v1 — Agent Routing Table")
    print("  Artifact → Y-ORC → Capability → ART → Worker → Artifact")
    print("="*65 + "\n")

    registry = load_worker_registry()
    art = ART(registry)

    log("RUNTIME_START", {"version": "ART-v1", "registry_path": str(WORKER_REGISTRY_PATH)})

    # ── STEP 1: Y-ORC watches registry (capability-aware, worker-blind)
    eligible = yorc_watcher(registry)
    if not eligible:
        print("\n  No eligible artifacts. Y-ORC idle.\n")
        log("RUNTIME_IDLE", {"reason": "no_eligible_artifacts"})
        return

    processed = 0
    for artifact in eligible:
        print(f"\n  [Y-ORC] Artifact: {artifact['id']} — {artifact.get('title', '')}")

        capability = artifact["detected_capability"]
        print(f"  [Y-ORC] Detected capability: {capability}")

        # ── STEP 2: Y-ORC calls ART.resolve() — never touches worker names
        routing = art.resolve(capability)
        if not routing:
            log("ART_UNRESOLVED", {"capability": capability})
            continue

        log("ART_RESOLVED", {
            "capability": capability,
            "worker": routing["worker"],
            "output_type": routing["output_type"],
            "all_workers": routing["all_workers"]
        })
        print(f"  [ART]   Resolved: {capability} → {routing['worker']}")

        # ── STEP 3: Y-ORC invokes worker (name comes from ART, not hardcoded)
        log("WORKER_INVOKED", {"worker": routing["worker"], "input": artifact["id"]})
        worker_result = execute_worker(routing["worker"], capability, artifact)
        log("WORKER_COMPLETED", {"worker": routing["worker"], "output": worker_result["title"]})
        print(f"  [Worker] {routing['worker']} completed → {worker_result['title']}")

        # ── STEP 4: Write artifact + lineage
        try:
            new_artifact = artifact_writer(artifact, worker_result, routing["output_type"])
        except Exception as e:
            log("WRITER_ERROR", {"error": str(e)})
            continue

        print(f"\n  ✅ New artifact in Notion Registry:")
        print(f"     ID      : {new_artifact['id']}")
        print(f"     Title   : {new_artifact['title']}")
        print(f"     URL     : {new_artifact['url']}")
        print(f"     Parent  : {new_artifact['parent_id']}")
        print(f"     Routing : {capability} → ART → {routing['worker']}")
        processed += 1

    log("RUNTIME_COMPLETE", {"processed": processed})
    print(f"\n{'='*65}")
    print(f"  ART Runtime v1 — Cycle complete | processed={processed}")
    print(f"  Log: {LOG_PATH}")
    print(f"{'='*65}\n")


# ─────────────────────────────────────────────
# DEMO: Worker replacement without modifying Y-ORC
# ─────────────────────────────────────────────

def demo_worker_replacement():
    """
    Prove: Y-ORC can be unchanged while workers are replaced.
    """
    registry = load_worker_registry()
    art = ART(registry)

    print("\n── Worker Replacement Demo ──")
    print(f"  Before: research → {art.resolve('research')['worker']}")

    old = art.replace_worker("research", "NewResearchAgent")
    print(f"  After:  research → {art.resolve('research')['worker']}")
    print(f"  (Old worker '{old}' replaced — Y-ORC code unchanged)")

    # Restore
    art.replace_worker("research", old)
    print(f"  Restored: research → {art.resolve('research')['worker']}\n")


if __name__ == "__main__":
    demo_worker_replacement()
    run_art_v1()
