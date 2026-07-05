# AGENT Roles

> **Version:** v1.0.0
> **Gate:** MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE

---

## Role Taxonomy

### Primary Roles

| Role ID | Name | Description |
|---|---|---|
| `architect` | Architect | Designs systems, defines specifications, creates architectural documents |
| `guardian` | Guardian | Reviews, validates, approves or rejects deliverables |
| `executor` | Executor | Executes Mega Prompts, runs code, produces artifacts |
| `reviewer` | Reviewer | Reviews code, documents, or artifacts for quality |
| `assimilator` | Assimilator | Ingests and structures knowledge into yOS (KAP role) |
| `orchestrator` | Orchestrator | Coordinates multi-agent workflows |
| `operator` | Operator | Human operator — manages, configures, approves |
| `observer` | Observer | Read-only monitoring and audit |

### YARP-Specific Roles

| Role ID | YARP Message Types | Description |
|---|---|---|
| `yarp_sender` | EXECUTE_MP, QUERY, PING | Initiates YARP messages |
| `yarp_receiver` | ACK, NACK, PROGRESS, RESULT, ERROR | Receives and processes YARP messages |
| `yarp_relay` | All | Forwards YARP messages between agents |
| `yarp_guardian` | APPROVE, REJECT | Approves or rejects YARP-carried artifacts |

---

## Agent-to-Role Mapping (v1.0.0)

| Agent | Primary Roles | YARP Roles |
|---|---|---|
| ChatGPT (A&G) | architect, guardian | yarp_sender, yarp_guardian |
| Manus | executor, orchestrator | yarp_receiver, yarp_sender |
| Claude | architect, reviewer | yarp_sender, yarp_receiver |
| Gemini | reviewer, assimilator | yarp_receiver |
| Codex | executor | yarp_receiver |
| Human Operator | operator, guardian | yarp_sender, yarp_guardian |

---

## Role Constraints

- An agent may hold multiple roles simultaneously.
- Role assignment does not grant permissions — trust level governs permissions.
- The `guardian` role requires minimum trust level T4 (canonical_writer) for corpus changes.
- The `operator` role (human) defaults to T5 (guardian_approved) for the session owner.
