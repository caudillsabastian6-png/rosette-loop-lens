# Tasks — Rosette Loop Lens, Phase 1

Rules of the list: one task ≈ one Kiro session. Work top to bottom; the
Gauntlet lane lands first, Night Shift/Rewind in sync behind it on the same
chassis. Check a box only when the task's verification has actually run.
Requirement numbers refer to `requirements.md`.

**Gate on everything below:** no task that touches BRZ code, the BRZ repo,
or the BRZ box may start before **Sun Nov 8, 2026, 6:00 PM ET** (the LabLab
filing) — R13. Tasks 1–2 are repo/spec work and are legal any time; the
operator's first *build* sessions happen after the Wed Nov 11 learn
session regardless.

## Scaffold

- [ ] **1. Repo scaffold.** Project skeleton, README carrying the public
  line ("Rosette — contained by Blast Radius Zero."), open-source LICENSE
  detectable at the top of the repo page, `/.kiro` (steering + this spec)
  committed and NOT gitignored. *(Serves: submission groundwork; R13.)*
  Verify: fresh clone shows `/.kiro` present; license renders on the repo
  page.
- [ ] **2. Session-log + burn ledger.** The running log every session
  appends to (date, task, what changed, verification, credits burned).
  *(Serves: total-record habit, credit discipline.)*
  Verify: Task 1's own entry exists and is complete.

## Shared chassis (build once — R1, R9, R10)

- [ ] **3. Chassis inventory (read-only).** After the freeze lifts: survey
  the BRZ chassis as-built (surfaces, gate, run store, frozen-core list per
  the Nov 5 autopsy) and write the adapter contract this project builds
  against. Modify nothing on the BRZ side. *(Serves: R1, R13.)*
  Verify: contract names every surface it relies on — including that gate
  state lives at `/gate/state` — and every claim traces to the autopsy.
- [ ] **4. Sandbox runner.** Fresh disposable sandbox per job: no network,
  time + memory caps, destroyed at job end, outcome recorded. *(Serves:
  R1.1–R1.3, R9.2.)*
  Verify: a probe job that tries to reach the network fails; a probe job
  that overruns its cap is killed and recorded as contained.
- [ ] **5. Proposals gate + meter.** The shared gate (nothing consequential
  executes unproposed) and meter (every run accounted in the run store).
  *(Serves: R1.4.)*
  Verify: an unproposed action cannot execute; a proposed-and-held action
  shows as pending, as the exhibit's gate does.
- [ ] **6. Receipt writer.** The R8 Glass Box record: lane + thresholds,
  exemplar identities + scores, tells fired, reader identity-only report,
  gate decision, verification results — no jewel data, ever. *(Serves:
  R8, R10.3.)*
  Verify: a sample run's receipt replays to the same outcome from the
  record alone; a receipt scanned for bank images/keys contains none.

## Lane A — Fake Gauntlet (lead — R2, R3, R4, R12)

- [ ] **7. Attack-set registry.** Per-lane registration (printed pair-sheet
  / crew-manufactured / future cardstock), manufactured/simulated labels on
  every item and surface, designated-fake check at intake, refusal of any
  non-manufactured material. *(Serves: R2.2–R2.4, R12.)*
  Verify: registering a physical-core item is refused and the refusal is
  recorded; every registered item shows its lane + label.
- [ ] **8. Volley runner.** Fire a registered set at the check pipeline
  inside the sandbox; per-item results to the run store. *(Serves: R2.1.)*
  Verify: a full volley of a small set completes; fired count equals the
  set's registered count.
- [ ] **9. Gate evaluator.** R3 semantics exactly: any genuine-side escape
  fails the build; forbidden outputs above zero fail the build; lanes
  scored separately, core never blended or rescued. *(Serves: R3.)*
  Verify: the examiner fixtures in Task 15 pass against this evaluator.
- [ ] **10. Scoreboard.** Per-lane fired / contained / escaped /
  inconclusive counts, re-derived from the run store, honesty labels on
  every figure. *(Serves: R4.)*
  Verify: scoreboard numbers match a hand count of the underlying run
  records for the same volley.

## Lane B — Night Shift + Rewind (in sync — R5, R6, R7)

- [ ] **11. Job registry + staging.** Named jobs with declared inputs;
  output lands in staging only; a job holds no write path to shared truth.
  *(Serves: R5.1–R5.2, R9.3.)*
  Verify: a probe job that attempts a direct write to a truth pile fails;
  its legitimate output appears in staging and nowhere else.
- [ ] **12. Rewind snapshotter.** Snapshot + hash-verify before any job is
  permitted near shared state; no verified snapshot, no start; restore
  path works and is receipted. *(Serves: R6.)*
  Verify: corrupt the snapshot check → job refuses to start; run a restore
  drill on a scratch pile → state matches the snapshot hash-for-hash.
- [ ] **13. Promotion gate.** Staged output promotes only via:
  designated-fake check → hash verify → examiner read; any failure aborts
  with state untouched and the abort receipted; promotions name their
  snapshot. *(Serves: R7, R10, R12.)*
  Verify: stage a designated-fake item → promotion aborts at step one;
  stage a hash-mismatched payload → aborts at step two; stage a clean
  payload → promotes, post-write verify recorded.
- [ ] **14. First real job, end-to-end.** Wire ONE named house job (owner
  picks which — design.md open question 2) through registry → sandbox →
  staging → promotion, unattended, once. *(Serves: R5, R6, R7 together.)*
  Verify: the run's receipt chain is complete and the job's output reached
  truth only through the gate.

## Examiner-style verification (nothing below is optional)

- [ ] **15. Gate-integrity exam.** Plant a known escape (a fake the
  pipeline is rigged to pass) and a known forbidden output: the build MUST
  fail both times, and the failure MUST be the reported result. *(Serves:
  R3.1, R3.2, R3.4.)*
- [ ] **16. Abort-path exam.** Force a hash mismatch and an identity-proof
  failure on consequential actions: both abort, prior state intact, both
  receipts say why. *(Serves: R10.)*
- [ ] **17. Isolation exam.** Inside a sandbox, attempt to reach: the
  banks, the issuer key, writable master labels, another user's scan, the
  network. All five MUST fail. *(Serves: R9, R1.2.)*
- [ ] **18. Honesty exam.** Sweep every output surface: verdict wording is
  exactly the three house lanes; the reader appears nowhere as a voter; no
  surface calls an outside model; every attack figure carries its
  simulated label. *(Serves: R11, R4.2, R8.4.)*

## Freeze + submission runway

- [ ] **19. Demo dry run.** Both lanes demoed together (a volley + a night
  job + a promotion + a rewind), timed, on the record. Fix list from the
  dry run is the only work allowed after this task. *(Serves: the Dec 1
  freeze.)*
- [ ] **20. Feature freeze — Tue Dec 1, 2026.** Freeze declared in the
  session log. From here: fixes and packaging only, no new scope.
- [ ] **21. Submission package.** Public GitHub repo (GitHub, not
  GitLab/Bitbucket) with license detectable, `/.kiro` present and not
  gitignored; functional-app URL; text description; demo video under 3
  minutes, public on YouTube; the "how Kiro was used" write-up (specs,
  steering, hooks — all real, all in the repo); the pre-existing-work
  disclosure, updated to name the fusion's actual reuse. *(Serves:
  Kiroween rules, per KIROWEEN-PREP.md §1.)*
- [ ] **22. Submit — target Thu Dec 3, 2026.** Submission filed a day
  ahead of the Fri Dec 4, 5:00 PM ET deadline. Dec 4 is buffer only.
  **This task requires the owner's explicit word before it runs (R14.2).**
