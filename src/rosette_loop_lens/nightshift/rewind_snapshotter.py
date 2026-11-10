"""Rewind snapshotter (fusion leg 3 scaffold; Task 12; R6).

Snapshot + hash-verify BEFORE any job may touch shared state; no
verified snapshot, no start. A snapshot records the SHA-256 of every
file in a shared-state directory; verify() re-hashes and compares;
restore() puts the snapshotted bytes back. Every snapshot taken through
NightShift (job_registry) names itself in the job's receipts, so a bad
night is a restore, not a loss.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import uuid


def _hash_tree(root: str) -> dict:
    hashes = {}
    for dirpath, _dirs, files in os.walk(root):
        for name in sorted(files):
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, root)
            with open(path, "rb") as fh:
                hashes[rel] = hashlib.sha256(fh.read()).hexdigest()
    return hashes


class RewindSnapshotter:
    def __init__(self, snapshot_root: str):
        self.snapshot_root = snapshot_root

    def snapshot(self, shared_dir: str) -> dict:
        """Copy shared_dir into a new snapshot; return its manifest."""
        snapshot_id = uuid.uuid4().hex[:12]
        dest = os.path.join(self.snapshot_root, snapshot_id)
        if os.path.exists(dest):
            shutil.rmtree(dest)
        shutil.copytree(shared_dir, dest)
        manifest = {"snapshot_id": snapshot_id, "source": shared_dir,
                    "hashes": _hash_tree(dest)}
        return manifest

    def verify(self, manifest: dict) -> bool:
        dest = os.path.join(self.snapshot_root, manifest["snapshot_id"])
        if not os.path.isdir(dest):
            return False
        return _hash_tree(dest) == manifest["hashes"]

    def verify_shared_unchanged(self, manifest: dict, shared_dir: str) -> bool:
        return _hash_tree(shared_dir) == manifest["hashes"]

    def restore(self, manifest: dict, shared_dir: str) -> dict:
        """Replace shared_dir's contents with the snapshot's bytes and
        verify hash-for-hash after the restore."""
        dest = os.path.join(self.snapshot_root, manifest["snapshot_id"])
        if not self.verify(manifest):
            raise ValueError("snapshot failed verification; refusing to restore from it")
        if os.path.exists(shared_dir):
            shutil.rmtree(shared_dir)
        shutil.copytree(dest, shared_dir)
        ok = _hash_tree(shared_dir) == manifest["hashes"]
        return {"snapshot_id": manifest["snapshot_id"], "restored": ok}
