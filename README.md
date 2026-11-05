# Rosette Loop Lens

**Rosette — contained by Blast Radius Zero.**

Rosette reads the card. Blast Radius Zero (BRZ) makes sure nothing Rosette
touches can hurt the collection, the keys, or the truth pile.

> Kiroween 2026 · **Frankenstein** category. This repository is the Kiro spec
> pack and (in later tasks) the Phase-1 build for the Rosette + BRZ fusion.

## What this is

Rosette Loop Lens fuses two pieces on **one shared BRZ chassis**:

- **Rosette** — the face. Reads a card and reports a verdict in exactly three
  lanes: *Likely Genuine / Likely Counterfeit / Inconclusive.*
- **Blast Radius Zero (BRZ)** — the engine. Disposable per-job sandboxes, a
  proposals gate, a meter, a run store, and the Glass Box receipt format, so
  nothing a job touches can reach the crown jewels or become truth by itself.
- **Basil** — the house reader. Reports identity only; never votes on a verdict.

Phase 1 builds two slices in sync on that chassis:

- **Lane A — Fake Gauntlet (lead):** manufactured fakes fired at the check
  pipeline as a build gate.
- **Lane B — Night Shift + Rewind (in sync):** long unattended house jobs run
  inside containment, snapshotted before they touch shared state, and promoted
  to truth only through a gate.

## The fences (non-negotiable)

- Verdict vocabulary is exactly three lanes — nothing "guaranteed" or "official".
- The house reader reports identity only; it never votes.
- No outside model on any live path.
- Designated-fake check first, on everything — including this system's own output.
- Crown jewels (card banks, issuer private key, master labels) stay outside every
  sandbox, this repo, every receipt, and every log.
- One scan in, one result + receipt out; sandboxes are fresh and disposable.

See [`.kiro/steering/steering.md`](.kiro/steering/steering.md) for the full
house rules in force every session.

## Repository layout

```
.
├── .kiro/                 # steering + the Rosette Loop Lens spec (committed, never gitignored)
│   ├── steering/          # house rules in force every session
│   └── specs/             # requirements · design · tasks
├── src/
│   └── rosette_loop_lens/
│       ├── chassis/       # shared BRZ chassis: sandbox runner, gate, meter, run store, receipts
│       ├── gauntlet/      # Lane A — attack-set registry, volley runner, gate evaluator, scoreboard
│       └── nightshift/    # Lane B — job registry, staging, rewind snapshotter, promotion gate
├── tests/                 # examiner-style verification (added in later tasks)
├── docs/                  # session log + burn ledger (Task 2) and other notes
├── LICENSE
└── README.md
```

> This is scaffold only. The chassis and lanes are stubs; no feature is
> implemented yet. Build work proceeds one task per session per
> [`.kiro/specs/rosette-loop-lens/tasks.md`](.kiro/specs/rosette-loop-lens/tasks.md).

## Specs

- [Requirements](.kiro/specs/rosette-loop-lens/requirements.md)
- [Design](.kiro/specs/rosette-loop-lens/design.md)
- [Tasks](.kiro/specs/rosette-loop-lens/tasks.md)

## License

Released under the [MIT License](LICENSE).
