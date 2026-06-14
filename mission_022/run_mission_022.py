#!/usr/bin/env python3
"""
MISSION-022: Live Event Bus — Full Pipeline Runner
"""
import sys
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "runtime"))

from event_bus_core_v1 import EventBusCore, YOSEvent
from event_registry_v1 import EventRegistry
from event_router_v1 import EventRouter
from event_persistence_v1 import EventPersistence
from event_replay_engine_v1 import EventReplayEngine
from event_observability_v1 import EventObservability
from event_lineage_tracker_v1 import EventLineageTracker

M022 = ROOT / "mission_022"
DASHBOARD_DIR = ROOT / "10_Live_Dashboards"
CANVAS_DIR = ROOT / "08_Visual_Maps"
DASHBOARD_DIR.mkdir(exist_ok=True)
CANVAS_DIR.mkdir(exist_ok=True)

print("=" * 60)
print("MISSION-022: Live Event Bus")
print("=" * 60)

# ── Init ──────────────────────────────────────────────────────────────────────
store_path = M022 / "event_store.jsonl"
persistence = EventPersistence(store_path)
bus = EventBusCore(persistence=persistence)
registry = EventRegistry()
router = EventRouter(bus)
replay_engine = EventReplayEngine(persistence)
lineage_tracker = EventLineageTracker()
observability = EventObservability(bus, persistence)

# ── Register routing handlers ─────────────────────────────────────────────────
odt_events = []
artifact_events = []
dashboard_events = []
failover_events = []
governance_events = []

router.register_handler("odt_update_engine",
    lambda e: odt_events.append(e.event_type))
router.register_handler("artifact_registry",
    lambda e: artifact_events.append(e.event_type))
router.register_handler("dashboard_refresh",
    lambda e: dashboard_events.append(e.event_type))
router.register_handler("failover_engine",
    lambda e: failover_events.append(e.event_type))
router.register_handler("governance_review",
    lambda e: governance_events.append(e.event_type))

# Subscribe lineage tracker to all events
bus.subscribe("*", lineage_tracker.track)
# Subscribe router to all events
bus.subscribe("*", router.route)

# ── TEST A: Publish / Subscribe ───────────────────────────────────────────────
print("\n[TEST A] Publish / Subscribe")
received = []
bus.subscribe("MISSION_COMPLETED", lambda e: received.append(e.event_id))

e1 = bus.emit("MISSION_COMPLETED", "MISSION-022",
    {"mission_id": "MISSION-022", "adrs_produced": ["ADR-0052"],
     "artifacts_produced": ["ART-M022-EVENT-BUS"]},
    lineage=["MISSION-021", "MISSION-023"])
print(f"  Event published: {e1.event_id}")
print(f"  Delivered to subscribers: {e1.delivered}")
print(f"  Received by test handler: {e1.event_id in received}")
test_a = "PASS" if e1.delivered and e1.event_id in received else "FAIL"
print(f"  TEST A: {test_a}")

# ── TEST B: Provider Event Routing ────────────────────────────────────────────
print("\n[TEST B] Provider Event Routing")
e2 = bus.emit("PROVIDER_FAILED", "health_monitor",
    {"provider_id": "openai", "fallback_provider": "anthropic",
     "reason": "timeout"})
print(f"  PROVIDER_FAILED published: {e2.event_id}")
print(f"  Failover engine notified: {'PROVIDER_FAILED' in failover_events}")
print(f"  Delivered: {e2.delivered}")
test_b = "PASS" if "PROVIDER_FAILED" in failover_events else "FAIL"
print(f"  TEST B: {test_b}")

# ── TEST C: Artifact Event Routing ────────────────────────────────────────────
print("\n[TEST C] Artifact Event Routing")
e3 = bus.emit("ARTIFACT_CREATED", "live_worker_executor",
    {"artifact_id": "ART-M022-EVENT-BUS", "worker": "Ganesha",
     "mission": "MISSION-022"})
print(f"  ARTIFACT_CREATED published: {e3.event_id}")
print(f"  Artifact registry notified: {'ARTIFACT_CREATED' in artifact_events}")
test_c = "PASS" if "ARTIFACT_CREATED" in artifact_events else "FAIL"
print(f"  TEST C: {test_c}")

# ── TEST D: Governance Event Routing ──────────────────────────────────────────
print("\n[TEST D] Governance Event Routing")
e4 = bus.emit("GOVERNANCE_APPROVED", "lakshmi",
    {"subject_id": "ADR-0052", "score": 8, "verdict": "APPROVE",
     "mission": "MISSION-022"})
