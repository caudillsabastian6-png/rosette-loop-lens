# Requirements — Rosette Loop Lens, Phase 1 (Fake Gauntlet + Night Shift/Rewind)

Phase-1 scope, decided Nov 5, 2026: **4.2 Fake Gauntlet leads; 4.4 Night
Shift + Rewind is built right behind it, in sync, on the one shared BRZ
chassis.** Slices 4.1 and 4.3 are named future phases and appear here only
where Phase 1 must not foreclose them.

## Glossary

- **Chassis** — the shared BRZ pattern both lanes run on: disposable sandbox
  per job, proposals gate, meter, run store. Consumed as a pattern (and,
  where sensible, harness code) — BRZ itself stays a standalone artifact.
- **Lane** — a family of card evidence with its own thresholds and its own
  numbers: the frozen physical core, printed pair-sheets, crew-manufactured,
  future cardstock. Lanes are never blended.
- **Gauntlet** — the attack-volley harness: manufactured fakes fired at the
  check pipeline as a build gate.
- **Night Shift** — a long unattended house job run inside containment.
- **Rewind** — the snapshot of shared state taken before a Night Shift job
  may touch it; the restore point if the job goes wrong.
- **Promotion gate** — the only door from staging to truth: designated-fake
  record check, hash verification, examiner read.
- **Receipt** — the replayable Glass Box record of a run (format fixed in
  Phase 1; UI is Phase 3).
- **Crown jewels** — the genuine/fake banks, the licence issuer private key,
  and master labels. They live outside all sandboxes.

## R1 — One shared chassis for both lanes

**User story:** As the builder, I want both slices on a single chassis, so
that containment is built and verified once instead of drifting into two
dialects.

Acceptance criteria:

1. WHEN a job of either lane starts, THE SYSTEM SHALL create a fresh,
   disposable sandbox for that job alone.
2. THE sandbox SHALL have no network access, a capped runtime, and a capped
   memory budget.
3. WHEN a job finishes or is aborted, THE SYSTEM SHALL destroy its sandbox
   and record the outcome in the run store.
4. THE proposals gate and the meter SHALL be chassis services shared by both
   lanes, not per-lane reimplementations.

## R2 — Fake Gauntlet volleys

**User story:** As the owner, I want manufactured fakes fired at the check
pipeline on every build, so a regression that lets a fake through fails
loudly instead of shipping quietly.

Acceptance criteria:

1. WHEN a volley is run, THE SYSTEM SHALL fire the registered attack sets —
   printed pair-sheet, crew-manufactured, and future cardstock — each set
   kept in its own lane and counted on its own numbers.
2. Every attack item SHALL be labelled as a manufactured/simulated attack,
   in its record and on every surface that reports it.
3. IF an item proposed for an attack set is not manufactured-lane material,
   THEN THE SYSTEM SHALL refuse it; physical-core material is never attack
   fodder and never enters a manufactured lane.
4. WHEN an item enters an attack set, THE SYSTEM SHALL first check it
   against the designated-fake record and its lane designation, and record
   that check.

## R3 — The Gauntlet gate

**User story:** As the owner, I want the build itself to fail when the
pipeline fails, so "the gate passed" always means something counted.

Acceptance criteria:

1. IF a fake in any lane escapes with a genuine-side verdict, THEN THE
   SYSTEM SHALL mark the build failed.
2. IF the forbidden-output count for a volley is above zero, THEN THE
   SYSTEM SHALL mark the build failed.
3. THE frozen physical core SHALL be judged on its own numbers alone; aux
   lanes SHALL NOT dilute or rescue core results, and core results SHALL
   NOT be reported as a blend.
4. A failed gate SHALL be reportable as failed — no re-roll, relabelling, or
   threshold change inside the same run to make it pass.

## R4 — Gauntlet scoreboard

**User story:** As a judge (or the owner), I want the volley results on one
honest scoreboard, so the containment claim is checkable at a glance.

