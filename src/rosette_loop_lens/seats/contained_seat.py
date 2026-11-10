"""Contained-seat prototype (fusion leg 6 — owner's Nov 6 addendum).

A minimal spike proving ONE acting Home Base seat working inside a BRZ
sandbox, local/VM-side only:

- Disposable workspace: the seat works in a fresh temp directory that
  is destroyed on dispose(); nothing outside it is reachable through
  the seat's file API (paths are jailed to the workspace).
- No secrets inside: the seat refuses to start if its environment
  carries any secret-shaped variable, and its environment is an
  allowlist, never an inheritance of the host's.
- Pocket Gate escalation: every action the seat wants to take in the
  world is a PROPOSAL that pends. Nothing approves itself — approval
  must come from an external approver identity, and the seat's own
  name is rejected as an approver. Only approved proposals execute,
  inside the workspace, and each execution emits a Glass Box receipt
  (kind "seat_action": who did what, replayable).
- Spend shape: a proposal carries an estimated cost; cost-bearing
  proposals pend exactly like the rest (the owner's tap is the only
  approval path — there is no auto-approve threshold in the spike).
"""

from __future__ import annotations

import os
import shutil
import tempfile
import uuid
from dataclasses import dataclass, field

from ..chassis.receipt_writer import GlassBoxReceipt

_SECRET_MARKERS = ("KEY", "TOKEN", "SECRET", "PASSWORD", "CREDENTIAL")
_ENV_ALLOWLIST = ("PATH", "LANG", "LC_ALL", "TZ")


class SeatError(RuntimeError):
    pass


@dataclass
class Proposal:
    proposal_id: str
    seat: str
    action: str
    est_cost_cents: int = 0
    status: str = "pending"   # pending | approved | rejected | executed
    approver: str | None = None


@dataclass
class ContainedSeat:
    name: str
    env: dict = field(default_factory=dict)
    receipt_log: object = None
    _workspace: str = field(default="", repr=False)
    _proposals: dict = field(default_factory=dict, repr=False)

    def __post_init__(self):
        for key in self.env:
            if any(marker in key.upper() for marker in _SECRET_MARKERS):
                raise SeatError(
                    f"refusing to seat {self.name!r}: environment carries "
                    f"secret-shaped variable {key!r}; no secrets inside a seat")
        self._workspace = tempfile.mkdtemp(prefix=f"seat-{self.name}-")

    # -- sandbox file API (jailed to the disposable workspace) --
    @property
    def workspace(self) -> str:
        return self._workspace

    def _jailed(self, rel_path: str) -> str:
        path = os.path.realpath(os.path.join(self._workspace, rel_path))
        if os.path.commonpath([path, self._workspace]) != self._workspace:
            raise SeatError(f"path escapes the seat sandbox: {rel_path!r}")
        return path

    def write_file(self, rel_path: str, content: str) -> None:
        path = self._jailed(rel_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)

    def read_file(self, rel_path: str) -> str:
        with open(self._jailed(rel_path), encoding="utf-8") as fh:
            return fh.read()

    def seat_env(self) -> dict:
        """The only environment the seat's actions see: the allowlist."""
        return {k: v for k, v in self.env.items() if k in _ENV_ALLOWLIST}

    # -- Pocket Gate --
    def propose(self, action: str, *, est_cost_cents: int = 0) -> Proposal:
        proposal = Proposal(proposal_id=uuid.uuid4().hex[:12],
                            seat=self.name, action=action,
                            est_cost_cents=est_cost_cents)
        self._proposals[proposal.proposal_id] = proposal
        return proposal

    def approve(self, proposal_id: str, *, approver: str) -> Proposal:
        """External approval only. The seat approving its own proposal —
        or an action approving itself by any name match — is refused."""
        proposal = self._proposals[proposal_id]
        if approver == self.name or approver == proposal.seat:
            raise SeatError("nothing approves itself: a seat cannot "
                            "approve its own proposal")
        if proposal.status != "pending":
            raise SeatError(f"proposal {proposal_id} is {proposal.status}, not pending")
        proposal.status = "approved"
        proposal.approver = approver
        return proposal

    def execute(self, proposal_id: str, fn) -> Proposal:
        """Run an approved proposal's action inside the workspace and
        receipt it. Pending or rejected proposals execute nothing."""
        proposal = self._proposals[proposal_id]
        if proposal.status != "approved":
            raise SeatError(
                f"proposal {proposal_id} is {proposal.status}; only an "
                "externally approved proposal may execute")
        fn(self)  # the action receives the seat (jailed workspace + env)
        proposal.status = "executed"
        if self.receipt_log is not None:
            GlassBoxReceipt(
                kind="seat_action", lane=f"seat:{self.name}",
                gate_decision="promoted",
                verification={"proposal_id": proposal.proposal_id,
                              "action": proposal.action,
                              "approver": proposal.approver,
                              "est_cost_cents": proposal.est_cost_cents},
            ).emit(self.receipt_log)
        return proposal

    def dispose(self) -> None:
        if self._workspace and os.path.isdir(self._workspace):
            shutil.rmtree(self._workspace)
        self._workspace = ""
