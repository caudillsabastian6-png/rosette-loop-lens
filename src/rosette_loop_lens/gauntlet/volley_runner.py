"""Volley runner (fusion leg 2 scaffold; Task 8; R2.1).

Fires a registered attack set at the check pipeline and writes per-item
results to the run store, one Glass Box receipt per item (leg 4).

The pipeline is a callable supplied by the caller (in production, the
Rosette check pipeline running inside a fresh sandbox; in tests, a
scripted stand-in). It receives an AttackItem and returns either a
verdict string or a dict with verdict + tells_fired +
exemplars_compared + reader_identity_report. The runner never calls a
pipeline for unregistered material, and never alters a verdict.
"""

from __future__ import annotations

from ..chassis.receipt_writer import GlassBoxReceipt


def run_volley(items, pipeline, *, run_store=None, receipt_log=None,
               thresholds=None) -> list[dict]:
    """Fire ``items`` at ``pipeline``; return per-item result dicts."""
    results = []
    for item in items:
        outcome = pipeline(item)
        if isinstance(outcome, str):
            outcome = {"verdict": outcome}
        result = {
            "kind": "volley_item",
            "item_id": item.item_id,
            "lane": item.lane,
            "label": item.label,
            "verdict": outcome.get("verdict"),
        }
        results.append(result)
        if run_store is not None:
            run_store.append(result)
        if receipt_log is not None:
            GlassBoxReceipt(
                kind="volley_item", lane=item.lane,
                thresholds=thresholds or {},
                exemplars_compared=outcome.get("exemplars_compared", []),
                tells_fired=outcome.get("tells_fired", []),
                reader_identity_report=outcome.get("reader_identity_report"),
                verdict=outcome.get("verdict"),
                verification={"item_id": item.item_id,
                              "label": item.label},
            ).emit(receipt_log)
    return results
