"""Promotion gate (fusion leg 3 scaffold; Task 13; R7, R10, R12).

The only door from staging to truth, in order:
  1. designated-fake record check — card material flagged in the
     designated-fake record never promotes into genuine piles;
  2. payload hash verify against the hash recorded at staging time;
  3. examiner read — an external examiner callable must pass it.
Any failure aborts with shared state untouched, and the abort is
receipted (kind "abort"). Every promotion names the Rewind snapshot it
was made against. Nothing a night job produces becomes truth by itself.
"""

from __future__ import annotations

import hashlib
import json
import os

from ..chassis.receipt_writer import GlassBoxReceipt


class PromotionAborted(RuntimeError):
    pass


def payload_hash(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def promote(*, staged_path: str, target_path: str, snapshot_id: str,
            expected_hash: str, designated_fake_check, examiner,
            receipt_log=None, lane: str = "nightshift") -> dict:
    """Promote one staged file to its target, through the three checks.

    ``designated_fake_check(payload_bytes) -> bool`` returns True when
    the payload is designated-fake material (promotion forbidden).
    ``examiner(payload_bytes) -> bool`` is the examiner read.
    """
    with open(staged_path, "rb") as fh:
        payload = fh.read()

    def abort(reason: str):
        if receipt_log is not None:
            GlassBoxReceipt(
                kind="abort", lane=lane, gate_decision="aborted",
                verification={"reason": reason, "snapshot_id": snapshot_id,
                              "target": target_path},
            ).emit(receipt_log)
        raise PromotionAborted(reason)

    # 1. Designated-fake record check — always first.
    if designated_fake_check(payload):
        abort("designated-fake record check: payload is designated-fake "
              "material; it never promotes into genuine piles")
    # 2. Hash verify against the hash recorded at staging time.
    actual = payload_hash(payload)
    if actual != expected_hash:
        abort(f"hash mismatch: staged payload sha256 {actual} != recorded "
              f"{expected_hash}; shared state untouched")
    # 3. Examiner read.
    if not examiner(payload):
        abort("examiner read did not pass the payload")

    os.makedirs(os.path.dirname(os.path.abspath(target_path)), exist_ok=True)
    with open(target_path, "wb") as fh:
        fh.write(payload)
    # Post-write verify (safety-checks-on-everything): re-read and hash.
    with open(target_path, "rb") as fh:
        written_ok = payload_hash(fh.read()) == expected_hash
    receipt = {"promoted": written_ok, "target": target_path,
               "sha256": expected_hash, "snapshot_id": snapshot_id}
    if receipt_log is not None:
        GlassBoxReceipt(
            kind="promotion", lane=lane, gate_decision="promoted",
            verification={"sha256": expected_hash,
                          "snapshot_id": snapshot_id,
                          "post_write_verify": written_ok},
        ).emit(receipt_log)
    return receipt
