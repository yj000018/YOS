# yOS MPM — Manus Fetch-and-Run Protocol (MPM Adapter)

> **yOS MPM — Mega Prompt Manager** (Inter-LLM Prompt Runtime & Relay System)
> Manus Adapter — Packet type: `MPM`
> Version: 1.5.0 — Patch: YOS-BUS-MPM-FUSION-AND-DIRECT-RUNTIME-GATE-2026-07-05

---

## 1. Purpose

This protocol allows Manus to execute MPMs without copy-paste. The user issues a single command; Manus reads the ledger, fetches the MPM, executes it, and reports back.

## 2. Trigger Command

**Canonical user command pattern:**
```
MPM sprint: <mission>
MPM run: <mission>
MPM marathon: <mission>
```

**Legacy execution commands (still accepted):**
```
Run next ready packet
Run next ready MPM
```

Or for a specific packet:
```
Run MPM <mpm_id>
```

**Bare `MP` command** — auto-runs the next safe ready MP (Canon v2). See `mpm-mp-command-canon-v2.md` and §6.

## 3. Execution Steps

### Step 1 — Open the Ledger
Read `kap-control-plane/00_META/inter_llm_execution_ledger.json`.

> **Collision pre-check:** Verify the target MPM is not already `running`, `executed_awaiting_guardian_review`, or `guardian_accepted` in the ledger. If it is, do not re-claim. See `mpm-transport-collision-rules.md` Rule 4.

### Step 2 — Find the Next Ready MPM
Find the oldest entry with `status: ready_for_execution`. If multiple exist, use priority order (highest-priority first, then oldest `created_at`).

### Step 3 — Claim and Mark as Running (Atomic)
- **Check for duplicate:** If file already exists in `02_MPMs/running/`, skip the move and verify ledger consistency.
- Update the ledger JSON entry: `status → running`, `started_at → now`, `mpm_path → 02_MPMs/running/...`.
- Move the MPM file from `ready/` to `02_MPMs/running/` (`git mv`).
- Regenerate the MD ledger view from JSON.
- **Single commit** (file move + ledger update together): `kap-control-plane: MPM-XXXXXX — claimed, status=running`.
- **Push immediately** — do not defer. This prevents GGG from committing a conflicting state.
- If push fails: pull `--no-rebase -X ours`, resolve duplicates, push again. See `mpm-transport-collision-rules.md` Rule 5.

### Step 4 — Read the MPM
Read the full MPM file. Parse the frontmatter. Validate against `mpm-frontmatter-schema.json`.

### Step 5 — Execute According to Mode
- `sprint`: Execute directly, minimal structure.
- `run`: Execute with full gate protocol.
- `marathon`: Activate Coordinator-Worker pattern (see `mpm-coordinator-worker-pattern.md`).

### Step 6 — Produce Required Outputs
Write all files listed in `expected_outputs`. Follow the output contract (`mpm-output-contract.md`).

### Step 7 — Produce the Report
Write the gate/execution report to `report_path`.

### Step 8 — Update MPM Frontmatter
Update the MPM file: `status → executed_awaiting_guardian_review`, `completed_at → now`, `execution_commit`, `control_plane_commit`.

### Step 9 — Update the Ledger JSON
Update the entry in `inter_llm_execution_ledger.json`. Regenerate the MD view.

### Step 10 — Commit Everything
```
git commit -m "kap-control-plane: MPM-XXXXXX — executed, awaiting Architect & Guardian review"
git commit -m "yos-cognitive-os: MPM-XXXXXX — gate outputs committed"
```

### Step 11 — STOP
Do not proceed to the next MPM unless the command was `Run all ready MPMs until blocked`.

---

## 4. Blocked Execution Protocol

If blocked during execution:
1. Write a blocker report to `06_REPORTS/BLOCKER-<MPM_ID>-<DATE>.md`.
2. Update ledger JSON: `status → blocked`, `notes → blocker description`.
3. Move MPM to `02_MPMs/blocked/`.
4. Commit.
5. If `Run all ready MPMs until blocked` was the command, stop here.

---

## 5. Bootstrap Note

> `kap-control-plane` is the current bootstrap runtime repository for the yOS MPM system.
> Final conceptual home: **yOS Backbone / MPM** (pending `MPM-BACKBONE-TOPOLOGY-DECISION-GATE` Architect & Guardian approval).
> KAP is one consumer of MPM, not the owner of the protocol.

---

## 6. Bare `MP` Command — Canon v2 (Auto-Run First)

> **Full spec:** `mpm-mp-command-canon-v2.md`

When user types only `MP`:

**If 1 safe ready MP exists → auto-run immediately. No menu.**

**Exception handlers (micro-menu only):**
- Risk/ambiguity detected → 4-option blocker menu
- Multiple ready MPs → 6-option queue menu
- No MP available → short info message only

**Deletion rule:** Never automatic. Require explicit confirmation. Move to `superseded/`. Log to `08_LOGS/`.

---

## 7. How to Create a Packet (Manus)

```
Create MPM run <gate/task description>
Create MP sprint <task>
```

Manus will:
1. Generate a new packet file with a valid `mpm_id` (e.g., `MPM-YYYYMMDD-SLUG`), `packet_type`, `target_llm`, and full frontmatter.
2. Save it to `02_MPMs/drafts/`.
3. Add a `draft` entry to the ledger JSON.
4. Regenerate the MD ledger view.
5. Commit.

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

MP now supports BUS-first input resolution. The resolution order is:

```
1. If $YOS_BUS_RUNTIME_ROOT is set: read $YOS_BUS_RUNTIME_ROOT/inbox/mpm/
2. If exactly one valid MPM packet: claim it (move to workspace/mpm/) and execute.
3. Else fallback to: 01_BACKBONE/MPM/04_QUEUE/ready/*.md
4. Else fallback to Git BUS domain: 01_BACKBONE/BUS/04_DOMAINS/mpm/inbox/
5. If none: report no ready MP.
6. If multiple or risk_flags not empty: show micro-menu.
```

MPR still uses `latest-mpr.json` fast path (unchanged):
```
1. Read 01_BACKBONE/MPM/06_REPORTS/indexes/latest-mpr.json
2. Read latest_mpr_path
3. A&G review
```

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

