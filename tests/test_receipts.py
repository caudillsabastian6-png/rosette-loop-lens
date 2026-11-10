"""Leg 4 — Glass Box receipt format + emission tests."""

import io
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from rosette_loop_lens.chassis.receipt_writer import (
    GlassBoxReceipt, ReceiptError, replay_outcome, validate_receipt)


class TestReceipts(unittest.TestCase):
    def test_receipt_emits_as_jsonl_and_replays(self):
        log = io.StringIO()
        record = GlassBoxReceipt(
            kind="check", lane="printed_pair_sheet",
            thresholds={"catch_bar": 0.80},
            exemplars_compared=[{"identity": "ex-001", "score": 0.91}],
            tells_fired=["straight_cut_edge"],
            reader_identity_report={"identity": "Charizard, 4/102"},
            verdict="Likely Counterfeit", gate_decision="pass",
        ).emit(log)
        lines = log.getvalue().strip().splitlines()
        self.assertEqual(len(lines), 1)
        parsed = json.loads(lines[0])
        self.assertEqual(parsed["receipt_id"], record["receipt_id"])
        self.assertEqual(replay_outcome(parsed),
                         ("check", "printed_pair_sheet",
                          "Likely Counterfeit", "pass"))

    def test_verdict_vocabulary_is_exact(self):
        with self.assertRaises(ReceiptError):
            GlassBoxReceipt(kind="check", lane="x",
                            verdict="Guaranteed Genuine").to_dict()

    def test_no_crown_jewel_data(self):
        with self.assertRaises(ReceiptError):
            GlassBoxReceipt(kind="check", lane="x",
                            verification={"bank_image": "..."}).to_dict()
        with self.assertRaises(ReceiptError):
            GlassBoxReceipt(kind="check", lane="x",
                            tells_fired=["data:image/png;base64,AAAA"]).to_dict()

    def test_reader_never_votes(self):
        with self.assertRaises(ReceiptError):
            GlassBoxReceipt(
                kind="check", lane="x",
                reader_identity_report={"identity": "Pikachu",
                                        "verdict": "Likely Genuine"}).to_dict()

    def test_exemplars_are_identity_and_score_only(self):
        with self.assertRaises(ReceiptError):
            GlassBoxReceipt(
                kind="check", lane="x",
                exemplars_compared=[{"identity": "ex-1", "score": 0.5,
                                     "scan_path": "/banks/ex-1.png"}]).to_dict()

    def test_validate_rejects_unknown_kind(self):
        bad = {"receipt_version": 1, "kind": "side_channel", "lane": "x",
               "verdict": None, "reader_identity_report": None,
               "exemplars_compared": []}
        with self.assertRaises(ReceiptError):
            validate_receipt(bad)


if __name__ == "__main__":
    unittest.main()