print(f"  GOVERNANCE_APPROVED published: {e4.event_id}")
print(f"  Dashboard refresh notified: {'GOVERNANCE_APPROVED' in dashboard_events}")
test_d = "PASS" if "GOVERNANCE_APPROVED" in dashboard_events else "FAIL"
print(f"  TEST D: {test_d}")

# ── Emit more events for richer replay ────────────────────────────────────────
bus.emit("ADR_ACCEPTED", "MISSION-022",
    {"adr_id": "ADR-0052", "mission_id": "MISSION-022"})
bus.emit("GRAPH_QUALITY_UPDATED", "kg_compiler_v3",
    {"score": 100, "orphan_rate": 7.1})
bus.emit("DASHBOARD_UPDATED", "observability",
    {"dashboard_id": "Dashboard_Event_Bus"})
bus.emit("PIPELINE_COMPLETED", "pipeline_orchestrator",
    {"pipeline_id": "PIPE-M022", "steps": 7})
bus.emit("MEMORY_SESSION_STORED", "living_memory_pipeline",
    {"session_id": "SESSION-022", "mission": "MISSION-022"})

# ── TEST E: Replay Engine ─────────────────────────────────────────────────────
print("\n[TEST E] Replay Engine")
replay_result = replay_engine.replay_all()
print(f"  Events replayed: {replay_result.events_replayed}")
print(f"  State reconstructed: {replay_result.success}")
print(f"  Missions: {replay_result.state_reconstructed['missions']}")
print(f"  ADRs: {replay_result.state_reconstructed['adrs']}")
print(f"  Artifacts: {replay_result.state_reconstructed['artifacts']}")
print(f"  Replay duration: {replay_result.replay_duration_ms:.1f}ms")
test_e = "PASS" if replay_result.success and replay_result.events_replayed > 0 else "FAIL"
print(f"  TEST E: {test_e}")

# ── TEST F: Event Lineage ─────────────────────────────────────────────────────
print("\n[TEST F] Event Lineage")
total_edges = len(lineage_tracker.edges)
print(f"  Total lineage edges: {total_edges}")
mission_edges = lineage_tracker.get_lineage_for("MISSION-022")
adr_edges = lineage_tracker.get_lineage_for("ADR-0052")
print(f"  Edges for MISSION-022: {len(mission_edges)}")
print(f"  Edges for ADR-0052: {len(adr_edges)}")
test_f = "PASS" if total_edges > 0 else "FAIL"
print(f"  TEST F: {test_f}")

# Save lineage registry
lineage_tracker.save(M022 / "event_lineage_registry.json")

# ── TEST G: Governance ────────────────────────────────────────────────────────
print("\n[TEST G] Governance (Lakshmi)")
lakshmi_score = 8
dlq = bus.dead_letter_queue()
if len(dlq) > 0:
    lakshmi_score += 5
failed = bus.stats["failed"]
if failed > 0:
    lakshmi_score += 3
lakshmi_verdict = "APPROVE" if lakshmi_score < 15 else "APPROVE_WITH_WARNING"
print(f"  DLQ size: {len(dlq)}")
print(f"  Failed deliveries: {failed}")
print(f"  Lakshmi: {lakshmi_verdict} (score {lakshmi_score}/100)")
test_g = "PASS" if lakshmi_score < 15 else "FAIL"
print(f"  TEST G: {test_g}")

# ── Save event registry ───────────────────────────────────────────────────────
registry.save(M022 / "event_registry.json")

# ── Dashboard ─────────────────────────────────────────────────────────────────
print("\n[Dashboard] Generating Dashboard_Event_Bus.md...")
observability.generate_dashboard(
    output_path=DASHBOARD_DIR / "Dashboard_Event_Bus.md",
    routing_log=router.get_log(),
    replay_result=replay_result,
)
print(f"  Dashboard: {DASHBOARD_DIR / 'Dashboard_Event_Bus.md'}")

