# Capability Query

> **Version:** v1.0.0
> **Gate:** MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE

---

## Static Capability Query

Read `01_REGISTRY/capabilities.json` and filter by:

```python
# Find agents with proven/candidate for a given capability
def query_agents_for_capability(capability_id, min_status="candidate"):
    with open("01_REGISTRY/capabilities.json") as f:
        registry = json.load(f)
    cap = next(c for c in registry["capabilities"] if c["capability_id"] == capability_id)
    return {
        agent_id: status
        for agent_id, status in cap["agents"].items()
        if status in ["proven", "candidate"] or status == min_status
    }
```

---

## Dynamic Capability Query (YARP)

```json
{
  "yarp_version": "1.0.0",
  "message_type": "CAPABILITY_QUERY",
  "message_id": "YARP-MSG-20260705-001",
  "sender_id": "chatgpt-ag",
  "receiver_id": "manus",
  "payload": {
    "query_type": "full",
    "requested_capabilities": ["execution", "filesystem", "coding"]
  }
}
```

Expected response: `CAPABILITY_RESPONSE` with `validated_status` per capability.
