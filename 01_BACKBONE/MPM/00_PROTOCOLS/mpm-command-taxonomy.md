# yOS MPM Command Taxonomy

> **yOS MPM — Mega Prompt Manager** (Inter-LLM Prompt Runtime & Relay System)
> Source: `mpm-frontmatter-schema.json`
> Version: 1.5.0 — Patch: YOS-BUS-MPM-FUSION-AND-DIRECT-RUNTIME-GATE-2026-07-05

---

## 1. Packet Type Taxonomy

| Packet Code | Full Name | Target LLM | Primary Use |
| :--- | :--- | :--- | :--- |
| `MP` | Mega Prompt (generic) | Generic / unspecified | Fallback or abstract Mega Prompt |
| `MPM` | Mega Prompt Manus | Manus | Execution, Git/files, long-run, multi-thread |
| `MPC` | Mega Prompt Claude | Claude | Deep critique, writing, long analysis |
| `MPX` | Mega Prompt ChatGPT | ChatGPT | Architecture, Architect & Guardian review, prompt generation |
| `MPG` | Mega Prompt Gemini | Gemini | Google/multimodal/large-context work |
| `MPP` | Mega Prompt Perplexity | Perplexity | Web research and cited external research |

> `MPA` is deprecated. Use `MP` (generic) instead.

---

## 2. Execution Modes

The yOS MPM system defines exactly three canonical execution modes, plus one alias.

| Mode | Alias | Description | Coordinator? | Workers? | Gate Required? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `sprint` | — | Small, fast, bounded task. Minimal structure. No heavy gate. Multi-thread only if trivially useful. | No | Optional | No |
| `run` | — | Powerful controlled Manus execution. Structured outputs, moderate controls. Stop after run/gate report. | No | Optional | Yes |
| `marathon` | `long run` | Maximum long-running mode. Coordinator Task plus parallel bounded Worker Tasks. Final Architect & Guardian review package. | Yes | Yes | Yes |

---

## 3. User-Level Command Library

### Creation Commands
```
Create MP sprint/run/marathon for <task>
Create MPM sprint/run/marathon for <task>
Create MPC sprint/run/marathon for <task>
Create MPX sprint/run/marathon for <task>
Create MPG sprint/run/marathon for <task>
Create MPP sprint/run/marathon for <task>
Route task to best packet type: <task>
```

> Legacy aliases still accepted: `MPM sprint create <task>`, `MPM run create <task>`, `MPM marathon create <task>`, `MPM long run create <task>`

### Primary User Command Pattern (canonical)
```
MPM sprint: <mission>
MPM run: <mission>
MPM marathon: <mission>
MPM mara: <mission>
```

Examples:
```
MPM sprint: patch transport collision protocol
MPM run: build Ludivine scope decision gate
MPM marathon: inventory Markdown and Obsidian vault recovery
```

> `MP / MPC / MPX / MPG / MPP` remain valid packet-code aliases, but `MPM` is the primary user-facing command.

### Execution Commands
```
Run next ready packet
Run next ready MPM
Run all ready packets until blocked
Run all ready MPMs until blocked
```

### Review Commands
```
Review latest executed packet
Review latest executed MPM
Review MPM <mpm_id>
Patch rejected MPM <mpm_id>
Archive accepted packets
Archive accepted MPMs
```

### Status Commands
```
Show packet queue
Show MPM queue
Show blocked packets
Show blocked MPMs
Show morning launchpad
```

---

## 4. Command Semantics

### `Run next ready packet` / `Run next ready MPM`
Manus opens the execution ledger (`inter_llm_execution_ledger.json`), finds the oldest/highest-priority entry with `status: ready_for_execution`, marks it `running`, executes it, and stops after producing the report.

### `Run all ready packets until blocked` / `Run all ready MPMs until blocked`
Same as above, but loops through all `ready_for_execution` entries in priority order. Stops on the first `blocked` result or when the queue is empty.

### `Review latest executed packet` / `Review latest executed MPM`
The Architect & Guardian LLM (ChatGPT/Claude) opens the ledger, finds the latest `executed_awaiting_guardian_review` entry, reads the packet and its report, and issues a decision (`accepted` / `rejected` / `patched`).

### `Patch rejected MPM <mpm_id>`
Moves the packet back to `draft`, applies the patch, and marks it `ready_for_execution` again.

### `Show packet queue` / `Show MPM queue`
Displays all entries with `status: ready_for_execution` in priority order.

### `Show blocked packets` / `Show blocked MPMs`
Displays all entries with `status: blocked` and their blocker notes.

### `Route task to best packet type: <task>`
Manus evaluates the task description and recommends the best packet type (MPM/MPC/MPX/MPG/MPP/MP) based on the nature of the work.

### `Show morning launchpad`
Displays the recommended next gates, which are safe, which require Architect & Guardian decision, and which are blocked.

---

## 5. Bare `MP` Command — Canon v2 (Auto-Run First)

> **See canonical reference:** `mpm-mp-command-canon-v2.md`

When the user types only:
```
MP
```

