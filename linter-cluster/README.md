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
