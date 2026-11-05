# Design — Rosette Loop Lens, Phase 1

Everything below is grounded in the fusion design
(`../ROSETTE-BRZ-FUSION-DESIGN-2026-11-05.md` + its Nov 5 owner addendum)
or in the verified BRZ chassis facts from the Nov 5 autopsy
(`~/workspace/house-autopsy-2026-11-05/BRZ.md`). Where the sources are
silent, this document says **OPEN QUESTION** — it never invents a product
decision.

## 1. The chassis as it actually exists (verified, Nov 5 autopsy)

Phase 1 consumes the BRZ *pattern* — and, where sensible, its harness code —
from a chassis that is real and measured, not aspirational:

- **Surfaces:** `/health`, `/gate` (the Pocket Gate), gate state at
  `/gate/state` (there is **no** `/gate/status` route), `/inspect` and
  `/replay` (Glass Box), `/nightshift`, `/rewind`. The Gauntlet volley,
  Pocket Gate, Glass Box, Night Shift, and Rewind all exist and answer.
- **Gate behaviour:** work is proposed, not executed directly. Proposals
  wait at the gate under a threshold ($500 in the exhibit's demo state);
  the phase-2 close left 42 proposals, all pending — the gate holds until
  a decision is recorded.
- **Containment proof on record:** Gauntlet volley `55d80996e615` — 7
  attacks in, 7 contained, 0 landed, $24,346 damage prevented (simulated,
  labelled). Night Shift run `2bdfb651854e` and Rewind day `a564597892e6`
  are completed exhibits of the two mechanisms Phase 1's second lane is
  named for.
- **Failure behaviour on record:** in 9 runs the model produced 3
  unparseable replies in a row — and containment held every time: no tool
  call was dispatched from an unparseable reply, and no proposal was
  invented. This is the chassis error semantic Phase 1 inherits (see §5).
- **Frozen core:** `loop.py`, `protocol.py`, `sandbox_client.py`,
  `tools.py`, `config.py`, `inference/*`, `worker/executor.py`,
  `agent/requirements.txt` are byte-identical to the day-1 commit. `main.py`
  grew additively at the agent layer only. The run store holds 67 run
  records + 5 state files.
- **A wart that shapes our reads:** long responses over the public path can
  truncate (the gate-state read was 30,366 bytes complete via localhost,
  truncated at 12,312 publicly). Any Phase-1 read of a gate state, run
  record, or receipt must be a *complete* read — a truncated fetch is not a
  verification (R10.3).

## 2. Components

```
   HOUSE SIDE (G1 / home — outside all sandboxes)
   ┌──────────────────────────────────────────────────────────────┐
   │ Crown jewels: genuine/fake banks · issuer private key ·      │
   │ master labels (read-only to jobs; writes only via R7 gate)   │
   │ Frozen core: lane thresholds · house reader (identity only)  │
   │ Promotion gate · designated-fake record · examiner           │
   └───────────────▲──────────────────────────┬───────────────────┘
        result + receipt out        one scan / declared inputs in
   ┌───────────────┴──────────────────────────▼───────────────────┐
   │ SHARED CHASSIS (one build, both lanes)                       │
   │  Sandbox runner — fresh disposable box per job, no network,  │
   │    time + memory capped                                      │
   │  Proposals gate — nothing executes unproposed                │
   │  Meter — every run accounted                                 │
   │  Run store — every run, volley, and receipt recorded         │
   │  Receipt writer — Glass Box record format (R8)               │
   └───────▲──────────────────────────────────▲───────────────────┘
           │                                  │
   ┌───────┴────────────┐          ┌──────────┴──────────────────┐
   │ LANE A — GAUNTLET  │          │ LANE B — NIGHT SHIFT        │
   │ attack-set registry│          │ job registry (declared      │
   │ volley runner      │          │   inputs per job)           │
   │ gate evaluator(R3) │          │ staging area                │
   │ scoreboard (R4)    │          │ Rewind snapshotter (R6)     │
   └────────────────────┘          └─────────────────────────────┘
```

- **Sandbox runner.** One fresh box per job; destroyed at job end. Pattern
  source: the chassis sandbox/worker pair (autopsy: `sandbox_client.py`,
  `worker/executor.py` — read-only reference, R13.3).
- **Proposals gate + meter.** Shared services, per R1.4. The gate is where
  Night Shift promotions and any consequential chassis action wait for
  their checks (R7); the meter is what makes every run accountable in the
  run store.
- **Receipt writer.** Emits the R8 record for every check, volley, job,
  promotion, and abort. Phase 1 stores receipts as records in the run
  store (the Glass Box *format*); rendering them in an app UI is Phase 3
  (4.3) and out of scope.
- **Lane A — Fake Gauntlet (lead).** Attack sets are registered per
  manufactured lane (printed pair-sheet / crew-manufactured / future
  cardstock), each item designated-fake-checked at intake (R2.4, R12). The
  volley runner fires a set at the check pipeline inside the sandbox. The
  gate evaluator applies R3: any genuine-side escape, or forbidden outputs
  above zero, fails the build. The scoreboard renders R4 counts per lane.
- **Lane B — Night Shift + Rewind (in sync, right behind).** Jobs are
  registered with declared inputs (the named house jobs: pool census,
  mirror verification, library organisation passes, Basil shadow batches).
  A job's output lands only in staging. Before a job may touch shared
  state, the snapshotter takes and hash-verifies a Rewind snapshot (R6).
  Promotion out of staging is a separate, gated act (R7), never part of
  the job itself.

## 3. Data flow

1. **Gauntlet run:** operator (or CI) selects a registered attack set →
   items re-checked against the designated-fake record → volley fires
   inside a fresh sandbox → pipeline verdicts return per item → gate
   evaluator scores per lane → receipt + full result to the run store →
   scoreboard re-derived from the store. Build status = gate outcome.
2. **Night Shift run:** job starts in a fresh sandbox with declared inputs
   only → output written to staging → receipt emitted → job ends, sandbox
   destroyed. Shared state is untouched at this point.
3. **Promotion:** staged output + its receipt presented at the promotion
   gate → designated-fake check → hash verify against recorded hashes →
   examiner read → on pass, write proceeds against the R6 snapshot's
   identity, post-write verify runs, receipt completed. On any failure:
   abort, state untouched, abort recorded (R7, R10).
4. **Rewind:** if a promoted change is judged bad, shared state restores
   from the snapshot named in the promotion record; the restore itself is
   receipted.

## 4. Where the crown jewels sit

On the house side, outside every sandbox, per the fusion architecture:
banks, issuer private key, and master labels live on the G1/home side. The
sandbox receives one scan plus a job's declared inputs and returns one
result plus one receipt. There is no mount, path, or credential inside a
sandbox that reaches a jewel (R9). The BRZ Vultr box remains what the
autopsy found it: the hackathon exhibit and the public demo of the pattern
— Phase 1 runs at home, per the fusion design's "where it runs."

## 5. Error and abort semantics (inherited, not invented)

- **Unparseable job output** → contained. Nothing is dispatched, nothing
  is invented to fill the gap, the run is recorded as failed-contained.
  (Chassis behaviour on record, §1.)
- **Hash mismatch at any verify point** → abort before the write, prior
  state intact, reason receipted (R10.2).
- **Identity not proven** → the action does not start (R10.1).
- **Caps exceeded (time/memory)** → job killed, sandbox destroyed,
  partial output never staged as complete (R5.3).
- **Gate failure (Gauntlet)** → the build is marked failed and stays
  failed for that run; fixing the pipeline is a new run, not a re-roll
  (R3.4).

## 6. How receipts work

A receipt is the run store's Glass Box record: lane + thresholds applied,
exemplar identities and scores compared, tells fired, the reader's
identity-only report, the gate/promotion decision, and the verification
results from R10. Receipts carry identities and scores — never bank
images, never keys, never another user's scan (R8.2). Because the
scoreboard and every reported number re-derive from the run store, a
receipt is also the audit path: replay = re-read the record, and the
outcome must match (R8.3).

## 7. Open questions (sources silent — owner's or design pass's call)

1. **Integration surface.** Does the Kiroween demo surface call the live
   BRZ exhibit's routes, run a ported harness locally, or both? The fusion
   design says Phase 1 runs at home and the box "remains the exhibit and
   public demo of the pattern," but the Loop Lens judging surface (a
   functional-app URL is required) is not pinned to either. **OPEN
   QUESTION.**
2. **First real Night Shift job.** Four jobs are named (pool census,
   mirror verification, library organisation, Basil shadow batches); which
   one is wired end-to-end first as the lane's proof is not decided in the
   sources. **OPEN QUESTION** (tasks.md wires one slot for it, unnamed).
3. **Meter denomination for Rosette work.** BRZ's gate/meter speak dollars
   and budgets (the exhibit's threshold is $500). How a Rosette job's
   budget is denominated — dollars, items, minutes — is not stated in the
   fusion design. **OPEN QUESTION.**
4. **Fusion vs. Lens composition.** The prep pack frames Loop Lens as a
   photo-measurement app with containment stitched in; the fusion addendum
   makes the Gauntlet the build's "first face." How the measurement
   surface and the two containment lanes compose into one submitted app is
   a presentation decision the sources leave open (fusion design §9.2 was
   only partly answered by the addendum). **OPEN QUESTION.**
5. **Receipt retention.** How long run-store receipts are kept, and where
   they are backed up, is not specified anywhere in the sources. **OPEN
   QUESTION.**
