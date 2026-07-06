# DISC-002 — BUS ≠ Protocol

**ID:** DISC-002
**Title:** BUS is a transport substrate, not a protocol
**Status:** canonical
**First seen:** MPM-20260705-YOS-AGENT-RELAY-PROTOCOL-CONSTITUTION-GATE

---

## The Discovery

YARP was initially placed inside BUS. The correction: YARP and BUS are peers.

BUS = physical/transport layer
YARP = semantic/protocol layer

## Canonical Phrase

"YARP defines meaning. BUS moves packets."

## Architectural Consequence

YARP gets its own backbone module: `01_BACKBONE/YARP/`
BUS remains the transport substrate.

## Sources

- YARP-CONSTITUTION.md v1.1.0 (Article I)
- MPM-20260705-YOS-YARP-CONSTITUTION-CLARIFICATION-PATCH-GATE-REPORT.md
