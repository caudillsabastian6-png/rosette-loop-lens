"""Gate evaluator (fusion leg 2 scaffold; Task 9; R3).

R3 semantics exactly:
- any manufactured fake that escapes with a genuine-side verdict
  ("Likely Genuine") FAILS the build;
- forbidden outputs above zero FAIL the build — a forbidden output is
  any pipeline output outside the exact verdict vocabulary (guaranteed/
  official wording, a reader vote, or anything else unparseable as one
  of the three house lanes);
- lanes are scored separately; the frozen physical core is never
  blended, diluted, or rescued by an auxiliary lane.
A failed gate stays failed for the run — no re-roll, relabel, or
threshold change (the evaluator holds no mutators for results).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..chassis.receipt_writer import VERDICT_VOCABULARY

GENUINE_SIDE = "Likely Genuine"


@dataclass
class GateResult:
    passed: bool
    escapes: list = field(default_factory=list)          # item_ids
    forbidden_outputs: int = 0
    per_lane: dict = field(default_factory=dict)         # lane -> counts

    def summary(self) -> dict:
        return {"passed": self.passed, "escapes": list(self.escapes),
                "forbidden_outputs": self.forbidden_outputs,
                "per_lane": self.per_lane}


def evaluate(results: list[dict]) -> GateResult:
    """Evaluate volley results: dicts with item_id, lane, verdict."""
    per_lane: dict = {}
    escapes: list = []
    forbidden = 0
    for result in results:
        lane = result["lane"]
        counts = per_lane.setdefault(
            lane, {"fired": 0, "contained": 0, "escaped": 0,
                   "inconclusive": 0, "forbidden": 0})
        counts["fired"] += 1
        verdict = result.get("verdict")
        if verdict not in VERDICT_VOCABULARY:
            forbidden += 1
            counts["forbidden"] += 1
        elif verdict == GENUINE_SIDE:
            escapes.append(result["item_id"])
            counts["escaped"] += 1
        elif verdict == "Inconclusive":
            counts["inconclusive"] += 1
        else:  # Likely Counterfeit — the fake was caught
            counts["contained"] += 1
    passed = not escapes and forbidden == 0
    return GateResult(passed=passed, escapes=escapes,
                      forbidden_outputs=forbidden, per_lane=per_lane)
