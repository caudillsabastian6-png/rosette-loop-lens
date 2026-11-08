"""Glass Box receipts — the receipt format + emission (fusion leg 4;
pulled forward from Phase 3 / Task 6; serves R8, R10.3).

RECEIPT FORMAT (v1) — one JSON object per event, JSONL in the lanes' logs:

    {
      "receipt_version": 1,
      "receipt_id": "<12 hex>",
      "kind": "check" | "volley_item" | "job" | "promotion" | "abort"
              | "seat_action",
      "created_at": "<UTC ISO-8601>",
      "lane": "<lane name — lanes are never blended>",
      "thresholds": {...},                  # the bars that applied
      "exemplars_compared": [{"identity": "<id>", "score": <float>}],
      "tells_fired": ["<tell name>", ...],
      "reader_identity_report": {"identity": "...", ...} | null,
      "gate_decision": "pass" | "fail" | "pending" | "promoted"
                       | "aborted" | null,
      "verdict": "Likely Genuine" | "Likely Counterfeit"
                 | "Inconclusive" | null,
      "verification": {...}                 # hash checks, snapshot ids, ...
    }

Rules (fusion design §4.3, §6):
- Exemplars appear as IDENTITIES + SCORES only.
- The reader reports identity only and never votes: a receipt carries
  the reader's identity report, never a reader verdict.
- Verdict vocabulary is exactly the three house lanes; anything else is
  rejected at emission time.
- Receipts contain NO crown-jewel data: no bank images, no keys, no
  secrets, no other users' scans. ``validate_receipt`` enforces this by
  rejecting forbidden field names and image payloads anywhere nested.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field

RECEIPT_VERSION = 1
VERDICT_VOCABULARY = ("Likely Genuine", "Likely Counterfeit", "Inconclusive")
RECEIPT_KINDS = ("check", "volley_item", "job", "promotion", "abort",
                 "seat_action")

_FORBIDDEN_KEY_PARTS = ("image", "private_key", "api_key", "secret",
                        "password", "credential", "base64", "bank_file")


class ReceiptError(ValueError):
    pass


def _scan_for_jewels(node, path="receipt"):
    if isinstance(node, dict):
        for key, value in node.items():
            lowered = str(key).lower()
            if any(part in lowered for part in _FORBIDDEN_KEY_PARTS):
                raise ReceiptError(
                    f"forbidden field {key!r} at {path}: receipts carry no "
                    "crown-jewel data (no bank images, no keys)")
            _scan_for_jewels(value, f"{path}.{key}")
    elif isinstance(node, (list, tuple)):
        for i, value in enumerate(node):
            _scan_for_jewels(value, f"{path}[{i}]")
    elif isinstance(node, str):
        if node.startswith("data:image") or node.startswith("data:application"):
            raise ReceiptError(f"embedded payload at {path}: receipts carry "
                               "identities and scores, never image data")


def validate_receipt(receipt: dict) -> dict:
    if receipt.get("receipt_version") != RECEIPT_VERSION:
        raise ReceiptError("receipt_version must be 1")
    if receipt.get("kind") not in RECEIPT_KINDS:
        raise ReceiptError(f"unknown receipt kind: {receipt.get('kind')!r}")
    verdict = receipt.get("verdict")
    if verdict is not None and verdict not in VERDICT_VOCABULARY:
        raise ReceiptError(
            f"verdict {verdict!r} is outside the house vocabulary "
            f"{VERDICT_VOCABULARY}")
    reader = receipt.get("reader_identity_report")
    if reader is not None:
        if not isinstance(reader, dict):
            raise ReceiptError("reader_identity_report must be an object")
        if "verdict" in reader or "vote" in reader:
            raise ReceiptError("the reader reports identity only; it never votes")
    for exemplar in receipt.get("exemplars_compared") or []:
        if not isinstance(exemplar, dict) or set(exemplar) - {"identity", "score"}:
            raise ReceiptError(
                "exemplars are recorded as identity + score only")
    _scan_for_jewels(receipt)
    return receipt


@dataclass
class GlassBoxReceipt:
    kind: str
    lane: str
    thresholds: dict = field(default_factory=dict)
    exemplars_compared: list = field(default_factory=list)
    tells_fired: list = field(default_factory=list)
    reader_identity_report: dict | None = None
    gate_decision: str | None = None
    verdict: str | None = None
    verification: dict = field(default_factory=dict)
    receipt_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    created_at: str = field(
        default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

    def to_dict(self) -> dict:
        return validate_receipt({
            "receipt_version": RECEIPT_VERSION,
            "receipt_id": self.receipt_id,
            "kind": self.kind,
            "created_at": self.created_at,
            "lane": self.lane,
            "thresholds": self.thresholds,
            "exemplars_compared": self.exemplars_compared,
            "tells_fired": self.tells_fired,
            "reader_identity_report": self.reader_identity_report,
            "gate_decision": self.gate_decision,
            "verdict": self.verdict,
            "verification": self.verification,
        })

    def emit(self, log) -> dict:
        """Append this receipt as one JSON line to a lane log.

        ``log`` is a text stream or a list (tests/collectors). Returns the
        validated receipt dict. Emission validates first — an invalid
        receipt is never written."""
        record = self.to_dict()
        line = json.dumps(record, ensure_ascii=False, sort_keys=True)
        if hasattr(log, "append"):
            log.append(line)
        else:
            log.write(line + "\n")
            if hasattr(log, "flush"):
                log.flush()
        return record


def replay_outcome(receipt: dict) -> tuple:
    """The outcome a replay must reproduce from the record alone (R8):
    (kind, lane, verdict, gate_decision)."""
    validate_receipt(receipt)
    return (receipt["kind"], receipt["lane"], receipt.get("verdict"),
            receipt.get("gate_decision"))
