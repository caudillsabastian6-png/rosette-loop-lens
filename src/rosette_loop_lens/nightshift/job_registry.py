"""Job registry + staging (fusion leg 3 scaffold; Task 11; R5.1-R5.2, R9.3).

Named jobs with declared inputs (pool census, mirror verification,
library organisation, Basil shadow batches). A job runs as a callable
that receives ONLY a staging directory handle: its output lands in
staging, and it holds no write path to shared truth — the registry's
API simply never hands it one.

A Rewind snapshot of shared state is taken and verified BEFORE the job
starts (no verified snapshot, no start), and the run is receipted
(job receipt naming the snapshot). Promotion out of staging is a
separate gated act (promotion_gate.py) — not part of a job's run.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

from ..chassis.receipt_writer import GlassBoxReceipt
from .rewind_snapshotter import RewindSnapshotter


@dataclass
class NightShift:
    staging_root: str
    snapshotter: RewindSnapshotter
    jobs: dict = field(default_factory=dict)  # name -> (inputs, fn)

    def register_job(self, name: str, declared_inputs: list, fn) -> None:
        self.jobs[name] = (list(declared_inputs), fn)

    def run_job(self, name: str, *, shared_dir: str, receipt_log=None,
                lane: str = "nightshift") -> dict:
        """Snapshot -> verify -> run into staging -> receipt.

        Returns {job, snapshot_id, staging_dir, files}. The job callable
        receives the staging directory path and nothing else."""
        if name not in self.jobs:
            raise KeyError(f"unknown night job: {name!r}")
        _inputs, fn = self.jobs[name]
        manifest = self.snapshotter.snapshot(shared_dir)
        if not self.snapshotter.verify(manifest):
            if receipt_log is not None:
                GlassBoxReceipt(
                    kind="abort", lane=lane, gate_decision="aborted",
                    verification={"job": name, "reason": "rewind snapshot "
                                  "failed verification; job did not start",
                                  "snapshot_id": manifest["snapshot_id"]},
                ).emit(receipt_log)
            raise RuntimeError("rewind snapshot failed verification; job did not start")
        staging_dir = os.path.join(self.staging_root, name)
        os.makedirs(staging_dir, exist_ok=True)
        fn(staging_dir)  # the job can only write where it is handed: staging
        files = sorted(os.listdir(staging_dir))
        result = {"job": name, "snapshot_id": manifest["snapshot_id"],
                  "staging_dir": staging_dir, "files": files}
        if receipt_log is not None:
            GlassBoxReceipt(
                kind="job", lane=lane,
                verification={"job": name,
                              "snapshot_id": manifest["snapshot_id"],
                              "snapshot_verified": True,
                              "staged_files": files},
            ).emit(receipt_log)
        return result
