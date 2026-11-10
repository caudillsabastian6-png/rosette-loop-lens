"""Run store — every run, volley, and receipt recorded (serves R1.3, R4.3, R8).

Scaffold implementation (fusion expansion night, 2026-11-08): an
append-only JSONL store. The scoreboard and every reported number are
re-derived from these records; a replay is a re-read of the record, and
the outcome must match. The store holds records only — never card
material, bank images, or keys (see .gitignore: runs/ stays uncommitted).
"""

from __future__ import annotations

import json
import os


class RunStore:
    def __init__(self, path: str):
        self.path = path

    def append(self, record: dict) -> None:
        os.makedirs(os.path.dirname(os.path.abspath(self.path)), exist_ok=True)
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    def read_all(self) -> list[dict]:
        if not os.path.exists(self.path):
            return []
        with open(self.path, encoding="utf-8") as fh:
            return [json.loads(line) for line in fh if line.strip()]

    def read_kind(self, kind: str) -> list[dict]:
        return [r for r in self.read_all() if r.get("kind") == kind]
