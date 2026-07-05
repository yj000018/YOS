# AGENT Capability Model

> **Version:** v1.0.0
> **Gate:** MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE

---

## Capability Ontology

A capability is a declared, bounded ability of an agent to perform a class of operations.

**Capability statuses:**

| Status | Meaning |
|---|---|
| `proven` | Validated through direct testing or empirical evidence |
| `candidate` | Likely available but not yet formally validated |
| `unknown` | Not tested — status undetermined |
| `unsupported` | Explicitly not available for this agent |

---

## Capability Domains

| Capability ID | Name | Description |
|---|---|---|
| `reasoning` | Reasoning | Logical inference, deduction, multi-step problem solving |
| `coding` | Coding | Code generation, debugging, refactoring, architecture |
| `vision` | Vision | Image understanding, OCR, visual analysis |
| `filesystem` | Filesystem | Read/write files, navigate directories, manage artifacts |
| `api` | API | Call external APIs, parse responses, handle auth |
| `memory` | Memory | Store, retrieve, and synthesize information across sessions |
| `planning` | Planning | Decompose goals into tasks, sequence steps, manage dependencies |
| `execution` | Execution | Run code, execute commands, manage processes |

---

## Capability Schema

Each capability schema (in `03_CAPABILITIES/`) defines:

```json
{
  "capability_id": "string",
  "name": "string",
  "description": "string",
  "input_types": ["string"],
  "output_types": ["string"],
  "risk_level": "low | medium | high | critical",
  "requires_auth": "boolean",
  "requires_filesystem": "boolean",
  "requires_network": "boolean",
  "requires_human_confirmation": "boolean",
  "validated_status": "proven | candidate | unknown | unsupported"
}
```

---

## Risk Level Definitions

| Level | Description | Example |
|---|---|---|
| `low` | Read-only, no side effects | Text generation, reasoning |
| `medium` | Write to runtime, reversible | Write to sandbox filesystem |
| `high` | Write to canonical corpus, hard to reverse | Git commit to main |
| `critical` | Irreversible, secret access, automation deployment | Delete corpus, deploy automation |

---

## Capability Composition

Capabilities may be composed. A complex task may require:

```
planning + reasoning + coding + filesystem + execution
```

MPM uses capability composition to select the right executor for each Mega Prompt.

---

## Validation Policy

- `proven` requires: direct test result OR empirical session evidence
- `candidate` requires: reasonable expectation based on agent documentation
- `unknown` is the default for undeclared capabilities
- `unsupported` must be explicitly declared — never inferred from absence
