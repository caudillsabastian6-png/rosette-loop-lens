"""Promotion gate (Task 13; R7, R10, R12).

The only door from staging to truth, in order: designated-fake record check ->
payload hash verify against recorded hashes -> examiner read. Any failure
aborts with shared state untouched and the abort receipted; every promotion
names the Rewind snapshot it was made against.

Scaffold stub — no implementation yet.
"""