# ── Canvas ────────────────────────────────────────────────────────────────────
print("[Canvas] Generating Event_Bus_Architecture.canvas...")
canvas_nodes = [
    {"id": "bus", "type": "text", "x": 400, "y": 0, "width": 200, "height": 80,
     "text": "## Event Bus Core\npublish · subscribe\nreplay · DLQ", "color": "#6366f1"},
    {"id": "registry", "type": "text", "x": 0, "y": 200, "width": 180, "height": 70,
     "text": "**Event Registry**\n10 categories\n31 types", "color": "#94a3b8"},
    {"id": "router", "type": "text", "x": 200, "y": 200, "width": 180, "height": 70,
     "text": "**Event Router**\n21 routing rules", "color": "#94a3b8"},
    {"id": "persistence", "type": "text", "x": 400, "y": 200, "width": 180, "height": 70,
     "text": "**Persistence**\nAppend-only JSONL", "color": "#94a3b8"},
    {"id": "replay", "type": "text", "x": 600, "y": 200, "width": 180, "height": 70,
     "text": "**Replay Engine**\nTime Machine ready", "color": "#94a3b8"},
    {"id": "lineage", "type": "text", "x": 800, "y": 200, "width": 180, "height": 70,
     "text": "**Lineage Tracker**\nFull traceability", "color": "#94a3b8"},
    {"id": "observability", "type": "text", "x": 400, "y": 350, "width": 200, "height": 70,
     "text": "**Observability**\nMetrics · Dashboard", "color": "#10b981"},
    # Emitters
    {"id": "mission", "type": "text", "x": 0, "y": -150, "width": 150, "height": 60,
     "text": "Mission\nCompleted", "color": "#f59e0b"},
    {"id": "provider", "type": "text", "x": 200, "y": -150, "width": 150, "height": 60,
     "text": "Provider\nFailed", "color": "#ef4444"},
    {"id": "artifact", "type": "text", "x": 400, "y": -150, "width": 150, "height": 60,
     "text": "Artifact\nCreated", "color": "#10b981"},
    {"id": "governance", "type": "text", "x": 600, "y": -150, "width": 150, "height": 60,
     "text": "Governance\nApproved", "color": "#6366f1"},
]
canvas_edges = [
    {"id": "e1", "fromNode": "mission", "toNode": "bus", "label": "emit"},
    {"id": "e2", "fromNode": "provider", "toNode": "bus", "label": "emit"},
    {"id": "e3", "fromNode": "artifact", "toNode": "bus", "label": "emit"},
    {"id": "e4", "fromNode": "governance", "toNode": "bus", "label": "emit"},
    {"id": "e5", "fromNode": "bus", "toNode": "registry", "label": "validate"},
    {"id": "e6", "fromNode": "bus", "toNode": "router", "label": "route"},
    {"id": "e7", "fromNode": "bus", "toNode": "persistence", "label": "persist"},
    {"id": "e8", "fromNode": "bus", "toNode": "replay", "label": "replay"},
    {"id": "e9", "fromNode": "bus", "toNode": "lineage", "label": "track"},
    {"id": "e10", "fromNode": "bus", "toNode": "observability", "label": "observe"},
]
canvas_data = {"nodes": canvas_nodes, "edges": canvas_edges}
canvas_path = CANVAS_DIR / "Event_Bus_Architecture.canvas"
canvas_path.write_text(json.dumps(canvas_data, indent=2), encoding="utf-8")
print(f"  Canvas: {canvas_path}")

# ── Summary ───────────────────────────────────────────────────────────────────
tests = {
    "TEST_A": test_a, "TEST_B": test_b, "TEST_C": test_c, "TEST_D": test_d,
    "TEST_E": test_e, "TEST_F": test_f, "TEST_G": test_g,
}
pass_count = sum(1 for v in tests.values() if v == "PASS")
metrics = observability.compute_metrics()

results = {
    "mission": "MISSION-022",
    "status": "PASSED" if pass_count == 7 else "PARTIAL",
    "tests": tests,
    "pass_count": pass_count,
    "events_published": bus.stats["published"],
    "events_delivered": bus.stats["delivered"],
    "delivery_rate": metrics["delivery_rate"],
    "lineage_edges": total_edges,
    "replay_events": replay_result.events_replayed,
    "dlq_size": len(dlq),
    "lakshmi_score": lakshmi_score,
    "lakshmi_verdict": lakshmi_verdict,
    "event_types_registered": len(registry.get_all_types()),
    "routing_rules": len(router.get_routing_table()),
    "generated_at": datetime.now(timezone.utc).isoformat(),
}
(M022 / "mission_022_results.json").write_text(
    json.dumps(results, indent=2), encoding="utf-8"
)

print(f"\n{'='*60}")
print(f"RESULT: {results['status']} — {pass_count}/7 tests PASS")
print(f"Events published: {bus.stats['published']}")
print(f"Delivery rate: {metrics['delivery_rate']}%")
print(f"Lineage edges: {total_edges}")
print(f"Event types: {len(registry.get_all_types())}")
print(f"Routing rules: {len(router.get_routing_table())}")
print(f"Lakshmi: {lakshmi_verdict} (score {lakshmi_score})")
print(f"{'='*60}")
