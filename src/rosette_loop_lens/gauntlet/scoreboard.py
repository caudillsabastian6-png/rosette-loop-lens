"""Scoreboard (fusion leg 2 scaffold; Task 10; R4).

Per-lane fired / contained / escaped / inconclusive counts, re-derived
from run-store volley records — never from a runner's in-memory tally —
with the honesty label on every figure (simulated attacks, labelled as
such). Lanes are reported separately, always.
"""

from __future__ import annotations

from .attack_registry import HONESTY_LABEL, LANES
from .gate_evaluator import evaluate


def scoreboard(run_store) -> dict:
    records = [r for r in run_store.read_all() if r.get("kind") == "volley_item"]
    gate = evaluate(records)
    board = {}
    for lane in LANES:
        counts = gate.per_lane.get(
            lane, {"fired": 0, "contained": 0, "escaped": 0,
                   "inconclusive": 0, "forbidden": 0})
        board[lane] = {**counts, "label": HONESTY_LABEL}
    board["gate_passed"] = gate.passed
    board["label"] = HONESTY_LABEL
    return board
