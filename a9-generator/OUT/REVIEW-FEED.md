# REVIEW-FEED — A9 generator delivery — 2026-09-06

**Purpose.** Evidence pack for the independent reviewer. It states what the inputs were, what was produced,
what changed item by item, and what is unverified. It contains no review criteria and draws no conclusion
about the quality of the output.

**Producer.** Max drafting seat (Fable, `claude-fable-5-1`) · Box identity rodwel@me.com (`183820787`) · Box MCP
connector only (reads by direct folder/file id; text uploads) · Authority: NONE. Output type: code-change set
(generator files + generated manifests) with authored documents.

---

## (a) GROUND TRUTH — pre-state

### IN `415602830059` — 17 items; server-side sha1/size; listed before the run and again after it (unchanged)

| file | Box id | bytes | sha1 |
|---|---|---|---|
| `APPENDIX-C-SLICE-sectioned-oracle-2026-09-06.md` | 2449866507942 | 7,837 | `a7acd7796821062cdaef170a0aa39164bf20a2fa` |
| `CHECKPOINT-oracle-codecli-2026-09-04.md` | 2449861192168 | 77,165 | `b765d4ee82740c71819204f64abcd9a795093039` |
| `corpus-boxlive-2026-09-06.json` | 2449860815455 | 1,600 | `9c1997090fe403476554168a2aaee3abf8e28b87` |
| `GENERATOR-INPUTS.md` | 2449860347356 | 8,483 | `caa21050afa7cfbbf3bad3b3a13a9bfcb07a1dde` |
| `HANDOFF.md` | 2449864551821 | 11,886 | `84ba9e990456a401ead8c8e88fa6c33898259a7a` |
| `inventory-390802629329-2026-09-04-1650Z.json` | 2450234898780 | 350,581 | `94cb9b1a4efbf96ac10a8a60e9c77c096721e447` |
| `manifest-live.json` | 2449861430379 | 2,425 | `e5993c1de7d888e308f5b5a09a2f89810e74ae8d` |
| `manifest-sealed.json` | 2449863955142 | 2,419 | `6049beb18899cb06379a9bd34b8a382cfd3c4905` |
| `OPEN-DECISIONS-oracle-2026-09-06.md` | 2449865068792 | 8,310 | `bee1671b0208ebcfc284bd8fae8f0dcbd61cde56` |
| `OPEN-ITEMS-DISPOSITION-2026-09-06.md` | 2449859195133 | 11,004 | `9028ffead4fb7a362f6d52d74ad0d87b73a16ffe` |
| `oracle-model-SETPIN-2026-07-28.json` | 2450238904095 | 1,513 | `9f4fc6c7d28e0bc27d1288ae04aee10f35cc4982` |
| `oracle_gen.py` | 2449860666966 | 18,690 | `d9485e36989b859dc6423bec52b4c09a0aa26a1a` |
| `oracle_lint.py` | 2449860388492 | 10,753 | `7137aab2c1da72f017f317c06d1985eb8bd49f22` |
| `README-PROTOTYPE.md` | 2449862905859 | 11,258 | `46a65f8ac01cf294305e1fb4d92e886eb3d78727` |
| `rules_as_data.yaml` | 2449859682122 | 4,920 | `314c5174c1b5dbce14560e2c4d9838068859dbee` |
| `SEEDS-RUNBOOK.md` | 2450241224989 | 7,797 | `69ab5edefc2542292619613f1e6f73c7f582550b` |
| `SET-IDENTITY-live-computation-2026-09-04.md` | 2450238882415 | 5,225 | `1dd432c5f1931ec7519830ef781ac40f07efe79a` |

### OUT `415603610278` — empty before the run (`totalCount` 0).

### Recorded expected pins (from `rules_as_data.yaml`, which was not changed)

| key | value | status in the rules |
|---|---|---|
| `engine_set.engine15_set_sha1` | `9520867753d0d26ec76e959d1a98a450d24255fa` | LIVE-POSITIVE |
| `engine_set.set16_set_sha1_live` | `df59d6f66748ba6e45e897ca724dc1126a3a536e` | LIVE-POSITIVE |
| `engine_set.set16_set_sha1_sealed` | `ccda65118beb01d742c60f86cea140828de2ad9d` | NEGATIVE-GUARD |
| `harness.file_sha1_live` | `a3e678f22dd1b4a8e89005e4c1f5d668e4c92b85` | LIVE-POSITIVE |
| `harness.file_sha1_sealed` | `3574c2d13a7f34f7cd8d1bac3543b05556e18ef9` | NEGATIVE-GUARD |

