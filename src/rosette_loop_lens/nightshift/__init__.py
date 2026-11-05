"""Lane B — Night Shift + Rewind (in sync; serves R5, R6, R7).

Long unattended house jobs run inside the chassis sandbox. Output lands only in
staging; before a job may touch shared state a Rewind snapshot is taken and
hash-verified; promotion out of staging is a separate gated act (designated-fake
check -> hash verify -> examiner read). Nothing becomes truth by itself.

Scaffold stub — components are filled in by tasks 11-14.
"""