**Default behavior (no menu):**
> If exactly one unprocessed ready MP exists and no risk flag is detected: run it immediately.

Manus auto-runs the MP. No menu. No confirmation. No friction.

### Auto-Run Safety Check

Before running, Manus checks for risk flags in the MP frontmatter:
`source_mutation` · `github_push` · `gdrive_mutation` · `icloud_mutation` · `merge_execution` · `canonicalization_execution` · `destructive_deduplication` · `broad_scan` · `ludivine_content_access` · `notion_body_block_export` · `unclear_authorization` · `unclear_target`

If any flag is present or inferred → Exception Case 1.

### Exception Cases (micro-menu only)

**Exception 1 — Risk/Ambiguity:**
```
Risk or ambiguity detected.
1. Explain blocker
2. Request clarification
3. Mark MP as blocked
4. Cancel
```

**Exception 2 — Multiple Ready MPs:**
```
Multiple ready MPs found.
1. Run next recommended MP
2. Run latest MP
3. Show ready queue
4. Run specific MP by ID
5. Archive/supersede stale queue entries
6. Cancel
```

**Exception 3 — No MP Available:**
```
No ready MP found in queue.
Use `MP queue` to inspect queue/status.
```

### Explicit Commands

| Command | Behavior |
| :--- | :--- |
| `MP` | Auto-run if 1 safe ready MP; else exception handler |
| `MP next` | Run next ready MP |
| `MP latest` | Run most recently created ready MP |
| `MP queue` | Show full queue with status |
| `MP run <mp_id>` | Run specific MP by ID |
| `MP status` | Show ledger summary |
| `MP clear queue` | Archive stale entries (requires confirmation) |
| `MP archive stale` | Archive old entries (requires confirmation) |

**Deletion rule:** Never automatic. Require explicit confirmation. Move to `superseded/`. Log in `08_LOGS/`.

> **Canonical summary:** `MP` is auto-run by default, not menu-first. Menus are exception handlers, not the normal path.

---

## MPR Canonical Path

After execution, the target LLM writes the canonical Mega Prompt Report (MPR) to:
```
01_BACKBONE/MPM/06_REPORTS/awaiting-review/
```
The source LLM retrieves the MPR from that canonical path for review.
See: `00_PROTOCOLS/mpr-report-placement-protocol.md`



---

## MP Runtime Resolution

All MP/MPM runtime resolution occurs inside repo `yj000018/YOS`.

| Command | Runtime |
| :--- | :--- |
| `MP` / `MP next` / `MP queue` | `yj000018/YOS @ main / 01_BACKBONE/MPM/` |
| `MP branch=<name>` | `yj000018/YOS @ <name> / 01_BACKBONE/MPM/` |
| `MP queue branch=<name>` | `yj000018/YOS @ <name> / 01_BACKBONE/MPM/` |

**Default runtime:** `YOS/main/01_BACKBONE/MPM/`
**Explicit branch runtime:** `YOS/<branch>/01_BACKBONE/MPM/`
**Legacy bootstrap:** `kap-control-plane` is fallback only — never default runtime.

See: `07_BRANCHES/BRANCH-RUNTIME-POLICY.md`

---

## BUS-First Input Resolution (v1.5 — 2026-07-05)

MP now supports BUS-first input resolution:

```
1. If $YOS_BUS_RUNTIME_ROOT is set: read $YOS_BUS_RUNTIME_ROOT/inbox/mpm/
2. If exactly one valid MPM packet: claim it and execute.
3. Else fallback to: 01_BACKBONE/MPM/04_QUEUE/ready/*.md
4. Else fallback to Git BUS domain: 01_BACKBONE/BUS/04_DOMAINS/mpm/inbox/
5. If none: report no ready MP.
6. If multiple or risk_flags not empty: show micro-menu.
```

MPR still uses `latest-mpr.json` fast path (unchanged).
MPM/04_QUEUE/ready remains the canonical Git fallback queue.

See: `02_ADAPTERS/mpm-bus-adapter.md` and `01_BACKBONE/BUS/00_PROTOCOLS/bus-mpm-bridge-protocol.md`



---

## Optimized Local Runtime (v2 — 2026-07-05)

**Canonical wording — apply to all executor contexts:**

- `ready/*.md` is the **active queue signal** — physical presence triggers execution eligibility.
- `mp-ledger.json` remains the **JSON-first registry/history/status source of truth**.
- Executors with a local clone **batch all file writes** and push **one commit per MP execution**.
- **GitHub online/API file-by-file mode** is fallback, not preferred.
- `latest-mpr.json` is the **default fast path** for ChatGPT/Architect & Guardian MPR review.
- **ChatGPT GitHub connector calls should be minimized** — Manus/local git is the preferred writer.
- **Ledger backward compatibility:** if `ready/*.md` and ledger disagree, prefer physical `ready/*.md` for queue discovery, then reconcile ledger.

**Local CLI:** `python 01_BACKBONE/MPM/08_TOOLS/mpm.py <command>`

See: `08_TOOLS/README.md`