### Access facts at the start
- `who_am_i` → user `183820787`, login rodwel@me.com.
- Folders `396978339615` and `403356419210` → *Item not found* (both list and details calls). Folder `402946233341`
  (exchange parent) → *Item not found*. Folders `415602830059` (IN) and `415603610278` (OUT) → readable by id.
- Environment: Python 3.11.15, PyYAML 6.0.1; no `Level 1 - Dev` tree; no raw Box credential.

## (b) OUTPUT — post-state of OUT `415603610278`

| file | Box id | bytes | sha1 (server read-back) |
|---|---|---|---|
| `oracle_gen.py` | 2450306185463 | 18,690 | `d9485e36989b859dc6423bec52b4c09a0aa26a1a` |
| `oracle_lint.py` | 2450307280287 | 10,753 | `7137aab2c1da72f017f317c06d1985eb8bd49f22` |
| `rules_as_data.txt` | 2450303541471 | 4,920 | `314c5174c1b5dbce14560e2c4d9838068859dbee` |
| `manifest-live.json` | 2450301277807 | 2,425 | `e5993c1de7d888e308f5b5a09a2f89810e74ae8d` |
| `manifest-sealed.json` | 2450305456260 | 2,419 | `6049beb18899cb06379a9bd34b8a382cfd3c4905` |
| `corpus-boxlive-2026-09-06.json` | 2450298608696 | 1,600 | `9c1997090fe403476554168a2aaee3abf8e28b87` |
| `manifest-boxlive-2026-09-06.json` | 2450304675825 | 2,449 | `54a545534922360cc7c35e595e25f92e234ede3b` |
| `VALIDATION-LOG-2026-09-06.md` | 2450306787923 | 13,768 | `5f79e66f5be093cdf44b35e187182796e8af9eaa` |
| `PROPOSED-PATCH-oracle_lint-boxlive-L9.txt` | assigned at upload — see session report | 1,498 | local `95bf61c494cd82c12e3382bdf81181d61f383fde` |
| `HANDOFF-BACK.md` | assigned at upload — see session report | — | local sha1 in the session report |
| `REVIEW-FEED.md` | assigned at upload — see session report | — | this file |

All rows with a Box id were read back with `version_number` 1, `created_by` `183820787`, `item_status` active,
parent `415603610278`.

Generated-manifest content: `manifest-boxlive-2026-09-06.json` carries `corpus_source.kind = "boxlive"`,
`path = "corpus-boxlive-2026-09-06.json"`, `read_at = "2026-09-06"`, `source_folders = {root: 396978339615,
l1lint: 403356419210}`, `oracle_version = "v0.2-PROTOTYPE"`, `rules_digest = 314c5174…`, `engine15_set_sha1 =
9520…`, `set16_set_sha1 = df59…`, `harness.file_sha1 = a3e6…`, 16 members sorted by relpath.

## (c) CHANGE-MANIFEST — per item, factual

| item | what happened |
|---|---|
| `oracle_gen.py` | Copied IN → OUT. No byte change (sha1 equal). No code edit made. |
| `oracle_lint.py` | Copied IN → OUT. No byte change. No code edit made. |
| `rules_as_data.yaml` | Bytes unchanged (sha1 equal). Stored in OUT under the name `rules_as_data.txt` because the upload connector does not accept the `.yaml` extension. |
| `manifest-live.json` | Regenerated by `oracle_gen.py gen --source live` from the staged inventory; output compared with `cmp` to the staged file: identical. |
| `manifest-sealed.json` | Regenerated by `oracle_gen.py gen --source sealed` from the staged setpin; `cmp` identical. |
| `corpus-boxlive-2026-09-06.json` | Copied IN → OUT unchanged. |
| `manifest-boxlive-2026-09-06.json` | Newly generated by `oracle_gen.py gen --source boxlive` from the staged snapshot. |
| `VALIDATION-LOG-2026-09-06.md` | New. A header written by the producer followed by verbatim machine output of one scripted run (13 commands). |
| `PROPOSED-PATCH-oracle_lint-boxlive-L9.txt` | New. A unified diff made with `diff -u` between the staged `oracle_lint.py` and a scratch copy edited in three places (L9 kind map gains `boxlive`; `load_corpus` receives `args.boxlive`; a `--boxlive` argument is added). Header lines annotated. Applied to nothing in IN or OUT. |
| `HANDOFF-BACK.md` | New, authored: verified inputs, pins as re-derived from staged corpora, OUT inventory, a target recommendation, the write-time steps for the promotion seat, the validation table, anomalies. |
| `REVIEW-FEED.md` | New, authored: this file. |
| IN `415602830059` | No item created, modified, moved or deleted; 17/17 server sha1s equal before and after. |
| Other Box locations | No write. |
| Outside Box | The OUT set, with the rules file named `rules_as_data.yaml`, committed to GitHub branch `claude/oracle-gen-a9-delivery-i5xmkb` of `rodwel-cmyk/temp` (commit hash in the session report). |

