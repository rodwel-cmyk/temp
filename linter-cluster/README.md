# L1 linter-cluster session output (byte-exact mirror)

FINAL cumulative file-set from the FABLE-CODE-SESSION-linter-cluster autonomous run (2026-07-24/25).
Canonical review deliverables (per-item reports, diffs, session log) live in the Box exchange folder `outbox/`.
This branch mirrors the FINAL files byte-exactly (the Box MCP pipe is text-based; git is sha-verifiable) plus the per-item incremental diffs.

Verify: shasum linter-cluster/*
- layer1_lint.py       089b42f9e293ef0763f25ae3b28b8739e915505c (107164 B)
- test_layer1_lint.py  e629d353fc44d66b7523984051a2f3edf1479045 (54243 B)
- manifest.yaml        0397bfd11cfe8023aa7eb4808681d0bd598ddad3 (3748 B)
- baseline.md          dd5da45a1f93963c6f1c381e9dcd292f6f79333d (48992 B, UNCHANGED input)

Gates: python3 linter-cluster/layer1_lint.py --selftest -> 88/88 PASS exit 0.
DRAFT + LOCAL-VERIFY ONLY: nothing here is applied to any governed substrate; Gemini review + GATE-V application are downstream.
