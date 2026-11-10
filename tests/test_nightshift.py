"""Leg 3 — Night Shift + Rewind lane scaffold tests."""

import hashlib
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from rosette_loop_lens.nightshift.job_registry import NightShift
from rosette_loop_lens.nightshift.promotion_gate import (
    PromotionAborted, payload_hash, promote)
from rosette_loop_lens.nightshift.rewind_snapshotter import RewindSnapshotter


def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


class TestNightShiftRewind(unittest.TestCase):
    def _setup(self, tmp):
        shared = os.path.join(tmp, "shared")
        _write(os.path.join(shared, "labels.txt"), "truth-v1\n")
        shift = NightShift(staging_root=os.path.join(tmp, "staging"),
                           snapshotter=RewindSnapshotter(os.path.join(tmp, "snaps")))
        return shared, shift

    def test_job_lands_in_staging_only_and_snapshot_names_itself(self):
        with tempfile.TemporaryDirectory() as tmp:
            shared, shift = self._setup(tmp)
            receipts = []
            shift.register_job("census", ["shared/labels.txt"],
                               lambda staging: _write(
                                   os.path.join(staging, "census.txt"), "counted\n"))
            result = shift.run_job("census", shared_dir=shared, receipt_log=receipts)
            self.assertEqual(result["files"], ["census.txt"])
            self.assertTrue(result["snapshot_id"])
            # Shared truth untouched by the run itself.
            with open(os.path.join(shared, "labels.txt")) as fh:
                self.assertEqual(fh.read(), "truth-v1\n")
            self.assertNotIn("census.txt", os.listdir(shared))
            self.assertEqual(len(receipts), 1)

    def test_rewind_restores_a_bad_night(self):
        with tempfile.TemporaryDirectory() as tmp:
            shared, shift = self._setup(tmp)
            manifest = shift.snapshotter.snapshot(shared)
            self.assertTrue(shift.snapshotter.verify(manifest))
            _write(os.path.join(shared, "labels.txt"), "corrupted\n")
            outcome = shift.snapshotter.restore(manifest, shared)
            self.assertTrue(outcome["restored"])
            with open(os.path.join(shared, "labels.txt")) as fh:
                self.assertEqual(fh.read(), "truth-v1\n")

    def test_corrupt_snapshot_refuses_restore(self):
        with tempfile.TemporaryDirectory() as tmp:
            shared, shift = self._setup(tmp)
            manifest = shift.snapshotter.snapshot(shared)
            snap_file = os.path.join(tmp, "snaps", manifest["snapshot_id"], "labels.txt")
            _write(snap_file, "tampered\n")
            self.assertFalse(shift.snapshotter.verify(manifest))
            with self.assertRaises(ValueError):
                shift.snapshotter.restore(manifest, shared)


class TestPromotionGate(unittest.TestCase):
    def _stage(self, tmp, payload=b"clean-result"):
        staged = os.path.join(tmp, "staging", "out.bin")
        _write(staged, payload.decode("latin1"))
        return staged, payload_hash(payload)

    def test_clean_payload_promotes_with_post_write_verify(self):
        with tempfile.TemporaryDirectory() as tmp:
            staged, digest = self._stage(tmp)
            receipts = []
            target = os.path.join(tmp, "truth", "out.bin")
            out = promote(staged_path=staged, target_path=target,
                          snapshot_id="snap1", expected_hash=digest,
                          designated_fake_check=lambda p: False,
                          examiner=lambda p: True, receipt_log=receipts)
            self.assertTrue(out["promoted"])
            self.assertEqual(out["snapshot_id"], "snap1")
            with open(target, "rb") as fh:
                self.assertEqual(hashlib.sha256(fh.read()).hexdigest(), digest)
            self.assertEqual(len(receipts), 1)

    def test_designated_fake_aborts_at_step_one(self):
        with tempfile.TemporaryDirectory() as tmp:
            staged, digest = self._stage(tmp, b"designated-fake-bytes")
            receipts = []
            target = os.path.join(tmp, "truth", "out.bin")
            with self.assertRaises(PromotionAborted):
                promote(staged_path=staged, target_path=target,
                        snapshot_id="snap1", expected_hash=digest,
                        designated_fake_check=lambda p: True,
                        examiner=lambda p: True, receipt_log=receipts)
            self.assertFalse(os.path.exists(target))
            self.assertEqual(len(receipts), 1)  # the abort is receipted

    def test_hash_mismatch_aborts_at_step_two(self):
        with tempfile.TemporaryDirectory() as tmp:
            staged, _digest = self._stage(tmp)
            target = os.path.join(tmp, "truth", "out.bin")
            with self.assertRaises(PromotionAborted):
                promote(staged_path=staged, target_path=target,
                        snapshot_id="snap1", expected_hash="0" * 64,
                        designated_fake_check=lambda p: False,
                        examiner=lambda p: True)
            self.assertFalse(os.path.exists(target))

    def test_examiner_failure_aborts_at_step_three(self):
        with tempfile.TemporaryDirectory() as tmp:
            staged, digest = self._stage(tmp)
            target = os.path.join(tmp, "truth", "out.bin")
            with self.assertRaises(PromotionAborted):
                promote(staged_path=staged, target_path=target,
                        snapshot_id="snap1", expected_hash=digest,
                        designated_fake_check=lambda p: False,
                        examiner=lambda p: False)
            self.assertFalse(os.path.exists(target))


if __name__ == "__main__":
    unittest.main()