Acceptance criteria:

1. THE scoreboard SHALL show, per lane: fired, contained, escaped,
   inconclusive — as counts, not adjectives.
2. Every figure SHALL carry its honesty label (simulated attacks, labelled
   as such), matching how BRZ reports its own volleys.
3. WHEN a volley completes, THE SYSTEM SHALL write its full result to the
   run store so the scoreboard can be re-derived, not just remembered.

## R5 — Night Shift jobs run contained, output staged

**User story:** As the owner, I want the overnight grind (pool census,
mirror verification, library organisation, Basil shadow batches) to run
where a 3 AM bug costs one sandbox — not a labelling wave.

Acceptance criteria:

1. WHEN a Night Shift job runs, THE SYSTEM SHALL run it inside the chassis
   sandbox (R1) with the job seeing only its declared inputs.
2. WHEN a job produces output, THE SYSTEM SHALL write it to a staging area
   only. A Night Shift job SHALL never write directly to master labels, the
   library, or any shared truth pile.
3. IF a job errors, exceeds its caps, or produces output that cannot be
   parsed, THEN THE SYSTEM SHALL contain the failure: no partial output is
   staged as if complete, and no follow-on action is invented on the job's
   behalf.

## R6 — Rewind before touch

**User story:** As the owner, I want a snapshot taken before any night job
may touch shared state, so a bad night is a restore, not a loss.

Acceptance criteria:

1. BEFORE a Night Shift job is permitted near shared state, THE SYSTEM
   SHALL take a Rewind snapshot of that state and record its identity.
2. THE snapshot SHALL be hash-verified at creation; IF verification fails,
   THEN the job SHALL NOT start.
3. WHEN a job or its promotion is judged bad, THE SYSTEM SHALL be able to
   restore shared state from the snapshot and SHALL record that it did.

## R7 — The promotion gate

**User story:** As the owner, I want nothing a night job produces to become
truth by itself, so the Nov 1 lesson (designated fakes reaching packets as
genuine) cannot recur by automation.

Acceptance criteria:

1. Staged output SHALL be promoted only after, in order: the
   designated-fake record check, payload hash verification against the
   recorded hashes, and an examiner read.
2. IF any step fails or mismatches, THEN THE SYSTEM SHALL abort the
   promotion, leave shared state untouched, and record the abort and its
   reason.
3. THE promotion record SHALL name which snapshot (R6) the promotion was
   made against, so any promotion can be rewound.

## R8 — A receipt for every run (Glass Box record; UI is Phase 3)

**User story:** As the owner, I want every gauntlet verdict and every night
outcome to leave a replayable receipt, so a wrong call gets audited instead
of argued about.

Acceptance criteria:

1. WHEN a check, volley, job, or promotion completes or aborts, THE SYSTEM
   SHALL emit a receipt recording: which lane and thresholds applied, which
   exemplars were compared (identities and scores), which tells fired, what
   the reader reported, and the gate decision.
2. A receipt SHALL NOT contain crown-jewel data: no bank images, no keys,
   no other users' scans.
3. THE receipt SHALL be sufficient to replay the decision — same inputs,
   same record, same outcome — without re-running the job.
4. The reader's contribution to a receipt SHALL be identity only; a receipt
   SHALL NOT record the reader as having voted on genuineness.

## R9 — Crown-jewel isolation

**User story:** As the owner, I want the banks, the issuer key, and the
master labels outside every sandbox, so no job — hostile, broken, or merely
buggy — can reach them.

Acceptance criteria:

1. THE banks, the issuer private key, and writable master labels SHALL live
   outside all sandboxes, on the house side (G1/home). The sandbox SHALL
   hold no path to them.
2. Exactly one scan and one job's declared inputs SHALL cross into a
   sandbox; exactly one result and one receipt SHALL cross out.
3. Master labels SHALL be read-only to jobs; writes happen only through the
   promotion gate (R7).
