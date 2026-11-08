# Chassis adapter contract — Rosette Loop Lens, Phase 1

*Task 3 deliverable (`tasks.md` #3). Serves R1, R13.*

This is the contract Rosette Loop Lens builds against: the set of BRZ
chassis surfaces and behaviours Phase 1 relies on, named as they actually
exist. It is a **read-only survey**. Producing it modified nothing on the
BRZ side (R13.1–R13.3): BRZ's repo, box, and frozen-core files were not
touched, and no feature was implemented.

## How to read this contract

- **Every claim traces to the Nov 5 autopsy facts carried in
  `design.md` §1**, or to the requirements/design sections cited inline.
  The autopsy source of record is `design.md` §1 ("The chassis as it
  actually exists (verified, Nov 5 autopsy)"), which in turn is grounded
  in `~/workspace/house-autopsy-2026-11-05/BRZ.md`. This contract does not
  re-derive facts from BRZ source; it consumes design.md §1 as the
  verified record.
- A claim this contract cannot ground in design.md §1 is marked
  **UNVERIFIED** with the reason. Nothing here is invented.
- Where `design.md` §7 marks an **OPEN QUESTION**, this contract repeats
  it as open and does **not** answer it.
- **Crown jewels** (card banks, the licence issuer private key, writable
  master labels) are named only by *placement*. No jewel data, images, or
  keys appear in this contract, this repo, or the session log (steering
  fence 6; R9; R8.2).

---

## 1. Surfaces Phase 1 relies on

Source: `design.md` §1, "Surfaces". The Gauntlet volley, Pocket Gate,
Glass Box, Night Shift, and Rewind all exist on the chassis and answer.

| Surface | Role in the chassis | Phase-1 use |
|---|---|---|
| `/health` | Liveness of the chassis. | Readiness probe before a run is dispatched. |
| `/gate` | The **Pocket Gate** — where work is proposed, not executed directly. | Proposals gate for both lanes (R1.4); Night Shift promotions and any consequential action wait here (R7). |
| `/gate/state` | **Gate state lives here.** Reads the current proposals and their pending/decided status. | Source for pending-proposal reads and scoreboard re-derivation inputs. |
| `/inspect` | **Glass Box** — inspect a recorded run/receipt. | Reading receipts for replay/audit (R8.3). |
| `/replay` | **Glass Box** — replay a recorded decision from its record. | Replay = re-read the record; outcome must match (R8.3). |
| `/nightshift` | Night Shift mechanism surface. | Lane B jobs (R5); exhibit run `2bdfb651854e` on record. |
| `/rewind` | Rewind mechanism surface. | Pre-touch snapshot / restore (R6); exhibit day `a564597892e6` on record. |

**There is NO `/gate/status` route.** Gate state is read at `/gate/state`.
(Source: `design.md` §1, "Surfaces" — stated explicitly there.) Phase-1
code and tooling must target `/gate/state`; a request to `/gate/status`
is not a chassis surface and must not be assumed to exist.

---

## 2. Gate behaviour (the Pocket Gate)

Source: `design.md` §1, "Gate behaviour".

- **Work is proposed, not executed directly.** Nothing consequential runs
  unproposed; proposals wait at the gate (R1.4).
- **Proposals wait under a threshold.** In the exhibit's demo state the
  threshold is **$500**. (The threshold value is the exhibit's demo state,
  not a Rosette setting — see Open Question OQ-3 below on meter
  denomination.)
- **The gate holds until a decision is recorded.** The phase-2 close left
  **42 proposals, all pending** — evidence that the gate holds rather than
  auto-executing.

Phase-1 adapter obligation: the proposals gate and meter are **shared
chassis services** consumed by both lanes, not per-lane reimplementations
(R1.4; `design.md` §2, "Proposals gate + meter").

---

## 3. Containment exhibits on record

Source: `design.md` §1, "Containment proof on record". These are the
completed exhibits of the three mechanisms Phase 1 builds against. All
attack figures are **simulated, labelled as such** (R2.2, R4.2; steering
fences 8).

- **Gauntlet volley `55d80996e615`** — 7 attacks in, 7 contained, 0
  landed, **$24,346 damage prevented (simulated, labelled)**.
- **Night Shift run `2bdfb651854e`** — completed exhibit of the Night
  Shift mechanism (Lane B, R5).
- **Rewind day `a564597892e6`** — completed exhibit of the Rewind
  mechanism (Lane B, R6).

These identifiers are the reference exhibits; Phase 1 reproduces the
*pattern*, not these specific runs.

---

## 4. Failure semantics Phase 1 inherits

Source: `design.md` §1, "Failure behaviour on record", and §5 ("Error and
abort semantics (inherited, not invented)").

- **An unparseable model reply dispatches nothing and invents nothing.**
  On record: in 9 runs the model produced 3 unparseable replies in a row,
  and containment held every time — no tool call was dispatched from an
  unparseable reply, and no proposal was invented.
- **The run is recorded failed-contained.** This is the chassis error
  semantic Phase 1 inherits (R5.3): no partial output is staged as if
  complete, and no follow-on action is invented on the job's behalf.

Related inherited semantics (from `design.md` §5, cited for the adapter's
completeness):
- Hash mismatch at any verify point → abort before the write, prior state
  intact, reason receipted (R10.2).
- Identity not proven → the action does not start (R10.1).
- Caps exceeded (time/memory) → job killed, sandbox destroyed, partial
  output never staged as complete (R5.3).
- Gauntlet gate failure → the build is marked failed and stays failed for
  that run; fixing the pipeline is a new run, not a re-roll (R3.4).

---

## 5. Frozen core and run-store shape

Source: `design.md` §1, "Frozen core"; steering, "The BRZ freeze"; R13.3.

**Frozen-core files** — byte-identical to the day-1 commit and treated as
**read-only reference for the life of this project** (R13.3). This project
never edits them in place and never modifies them to serve Phase 1:

- `loop.py`
- `protocol.py`
- `sandbox_client.py`
- `tools.py`
- `config.py`
- `inference/*`
- `worker/executor.py`
- `agent/requirements.txt`

(`main.py` grew additively at the agent layer only — noted for context;
it is not in the Phase-1 adapter's write path.)

**Run store shape (as of the Nov 5 autopsy):** **67 run records + 5 state
files.** The run store is where every run, volley, and receipt is recorded
and from which the scoreboard and every reported number re-derive
(`design.md` §2, §6; R4.3, R8.3).

---

## 6. The complete-read rule (R10.3)

Source: `design.md` §1, "A wart that shapes our reads".

- Long responses over the **public path can truncate.** On record: the
  gate-state read was **30,366 bytes complete via localhost** but
  **truncated at 12,312 bytes publicly.**
- **A truncated fetch is not a verification.** Any Phase-1 read of a gate
  state, a run record, or a receipt must be a **complete read** before it
  counts as verified.

Phase-1 adapter obligation: before treating any gate-state, run-record, or
receipt read as verified, confirm the read is complete (e.g. read over the
localhost/complete path, or confirm the full byte length). A read that may
have truncated is treated as unverified.

---

## 7. Crown-jewel placement (names only)

Source: `design.md` §1 (context), §2 and §4 ("Where the crown jewels
sit"); R9; steering fence 6. **Placement only — no jewel data appears
here.**

- The **card banks**, the **issuer private key**, and **writable master
  labels** live on the **house side (G1 / home), outside every sandbox.**
- The sandbox holds **no mount, path, or credential** that reaches a jewel
  (R9.1). Exactly one scan plus a job's declared inputs cross in; exactly
  one result plus one receipt cross out (R9.2).
- **Master labels are read-only to jobs;** writes happen only through the
  promotion gate (R9.3, R7).
- Receipts carry exemplar identities and scores — **never bank images,
  never keys, never another user's scan** (R8.2).

This contract names placement only. No bank image, key, or jewel payload
appears in this contract, this repo, or the session log.

---

## 8. Open questions (repeated as open — not answered here)

Source: `design.md` §7. Per the contract's reading rules, these are
carried forward as **open**; this contract does not answer them.

- **OQ-1 — Integration surface.** Whether the Kiroween demo surface calls
  the live BRZ exhibit's routes, runs a ported harness locally, or both,
  is **OPEN**.
- **OQ-2 — First real Night Shift job.** Which of the four named jobs
  (pool census, mirror verification, library organisation, Basil shadow
  batches) is wired end-to-end first is **OPEN** (`tasks.md` #14 holds the
  slot, unnamed).
- **OQ-3 — Meter denomination for Rosette work.** BRZ's gate/meter speak
  dollars and budgets (exhibit threshold $500); how a Rosette job's budget
  is denominated — dollars, items, minutes — is **OPEN**.
- **OQ-4 — Fusion vs. Lens composition.** How the measurement surface and
  the two containment lanes compose into one submitted app is **OPEN**.
- **OQ-5 — Receipt retention.** How long run-store receipts are kept, and
  where they are backed up, is **OPEN**.

---

## 9. UNVERIFIED items

None. Every claim in this contract traces to `design.md` §1 (the Nov 5
autopsy facts) or to the requirements/design sections cited inline. If a
later session needs a chassis fact not present in `design.md` §1, it must
be surveyed and added here marked UNVERIFIED with its reason until the
autopsy record (or a new verified read, complete per §6) grounds it.
