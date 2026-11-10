"""Leg 2 — Fake Gauntlet lane scaffold tests."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from rosette_loop_lens.chassis.run_store import RunStore
from rosette_loop_lens.gauntlet.attack_registry import (
    AttackRegistry, RegistrationRefused)
from rosette_loop_lens.gauntlet.gate_evaluator import evaluate
from rosette_loop_lens.gauntlet.scoreboard import scoreboard
from rosette_loop_lens.gauntlet.volley_runner import run_volley


def _registry_with(*specs):
    reg = AttackRegistry()
    items = []
    for item_id, lane in specs:
        items.append(reg.register(item_id, lane, designated_fake=True))
    return reg, items


class TestRegistry(unittest.TestCase):
    def test_register_ok_carries_honesty_label(self):
        _reg, items = _registry_with(("pps-001", "printed_pair_sheet"))
        self.assertEqual(items[0].label, "simulated/manufactured")
        self.assertEqual(items[0].lane, "printed_pair_sheet")

    def test_designated_fake_check_is_mandatory(self):
        reg = AttackRegistry()
        with self.assertRaises(RegistrationRefused):
            reg.register("x-1", "crew_manufactured_digital", designated_fake=False)
        self.assertEqual(len(reg.refusals), 1)

    def test_physical_core_is_never_a_lane(self):
        reg = AttackRegistry()
        with self.assertRaises(RegistrationRefused):
            reg.register("core-1", "physical_core", designated_fake=True)

    def test_non_manufactured_material_refused(self):
        reg = AttackRegistry()
        with self.assertRaises(RegistrationRefused):
            reg.register("g-1", "printed_pair_sheet", designated_fake=True,
                         manufactured=False)

    def test_lanes_stay_separated_in_counts(self):
        reg, _items = _registry_with(
            ("a", "printed_pair_sheet"), ("b", "crew_manufactured_digital"),
            ("c", "printed_pair_sheet"))
        counts = reg.counts()
        self.assertEqual(counts["printed_pair_sheet"], 2)
        self.assertEqual(counts["crew_manufactured_digital"], 1)
        self.assertEqual(counts["crew_manufactured_cardstock"], 0)


class TestVolleyAndGate(unittest.TestCase):
    def test_clean_volley_passes_and_receipts_are_emitted(self):
        _reg, items = _registry_with(
            ("a", "printed_pair_sheet"), ("b", "printed_pair_sheet"))
        receipts = []
        with tempfile.TemporaryDirectory() as tmp:
            store = RunStore(os.path.join(tmp, "runs.jsonl"))
            results = run_volley(
                items, lambda item: {"verdict": "Likely Counterfeit",
                                     "tells_fired": ["straight_cut_edge"]},
                run_store=store, receipt_log=receipts)
            gate = evaluate(results)
            self.assertTrue(gate.passed)
            self.assertEqual(gate.per_lane["printed_pair_sheet"]["contained"], 2)
            self.assertEqual(len(receipts), 2)
            board = scoreboard(store)
            self.assertEqual(board["printed_pair_sheet"]["fired"], 2)
            self.assertTrue(board["gate_passed"])
            self.assertEqual(board["label"], "simulated/manufactured")

    def test_genuine_side_escape_fails_the_build(self):
        _reg, items = _registry_with(("a", "crew_manufactured_digital"))
        results = run_volley(items, lambda item: "Likely Genuine")
        gate = evaluate(results)
        self.assertFalse(gate.passed)
        self.assertEqual(gate.escapes, ["a"])

    def test_forbidden_output_fails_the_build(self):
        _reg, items = _registry_with(("a", "printed_pair_sheet"))
        results = run_volley(items, lambda item: "Guaranteed Authentic")
        gate = evaluate(results)
        self.assertFalse(gate.passed)
        self.assertEqual(gate.forbidden_outputs, 1)

    def test_inconclusive_is_not_an_escape(self):
        _reg, items = _registry_with(("a", "printed_pair_sheet"))
        gate = evaluate(run_volley(items, lambda item: "Inconclusive"))
        self.assertTrue(gate.passed)
        self.assertEqual(gate.per_lane["printed_pair_sheet"]["inconclusive"], 1)


if __name__ == "__main__":
    unittest.main()