4. Other users' scans SHALL NOT be visible to a job processing someone
   else's material.

## R10 — Safety checks on everything

**User story:** As the owner, I want the gadget-flash gate pattern on every
consequential action in this system, not just the ones we remembered.

Acceptance criteria:

1. BEFORE acting on a target, THE SYSTEM SHALL prove the target's identity.
2. BEFORE writing a payload, THE SYSTEM SHALL verify it against its
   recorded hash; IF the hash mismatches, THEN THE SYSTEM SHALL abort
   instead of pushing through.
3. AFTER writing, THE SYSTEM SHALL verify the result (hash/count) and
   record the verification in the run's receipt.
4. An abort SHALL leave prior state intact and SHALL say why, in the
   receipt and on the reporting surface.

## R11 — Honesty of verdicts

**User story:** As the owner, I want the honesty law to be structural, so
no build of this system can print a verdict the evidence can't carry.

Acceptance criteria:

1. Verdict output SHALL use exactly this vocabulary: **Likely Genuine /
   Likely Counterfeit / Inconclusive**. No other verdict wording, no
   "guaranteed", no "official".
2. THE SYSTEM SHALL NOT emit canned, guessed, or placeholder verdicts.
   Inconclusive is a first-class answer whenever the evidence can't carry
   more.
3. The house reader SHALL report identity only and SHALL never vote on a
   verdict.
4. No outside model SHALL be called by any live path in this system.
5. The public launch gate (blind proof: false-flag ≤5% · catch ≥80% ·
   coverage ≥80% · forbidden outputs 0) is unchanged by this project and
   still owed before any public real-verdict release; the Gauntlet gate
   (R3) is a build gate, not a substitute for it.

## R12 — Designated-fake check before any pile

**User story:** As the owner, I want every card — sandbox-produced or not —
checked against the designated-fake record before it approaches the genuine
piles, every time, no exceptions.

Acceptance criteria:

1. WHEN any item is proposed for an attack set, a staging area, or a
   promotion, THE SYSTEM SHALL check it against the designated-fake record
   first.
2. IF the item is designated fake, THEN THE SYSTEM SHALL route it only to
   fake-side destinations and SHALL record the routing.
3. The check SHALL apply to items produced by this system's own jobs
   exactly as to items from outside.

## R13 — The BRZ freeze, and BRZ stays standalone

**User story:** As the owner, I want the LabLab exhibit untouched by this
build, so the fusion never costs BRZ its own filing or its own purity.

Acceptance criteria:

1. BEFORE Sun Nov 8, 2026, 6:00 PM ET, THIS PROJECT SHALL NOT modify the
   BRZ repository, the BRZ box, or any BRZ chassis file — in any way, for
   any reason. Work before that moment is spec work only.
2. AFTER the freeze lifts, the fusion SHALL consume BRZ's pattern (and,
   where sensible, its harness code) inside this project's own repo; the
   BRZ repo and box SHALL NOT be edited in place to serve this project.
3. BRZ's frozen core files (per the Nov 5 autopsy: `loop.py`,
   `protocol.py`, `sandbox_client.py`, `tools.py`, `config.py`,
   `inference/*`, `worker/executor.py`, `agent/requirements.txt`) SHALL be
   treated as read-only reference for the life of this project.

## R14 — No spend, no publish, no submit without the owner's word

**User story:** As the owner, I want my standing approvals to bind the
build itself, so the agent can move fast on everything except the things
that are mine to decide.

Acceptance criteria:

1. THIS PROJECT SHALL NOT purchase, subscribe, upgrade, or commit to any
   paid service. (The 4,000-credit pot is already paid for by the event;
   burning credits on build sessions is the one sanctioned spend.)
2. THIS PROJECT SHALL NOT publish a repo, post publicly, or submit the
   entry without the owner's explicit word naming that act.
3. WHEN a step would cross either line, THE SYSTEM (and the operator)
   SHALL stop and surface it instead of proceeding.
