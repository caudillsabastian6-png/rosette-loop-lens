"""Leg 6 — Home Base contained-seat prototype tests."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from rosette_loop_lens.seats.contained_seat import ContainedSeat, SeatError


class TestContainedSeat(unittest.TestCase):
    def test_seat_works_inside_disposable_workspace(self):
        seat = ContainedSeat("Lister")
        try:
            seat.write_file("drafts/listing.txt", "hello")
            self.assertEqual(seat.read_file("drafts/listing.txt"), "hello")
            ws = seat.workspace
            self.assertTrue(os.path.isdir(ws))
        finally:
            seat.dispose()
        self.assertFalse(os.path.isdir(ws))  # disposable: gone

    def test_no_secrets_inside(self):
        with self.assertRaises(SeatError):
            ContainedSeat("Lister", env={"SOME_API_KEY": "nope"})
        seat = ContainedSeat("Lister", env={"PATH": "/usr/bin",
                                            "UNLISTED": "x"})
        try:
            self.assertEqual(seat.seat_env(), {"PATH": "/usr/bin"})
        finally:
            seat.dispose()

    def test_jail_blocks_escape(self):
        seat = ContainedSeat("Lister")
        try:
            with self.assertRaises(SeatError):
                seat.write_file("../escape.txt", "x")
        finally:
            seat.dispose()

    def test_pocket_gate_nothing_approves_itself(self):
        seat = ContainedSeat("Lister")
        try:
            proposal = seat.propose("reprice 3 listings", est_cost_cents=0)
            self.assertEqual(proposal.status, "pending")
            # Pending proposals execute nothing.
            with self.assertRaises(SeatError):
                seat.execute(proposal.proposal_id, lambda s: None)
            # The seat cannot approve its own proposal.
            with self.assertRaises(SeatError):
                seat.approve(proposal.proposal_id, approver="Lister")
            # External approval (the owner's tap) unlocks execution,
            # and the action is receipted.
            receipts = []
            seat.receipt_log = receipts
            seat.approve(proposal.proposal_id, approver="owner")
            done = seat.execute(
                proposal.proposal_id,
                lambda s: s.write_file("done.txt", "executed"))
            self.assertEqual(done.status, "executed")
            self.assertEqual(seat.read_file("done.txt"), "executed")
            self.assertEqual(len(receipts), 1)
        finally:
            seat.dispose()


if __name__ == "__main__":
    unittest.main()
