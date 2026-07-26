# L1 linter-cluster session output (byte-exact mirror)

FINAL cumulative file-set from the FABLE-CODE-SESSION-linter-cluster autonomous run (2026-07-24/25).
Canonical review deliverables (per-item reports, diffs, session log) live in the Box exchange folder `outbox/`.
This branch mirrors the FINAL files byte-exactly (the Box MCP pipe is text-based; git is sha-verifiable) plus the per-item incremental diffs.

Verify: shasum linter-cluster/*
- layer1_lint.py       a87ce5101fe82ff10af67e4dc0b24c9771c0e6f7 (107222 B)
- test_layer1_lint.py  31d74400b7a9f9064a49f0ea52ff8df3f485e39a (54983 B)
- manifest.yaml        0397bfd11cfe8023aa7eb4808681d0bd598ddad3 (3748 B)
- baseline.md          dd5da45a1f93963c6f1c381e9dcd292f6f79333d (48992 B, UNCHANGED input)

Gates: python3 linter-cluster/layer1_lint.py --selftest -> 89/89 PASS exit 0.
REV1 (2026-07-25): item 07 revised per Gemini Finding 1 — non-dict pointed_to_docs.gate_v
no longer crashes the P02 recorded-pin lookup (clean FAIL) + fixture PN09; diffs/item7.diff updated.
DRAFT + LOCAL-VERIFY ONLY: nothing here is applied to any governed substrate; Gemini review + GATE-V application are downstream.

## 869drd6uy tier-engine modular split (2026-07-26)

The engine now ships as an entrypoint shim + the `l1lint/` package (verbatim-slice split of
the a87ce510 monolith; the monolith's bytes are preserved as `oracle_layer1_lint.py`).
Invocation unchanged: `python3 linter-cluster/layer1_lint.py --selftest` -> 89/89 PASS exit 0.

Verify: shasum linter-cluster/layer1_lint.py linter-cluster/l1lint/* (full table incl.
per-module monolith line-ranges: MODULE-MAP.md; machine-readable: split_ledger.json;
review evidence: REVIEW-FEED.md + evidence/).
- oracle_layer1_lint.py  a87ce5101fe82ff10af67e4dc0b24c9771c0e6f7 (107222 B, frozen monolith)
- test_layer1_lint.py / manifest.yaml / baseline.md unchanged (hashes above).

Gates: --selftest 89/89 (stdout+stderr byte-identical to the oracle) AND the full Phase-A
oracle differential — `python3 linter-cluster/test_layer1_lint.py --phase A` -> OVERALL
Phase A: PASS (1151/1151 content+fuzz as-expected, determinism K=3 STABLE, zero deltas
declared; transcript: evidence/diff_phaseA.log).
DRAFT + LOCAL-VERIFY ONLY: nothing here is applied to any governed substrate; Gemini review
+ GATE-V application are downstream.
