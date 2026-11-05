# Steering — Rosette Loop Lens (house rules, every session)

This file lives at `/.kiro/steering/steering.md` in the project repo and is
in force for **every** Kiro session on this project. If a session prompt and
this file ever conflict, this file wins and the conflict gets noted in the
session log.

## What this project is

**Rosette Loop Lens** (Kiroween 2026, **Frankenstein** category).
Public line: **"Rosette — contained by Blast Radius Zero."**
Rosette reads the card. Blast Radius Zero makes sure nothing Rosette
touches can hurt the collection, the keys, or the truth pile.

Phase 1 builds two slices, in sync, on one shared BRZ chassis:
**4.2 Fake Gauntlet** (lead) and **4.4 Night Shift + Rewind** (right behind
it). Slices 4.1 and 4.3 are future phases — never build ahead into them.

## The fences (non-negotiable)

1. **Verdict vocabulary is exactly three lanes:** *Likely Genuine /
   Likely Counterfeit / Inconclusive.* No other verdict wording. Never
   "guaranteed", never "official", never a canned or guessed verdict.
   Inconclusive is a first-class, honest answer.
2. **The reader never votes.** The house reader reports identity only.
   Nothing in this project may record it as judging genuineness.
3. **No outside model on any live path.** If a design seems to need one,
   stop and surface it; do not wire one in.
4. **Designated-fake check first.** Any card, item, or output — including
   this system's own output — is checked against the designated-fake
   record before it approaches any genuine pile, staging area, or
   promotion. Every time, no exceptions.
5. **Safety checks on everything.** Prove the target's identity before
   acting. Verify payloads against recorded hashes before writing. Verify
   the result after writing. Abort on any mismatch — never push through.
   An abort leaves prior state intact and says why.
6. **Crown jewels stay outside.** The card banks, the licence issuer
   private key, and writable master labels are never inside a sandbox,
   never in this repo, never in a receipt, never in a log. Receipts carry
   exemplar identities and scores — never bank images or keys.
7. **One scan in, one result + receipt out.** Sandboxes are fresh and
   disposable per job: no network, capped time, capped memory.
8. **Lanes never blend.** The frozen physical core is judged on its own
   numbers; manufactured lanes (printed pair-sheet, crew-manufactured,
   future cardstock) never dilute or rescue it, and attacks are always
   labelled simulated/manufactured.
9. **Nothing becomes truth by itself.** Night-job output lands in staging
   and reaches truth only through the promotion gate: designated-fake
   check → hash verify → examiner read.

## The BRZ freeze

- **Before Sun Nov 8, 2026, 6:00 PM ET:** do not modify the BRZ repository,
  the BRZ box, or any BRZ file, for any reason. Work on this project before
  that moment is spec work in this repo only.
- **After the freeze:** this project consumes BRZ's *pattern* (and, where
  sensible, harness code) inside its own repo. Never edit BRZ in place to
  serve this project. BRZ's frozen core files (`loop.py`, `protocol.py`,
  `sandbox_client.py`, `tools.py`, `config.py`, `inference/*`,
  `worker/executor.py`, `agent/requirements.txt`) are read-only reference
  for the life of this project.

## Money and publishing

- **Spending money needs the owner's word first** — the exact item, in the
  moment. No purchases, subscriptions, plan upgrades, or paid APIs. The
  4,000 Kiro credits are the event's own pot; burning them on build
  sessions is the only sanctioned spend.
- **No publishing without the owner's word:** no public repo push, no
  posts, no submission. Drafts and local work are always fine.

## Working habits

- **One task per session.** Work the single task named in `tasks.md`; check
  its box only when its verification has actually run. If a task won't fit
  one session, split it in `tasks.md` rather than grinding.
- **Total record.** Every session appends to the session log: date, task,
  what changed, how it was verified, credits burned. Work that isn't
  recorded didn't happen.
- **Honesty law.** Never fake a result: no stubbed verdicts, no
  placeholder numbers presented as measured, no re-rolled gate runs. A
  failed check is reported as failed. If you cannot verify something, say
  so in the log instead of smoothing it over.
- **Scope discipline.** If you believe a task needs work outside
  `tasks.md`, write that belief in the session log and stop at the task's
  edge. The spec is amended deliberately, never drifted into.
- **Naming.** Products keep their names: **Rosette** is the face,
  **Blast Radius Zero (BRZ)** is the engine, **Basil** is the house reader
  (identity only). People and machines in house records: Sabastian (the
  owner), the G1 (house machine), Penguin (spare), Allie (frozen fallback
  machine).
