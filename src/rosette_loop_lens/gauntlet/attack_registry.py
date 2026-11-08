"""Attack-set registry (fusion leg 2 scaffold; Task 7; R2.2-R2.4, R12).

Per-lane registration under the Nov 2, 2026 lane-separation ruling:
manufactured lanes stay separated and are never blended into — or scored
against — the frozen physical core. Lanes:

- ``printed_pair_sheet``       — Chris's printed pair-sheet fakes
- ``crew_manufactured_digital``— Foundry-manufactured digital fakes
- ``crew_manufactured_cardstock`` — future manufactured cardstock sheets

Intake rules (all recorded, refusals included):
- The designated-fake record check runs FIRST: an item is registered
  only when it is confirmed designated-fake manufactured material.
- Any non-manufactured material is refused — physical-core material is
  never attack fodder, and genuine material never enters a volley.
- Every registered item carries the honesty label
  ``simulated/manufactured`` on every surface.
"""

from __future__ import annotations

from dataclasses import dataclass, field

LANES = ("printed_pair_sheet", "crew_manufactured_digital",
         "crew_manufactured_cardstock")
HONESTY_LABEL = "simulated/manufactured"


class RegistrationRefused(ValueError):
    pass


@dataclass
class AttackItem:
    item_id: str
    lane: str
    label: str = HONESTY_LABEL
    source: str = "crew-manufactured"

    def describe(self) -> dict:
        return {"item_id": self.item_id, "lane": self.lane,
                "label": self.label, "source": self.source}


@dataclass
class AttackRegistry:
    refusals: list = field(default_factory=list)
    _items: dict = field(default_factory=dict)  # lane -> [AttackItem]

    def register(self, item_id: str, lane: str, *, designated_fake: bool,
                 manufactured: bool = True, source: str = "crew-manufactured") -> AttackItem:
        """Register one attack item, or record a refusal and raise.

        ``designated_fake`` is the caller's attestation that the
        designated-fake record check was run for this item and confirms
        it as designated-fake material. The registry records the check;
        it cannot be skipped — there is no parameter to bypass it."""
        reason = None
        if lane not in LANES:
            reason = (f"lane {lane!r} is not a manufactured lane; the frozen "
                      "physical core is never a Gauntlet lane")
        elif not manufactured:
            reason = "non-manufactured material refused: physical/genuine material is never attack fodder"
        elif not designated_fake:
            reason = "designated-fake record check did not confirm this item as designated-fake material"
        if reason is not None:
            self.refusals.append({"item_id": item_id, "lane": lane,
                                  "refused": reason})
            raise RegistrationRefused(reason)
        item = AttackItem(item_id=item_id, lane=lane, source=source)
        self._items.setdefault(lane, []).append(item)
        return item

    def items(self, lane: str) -> list:
        return list(self._items.get(lane, []))

    def all_items(self) -> list:
        out = []
        for lane in LANES:  # fixed lane order; lanes never merged in output
            out.extend(self._items.get(lane, []))
        return out

    def counts(self) -> dict:
        return {lane: len(self._items.get(lane, [])) for lane in LANES}