Validation outputs, verbatim, are in `VALIDATION-LOG-2026-09-06.md`; the summarised table is in HANDOFF-BACK §6.

## (d) OPEN QUESTIONS / RISKS — what is unverified or uncertain

1. **No live read of the engine.** Folders `396978339615` / `403356419210` were not readable by this identity, so
   every MATCH is against staged, dated inputs: the inventory (2026-09-04 16:50Z) and the snapshot (2026-09-06, read by
   the Teams seat). Whether the engine is unchanged at this moment is unknown from here.
2. **Single-machine, single-seat claims.** Every validation result comes from one run on one machine by the producer.
   No independent re-run has occurred yet.
3. **Transfer path.** Every file passed through the model as text at two hops (Box → disk, disk → Box). Each hop was
   checked by sha1 against the Box server value, but the same connector performed the read and the write and the read-back.
4. **The proposed L9 patch** was tested on a scratch copy only; it would change `oracle_lint.py`'s sha1 (to
   `69b11a31d42cf248567d100786e9d4d64d7b5932` if applied verbatim); it carries no version bump; README-PROTOTYPE §1A says
   `--enforce` is to be promoted "only after S8 extends this to every section" — whether extending L9 to the `boxlive`
   kind falls inside S7/S8's intended scope is not ruled anywhere in the inputs.
5. **Target recommendation ungrounded in a live read.** HANDOFF-BACK §4 recommends a new subfolder under `396978339615`
   with new-file creates; the target's existence, lock state, ancestors, container guard and principal were not observed.
6. **Instrument deviation.** HANDOFF §4's raw-API procedure and `box_rw.py` were not available; the MCP connector was
   the write instrument. CHECKPOINT §20.3 records the launch prompt naming `box_rw.py` "explicitly NOT the MCP path" for
   the S9 write; whether that preference also governs staging into an exchange OUT folder is not stated in the inputs.
7. **Two Teams-side principals.** The staged snapshot's `_note` attributes the read to `mail@rodwell.biz` (10546707);
   HANDOFF attributes the staging to CCG `52284892504`. Which principal produced the snapshot is not verifiable here.
8. **Provenance dates differ.** `manifest-live.json` declares the 2026-09-04 inventory as its corpus; the snapshot-derived
   manifest declares 2026-09-06. Their pins are equal; their corpus dates are two days apart.
9. **Inventory checked by shape only** — 722 records, root id present once, 21 file records under the Tooling path. No
   member sha1 inside it was re-derived from bytes (by design: hash-not-ingest).
10. **Appendix C slice** — parent document not in IN; the cited parent sha1 could not be checked.
11. **Name-dependent consumer.** OUT contains no file literally named `rules_as_data.yaml`; a consumer running the OUT set
    as stored will fail at the `RULES` path until the file is renamed.
12. **Authored prose.** The VALIDATION-LOG header, HANDOFF-BACK and this file were written by the producer; only the log
    body under the fence is machine output.
13. **Search results as a side observation.** A Box name search under this identity returned 435 hits for the engine file
    names in exchange/archive folders, several with sha1s equal to engine members. None was used; their existence is
    recorded because it bears on identity-by-name hazards already noted in CHECKPOINT §12.6.

*END of evidence. No verdict is offered here.*
