# Session log — Rosette Loop Lens

Every session appends here: date, task, what changed, how it was verified,
credits burned. Work that isn't recorded didn't happen (steering: Total record).

> Note: Task 2 formalizes this log plus a burn ledger. This file starts the
> record now because the Total-record habit and Task 1's own instructions
> require Task 1 to be logged. Task 2 will build on it, not replace the habit.

---

## 2026-11-05 — Task 1: Repo scaffold

**Task:** `tasks.md` #1 — Repo scaffold (serves submission groundwork; R13).

**What changed (scaffold only, no feature implemented):**
- Added `README.md` carrying the public line verbatim:
  "Rosette — contained by Blast Radius Zero." plus project overview, the
  fences, and the repo layout.
- Added an open-source `LICENSE` (MIT) at the repo root so it is detectable
  at the top of the repo page.
- Added `.gitignore` tuned for Python + crown-jewel exclusions; it explicitly
  does **not** ignore `/.kiro` (an un-ignore for `.kiro/` and `.kiro/**` is
  kept last as a safety net).
- Created the source skeleton under `src/rosette_loop_lens/`:
  `chassis/` (sandbox_runner, proposals_gate, run_store, receipt_writer),
  `gauntlet/` (attack_registry, volley_runner, gate_evaluator, scoreboard),
  `nightshift/` (job_registry, rewind_snapshotter, promotion_gate). Every
  module is a docstring stub naming the task and requirements that will build
  it — no feature logic.
- Added `pyproject.toml` (metadata only, no dependencies) and `tests/` +
  `docs/` placeholders.
- Checked the Task 1 box in `tasks.md`.

**How it was verified:**
- `git check-ignore` on `.kiro`, `.kiro/steering/steering.md`, and
  `.kiro/specs/.../tasks.md` → exit 1 (none ignored); `.kiro` remains tracked.
- `git add -A -n` preview confirms README, LICENSE, .gitignore, pyproject, and
  the full `src/` tree would be committed.
- `grep -F "Rosette — contained by Blast Radius Zero." README.md` matches the
  public line verbatim.
- `PYTHONPATH=src python3 -c "import rosette_loop_lens, ...chassis, ...gauntlet,
  ...nightshift"` → "import OK 0.0.0": the package tree imports cleanly.
- Fresh-clone check RAN: cloned branch `task-1-repo-scaffold` into a temp dir;
  `/.kiro` present (steering.md + specs), root `LICENSE` (MIT) present, README
  public line present, Task 1 box checked. Clone then removed.
- License "renders on the repo page": MIT in a root `LICENSE` file is the
  standard GitHub-detectable form. HONEST NOTE: `gh api .../license` returns
  404 right now because GitHub detects the license on the DEFAULT branch
  (`main`), and the LICENSE currently lives only on the `task-1-repo-scaffold`
  branch (branch policy forbids committing to `main` directly). It will render
  on the repo page once this branch is merged to `main`. The file itself is
  correct and in the right location — verified by fresh clone.

**Scope notes / fences honored:**
- No feature implemented; BRZ untouched (R13 freeze respected).
- No publishing: work committed to a session branch for review, not a public
  repo push or submission (steering: no publish without the owner's word).
- No spend. 0 Kiro credits tracked for this session (credit accounting is
  formalized in Task 2's burn ledger).

**Credits burned:** not separately metered this session; ledger starts in Task 2.

---

## 2026-11-08 — Task 3: Chassis inventory (read-only)

**Task:** `tasks.md` #3 — Chassis inventory (read-only); write the adapter
contract this project builds against (serves R1, R13).

**What changed (survey + documentation only, no feature implemented, BRZ
untouched):**
- Added `docs/chassis-adapter-contract.md` — the adapter contract Phase 1
  builds against. It names every BRZ chassis surface Phase 1 relies on and
  traces every claim to the Nov 5 autopsy facts carried in `design.md` §1
  (or to the requirements/design sections cited inline). Contents:
  - **§1 Surfaces:** `/health`, `/gate` (Pocket Gate), `/gate/state` (gate
    state lives here; states explicitly there is **no** `/gate/status`
    route), `/inspect` and `/replay` (Glass Box), `/nightshift`, `/rewind`.
  - **§2 Gate behaviour:** work is proposed not executed; proposals wait
    under a threshold ($500 in the exhibit's demo state); the phase-2 close
    left 42 proposals, all pending.
  - **§3 Containment exhibits:** Gauntlet volley `55d80996e615`
    (7 in / 7 contained / 0 landed / $24,346 prevented — simulated,
    labelled); Night Shift run `2bdfb651854e`; Rewind day `a564597892e6`.
  - **§4 Failure semantics inherited:** an unparseable model reply
    dispatches nothing and invents nothing — run recorded failed-contained.
  - **§5 Frozen core + run-store shape:** the frozen-core file list
    (`loop.py`, `protocol.py`, `sandbox_client.py`, `tools.py`,
    `config.py`, `inference/*`, `worker/executor.py`,
    `agent/requirements.txt`) as read-only reference (R13.3); run store =
    67 run records + 5 state files as of the autopsy.
  - **§6 Complete-read rule (R10.3):** public-path reads can truncate
    (gate state 30,366 bytes complete via localhost vs 12,312 truncated
    publicly); a read of gate state / run record / receipt counts as
    verified only if complete.
  - **§7 Crown-jewel placement (names only):** banks, issuer private key,
    writable master labels live house-side (G1/home), outside every
    sandbox; no jewel data, images, or keys in the contract, repo, or log.
  - **§8 Open questions:** `design.md` §7 OQ-1..OQ-5 repeated as **open**,
    not answered.
  - **§9 UNVERIFIED items:** none; all claims traced.
- Checked the Task 3 box in `tasks.md`.

**How it was verified (Task 3's own verification ran):**
- Surface coverage check RAN: grep confirmed `/health`, `/gate`,
  `/gate/state`, `/inspect`, `/replay`, `/nightshift`, `/rewind` all
  present, plus the explicit "NO `/gate/status` route" statement
  (contract lines 46–48).
- Claim-tracing check RAN: grep confirmed each autopsy figure appears in
  the contract and matches `design.md` §1 — `55d80996e615`, `$24,346`,
  `2bdfb651854e`, `a564597892e6`, `42 proposals`, `$500`, `67 run records
  + 5 state files`, `30,366` / `12,312`, failed-contained. §9 asserts no
  UNVERIFIED items.
- Open-question check: §8 repeats `design.md` §7 OQ-1..OQ-5 as open; the
  contract answers none of them.
- Both Task 3 verification conditions hold: the contract names every
  surface it relies on (including `/gate/state`) and every claim traces to
  the autopsy.

**Scope notes / fences honored:**
- Read-only survey + documentation only; no feature implemented.
- BRZ untouched — no edit to the BRZ repo, box, or any frozen-core file
  (R13.1–R13.3). This task modified nothing outside this repository.
- No jewel data, images, or keys written anywhere (steering fence 6; R9;
  R8.2).
- Branch policy: the current branch at session start was `main` (the
  default), so a new session branch is used for the commit; no commit
  direct to `main`. No publish/submit (R14.2) — work stays local/branch
  for review until the owner's word.
- Stopped at Task 3's edge; did not start Task 4 (scope discipline).

**Credits burned:** UNKNOWN — this session surfaced no credit/burn footer
to read, so the exact credits burned cannot be stated honestly and are not
guessed (Honesty law). Task 2's burn ledger, once built, is the intended
home for this figure.
